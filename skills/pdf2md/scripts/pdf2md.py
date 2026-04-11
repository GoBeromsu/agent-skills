#!/usr/bin/env python3
"""
pdf2md — Convert PDF to Markdown using Upstage Document Parse API.

Merge-first architecture:
  Phase 1: API call → single merged.md + headings.json + assets/*.png
  Phase 2: Optional split from merged output based on heading pattern

Usage:
  # Convert (estimate only, no --confirm)
  python3 pdf2md.py input.pdf --output-dir /tmp/pdf2md_output

  # Convert (execute API call)
  python3 pdf2md.py input.pdf --output-dir /tmp/pdf2md_output --confirm

  # Split from existing output
  python3 pdf2md.py --split-from /tmp/pdf2md_output --split-pattern "Part" --output-dir /tmp/pdf2md_split
  python3 pdf2md.py --split-from /tmp/pdf2md_output --split-on-h1 --output-dir /tmp/pdf2md_split
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://api.upstage.ai/v1"
SYNC_ENDPOINT = f"{API_BASE}/document-digitization"
ASYNC_ENDPOINT = f"{API_BASE}/document-digitization/async"
ASYNC_STATUS_ENDPOINT = f"{API_BASE}/document-digitization/requests"
DEFAULT_MODEL = "document-parse-251217"
DEFAULT_MODE = "auto"
MAX_SYNC_PAGES = 100
POLL_INTERVAL = 10
MAX_POLL_ITERATIONS = 120  # 20 min max


def get_api_key():
    key = os.environ.get("UPSTAGE_API_KEY")
    if not key:
        print("ERROR: UPSTAGE_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return key


def get_page_count(pdf_path: str) -> int:
    """Get PDF page count using macOS native tools."""
    # Try mdls first (Spotlight metadata, fastest)
    try:
        result = subprocess.run(
            ["mdls", "-name", "kMDItemNumberOfPages", pdf_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            match = re.search(r"(\d+)", result.stdout)
            if match:
                return int(match.group(1))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback to pdfinfo (poppler)
    try:
        result = subprocess.run(
            ["pdfinfo", pdf_path],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.startswith("Pages:"):
                    return int(line.split(":")[1].strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print("WARNING: Could not determine page count. Assuming sync mode (≤100p).", file=sys.stderr)
    return -1


def detect_category_field(elements: list) -> str:
    """Detect whether API uses 'category' or 'type' for element classification."""
    if not elements:
        return "category"
    sample = elements[0]
    if "category" in sample:
        return "category"
    if "type" in sample:
        return "type"
    return "category"


def call_sync_api(pdf_path: str, api_key: str, model: str, mode: str) -> dict:
    """Call the sync Document Parse API (≤100 pages)."""
    headers = {"Authorization": f"Bearer {api_key}"}
    with open(pdf_path, "rb") as f:
        files = {"document": (Path(pdf_path).name, f, "application/pdf")}
        data = {
            "model": model,
            "output_formats": '["markdown"]',
            "base64_encoding": '["figure"]',
            "mode": mode,
        }
        print(f"  Calling sync API (model={model}, mode={mode})...")
        response = requests.post(
            SYNC_ENDPOINT, files=files, data=data, headers=headers, timeout=300
        )

    if response.status_code == 401:
        print("ERROR: API key expired or invalid.", file=sys.stderr)
        sys.exit(1)
    if response.status_code == 429:
        print("ERROR: Rate limited. Wait and retry.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()
    return response.json()


def call_async_api(pdf_path: str, api_key: str, model: str, mode: str) -> dict:
    """Call the async Document Parse API (>100 pages) with polling and batch merging."""
    headers = {"Authorization": f"Bearer {api_key}"}

    # Submit
    with open(pdf_path, "rb") as f:
        files = {"document": (Path(pdf_path).name, f, "application/pdf")}
        data = {
            "model": model,
            "output_formats": '["markdown"]',
            "base64_encoding": '["figure"]',
            "mode": mode,
        }
        print(f"  Submitting async API request (model={model}, mode={mode})...")
        response = requests.post(
            ASYNC_ENDPOINT, files=files, data=data, headers=headers, timeout=60
        )

    if response.status_code == 401:
        print("ERROR: API key expired or invalid.", file=sys.stderr)
        sys.exit(1)
    response.raise_for_status()
    request_id = response.json()["request_id"]
    print(f"  Request ID: {request_id}")

    # Poll
    for i in range(MAX_POLL_ITERATIONS):
        time.sleep(POLL_INTERVAL)
        status_resp = requests.get(
            f"{ASYNC_STATUS_ENDPOINT}/{request_id}",
            headers=headers, timeout=30
        )
        status_resp.raise_for_status()
        status_data = status_resp.json()
        status = status_data.get("status", "unknown")
        completed = status_data.get("completed_pages", 0)
        total = status_data.get("total_pages", "?")
        print(f"  Polling [{i+1}/{MAX_POLL_ITERATIONS}]: {status} ({completed}/{total} pages)")

        if status == "completed":
            return _download_and_merge_batches(status_data, headers)
        if status == "failed":
            msg = status_data.get("failure_message", "Unknown error")
            print(f"ERROR: Async processing failed: {msg}", file=sys.stderr)
            sys.exit(1)

    print("ERROR: Async polling timed out.", file=sys.stderr)
    sys.exit(1)


def _download_and_merge_batches(status_data: dict, headers: dict) -> dict:
    """Download all batches immediately, merge elements in page order with dedup."""
    batches = status_data.get("batches", [])
    if not batches:
        print("ERROR: No batches in async result.", file=sys.stderr)
        sys.exit(1)

    # Sort batches by start_page
    batches.sort(key=lambda b: b.get("start_page", 0))

    # Download all immediately (15min URL expiry protection)
    print(f"  Downloading {len(batches)} batches...")
    batch_results = []
    for batch in batches:
        url = batch.get("download_url")
        if not url:
            print(f"  WARNING: Batch {batch.get('id')} has no download_url, skipping.", file=sys.stderr)
            continue
        resp = requests.get(url, headers=headers, timeout=120)
        resp.raise_for_status()
        batch_results.append(resp.json())

    # Merge elements with dedup by (page, id)
    seen = set()
    all_elements = []
    full_markdown_parts = []

    for result in batch_results:
        elements = result.get("elements", [])
        for elem in elements:
            page = elem.get("page", 0)
            elem_id = elem.get("id", id(elem))
            key = (page, elem_id)
            if key not in seen:
                seen.add(key)
                all_elements.append(elem)
        # Collect full markdown content if available
        content = result.get("content", {})
        if content.get("markdown"):
            full_markdown_parts.append(content["markdown"])

    # Sort by (page, id)
    all_elements.sort(key=lambda e: (e.get("page", 0), e.get("id", 0)))

    # Build merged response structure
    merged = {
        "elements": all_elements,
        "content": {
            "markdown": "\n\n".join(full_markdown_parts),
        },
        "usage": {"pages": status_data.get("total_pages", 0)},
        "model": status_data.get("model", DEFAULT_MODEL),
    }
    return merged


def extract_figures(elements: list, cat_field: str, output_dir: Path, book_slug: str) -> dict:
    """Extract figure elements as PNG files. Returns {element_id: filename} mapping."""
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    figure_map = {}
    fig_count = 0

    for elem in elements:
        category = elem.get(cat_field, "")
        if category != "figure":
            continue

        b64_data = elem.get("base64_encoding")
        if not b64_data:
            continue

        fig_count += 1
        filename = f"{book_slug}_fig_{fig_count}.png"
        filepath = assets_dir / filename

        try:
            img_bytes = base64.b64decode(b64_data)
            # Skip tiny decorative images (chapter dividers, ornaments)
            if len(img_bytes) < 10000:
                print(f"  Skipped decorative figure: {filename} ({len(img_bytes)} bytes)")
                fig_count -= 1
                continue
            filepath.write_bytes(img_bytes)
            elem_id = elem.get("id", fig_count)
            figure_map[elem_id] = filename
            print(f"  Extracted figure: {filename} ({len(img_bytes)} bytes)")
        except Exception as e:
            print(f"  WARNING: Failed to decode figure {fig_count}: {e}", file=sys.stderr)

    return figure_map


def build_headings_json(elements: list, cat_field: str) -> list:
    """Extract heading elements into a structured list."""
    headings = []
    heading_categories = {"heading1", "heading2", "heading3", "heading4", "heading5"}

    for i, elem in enumerate(elements):
        category = elem.get(cat_field, "")
        if category in heading_categories:
            level = int(category[-1])
            text = ""
            content = elem.get("content", {})
            if isinstance(content, dict):
                text = content.get("markdown", "") or content.get("text", "")
            elif isinstance(content, str):
                text = content
            # Clean heading markers from text
            text = re.sub(r"^#+\s*", "", text.strip())

            headings.append({
                "index": i,
                "level": level,
                "text": text,
                "page": elem.get("page", 0),
            })

    return headings


def assemble_markdown(elements: list, cat_field: str, figure_map: dict) -> str:
    """Assemble elements into a single markdown document with wikilink image references."""
    parts = []
    fig_counter = 0

    for elem in elements:
        category = elem.get(cat_field, "")
        elem_id = elem.get("id")

        # Figure → wikilink image
        if category == "figure":
            if elem_id in figure_map:
                filename = figure_map[elem_id]
                # Just embed the image, skip API placeholder junk and figcaption HTML
                parts.append(f"![[{filename}]]")
            # Figure without base64 or not in figure_map — skip
            continue

        # All other elements — use markdown content
        content = elem.get("content", {})
        if isinstance(content, dict):
            md = content.get("markdown", "") or content.get("text", "")
        elif isinstance(content, str):
            md = content
        else:
            continue

        md = md.strip()
        if md:
            parts.append(md)

    return "\n\n".join(parts)


def verify(elements: list, cat_field: str, markdown: str, figure_map: dict,
           output_dir: Path, page_count: int) -> dict:
    """Run verification checks on the conversion output."""
    headings = build_headings_json(elements, cat_field)
    assets_dir = output_dir / "assets"

    # 1. Heading hierarchy check
    heading_levels_valid = True
    for h in headings:
        if h["level"] < 1 or h["level"] > 6:
            heading_levels_valid = False
            break

    # 2. Image links check
    wikilink_pattern = re.compile(r"!\[\[([^\]]+)\]\]")
    image_refs = wikilink_pattern.findall(markdown)
    missing_images = []
    for ref in image_refs:
        if not (assets_dir / ref).exists():
            missing_images.append(ref)
    image_links_valid = len(missing_images) == 0

    # 3. Text completeness — compare assembled markdown against sum of all element content
    #    Uses whichever field has content (markdown or text), skipping header/footer
    raw_text_length = 0
    skip_categories = {"header", "footer"}
    for elem in elements:
        if elem.get(cat_field, "") in skip_categories:
            continue
        content = elem.get("content", {})
        if isinstance(content, dict):
            text = content.get("markdown", "") or content.get("text", "")
        elif isinstance(content, str):
            text = content
        else:
            text = ""
        raw_text_length += len(text.strip())

    # Strip only wikilink image embeds for fair comparison (not captions/formatting)
    md_text_only = re.sub(r"!\[\[[^\]]+\]\]", "", markdown)
    text_ratio = len(md_text_only.strip()) / max(raw_text_length, 1)

    # 4. Figure count match
    api_figure_count = sum(1 for e in elements if e.get(cat_field) == "figure")
    extracted_figure_count = len(figure_map)
    # Some figures may not have base64, so extracted ≤ api count
    figure_match = extracted_figure_count <= api_figure_count

    # 5. Element coverage
    total_elements = len(elements)
    processed = sum(1 for e in elements if e.get(cat_field, "") not in {"header", "footer"})

    warnings = []
    if not heading_levels_valid:
        warnings.append("Invalid heading levels detected")
    if missing_images:
        warnings.append(f"Missing image files: {missing_images}")
    if text_ratio < 0.90:
        warnings.append(f"Low text ratio: {text_ratio:.2%}")
    elif text_ratio < 0.95:
        warnings.append(f"Text ratio slightly below target: {text_ratio:.2%}")
    if api_figure_count > 0 and extracted_figure_count == 0:
        warnings.append(f"API returned {api_figure_count} figures but none were extracted")
    if extracted_figure_count < api_figure_count:
        warnings.append(
            f"Extracted {extracted_figure_count}/{api_figure_count} figures "
            f"({api_figure_count - extracted_figure_count} missing base64)"
        )

    passed = (
        heading_levels_valid
        and image_links_valid
        and text_ratio >= 0.90
        and figure_match
    )

    return {
        "passed": passed,
        "heading_count": len(headings),
        "heading_hierarchy_valid": heading_levels_valid,
        "image_count": len(image_refs),
        "image_links_valid": image_links_valid,
        "missing_images": missing_images,
        "text_ratio": round(text_ratio, 4),
        "api_figure_count": api_figure_count,
        "extracted_figure_count": extracted_figure_count,
        "figure_match": figure_match,
        "element_coverage": round(processed / max(total_elements, 1), 4),
        "total_elements": total_elements,
        "warnings": warnings,
    }


def split_markdown(merged_md: str, headings: list, pattern: str = None,
                   split_on_h1: bool = False) -> list:
    """Split merged markdown into parts based on heading pattern or h1 boundaries.

    Returns list of {title, content} dicts.
    """
    if not headings:
        return [{"title": "Full Document", "content": merged_md}]

    # Find split points
    h1_headings = [h for h in headings if h["level"] == 1]

    if not h1_headings:
        return [{"title": "Full Document", "content": merged_md}]

    if pattern:
        # Split only on h1 headings matching pattern
        split_headings = [h for h in h1_headings if pattern.lower() in h["text"].lower()]
    elif split_on_h1:
        split_headings = h1_headings
    else:
        return [{"title": "Full Document", "content": merged_md}]

    if not split_headings:
        return [{"title": "Full Document", "content": merged_md}]

    # Find line positions in markdown for each split heading
    lines = merged_md.split("\n")
    split_positions = []

    for sh in split_headings:
        heading_text = sh["text"].strip()
        for i, line in enumerate(lines):
            cleaned = re.sub(r"^#+\s*", "", line.strip())
            if cleaned == heading_text or heading_text in cleaned:
                split_positions.append({"line": i, "title": heading_text})
                break

    if not split_positions:
        return [{"title": "Full Document", "content": merged_md}]

    # Build parts
    parts = []

    # Content before first split point (Introduction, etc.)
    if split_positions[0]["line"] > 0:
        pre_content = "\n".join(lines[:split_positions[0]["line"]]).strip()
        if pre_content:
            parts.append({"title": "Introduction", "content": pre_content})

    # Split sections
    for idx, sp in enumerate(split_positions):
        start = sp["line"]
        end = split_positions[idx + 1]["line"] if idx + 1 < len(split_positions) else len(lines)
        content = "\n".join(lines[start:end]).strip()
        if content:
            parts.append({"title": sp["title"], "content": content})

    # Check if there's trailing content after the last split heading's content
    # (e.g., Conclusion that's not a split heading)
    # This is already handled by the end = len(lines) case above

    return parts


def escape_hash_numbers(markdown: str) -> str:
    """Escape #N) patterns that get misinterpreted as headings."""
    return re.sub(r"^#(\d+[\.\)])", r"\\#\1", markdown, flags=re.MULTILINE)


def fix_headings_with_toc(markdown: str, toc_data: dict) -> tuple:
    """Fix heading hierarchy using known TOC structure.

    Args:
        markdown: merged markdown from API
        toc_data: {
            "parts": {"Part 1: The Idea": 1, ...},       # text → heading level
            "chapters": {"Deep Work Is Valuable": 2, ...}, # text → heading level
            "sections": {"The High-Skilled Workers": 3, ...}
        }

    Returns:
        (fixed_markdown, fix_report)
    """
    all_known = {}
    for mapping in [toc_data.get("parts", {}),
                    toc_data.get("chapters", {}),
                    toc_data.get("sections", {})]:
        all_known.update(mapping)

    # Normalize for matching: strip, lower
    known_lower = {k.strip().lower(): (k, v) for k, v in all_known.items()}

    lines = markdown.split("\n")
    fixed_lines = []
    demoted = 0
    promoted = 0
    escaped = 0
    promoted_entries = []
    demoted_entries = []

    # Track which TOC entries were found (to detect missing headings)
    found_toc_entries = set()

    for line in lines:
        # Escape #N) patterns
        if re.match(r"^#\d+[\.\)]", line):
            fixed_lines.append(re.sub(r"^#(\d+[\.\)])", r"\\#\1", line))
            escaped += 1
            continue

        # Check if it's a heading
        m = re.match(r"^(#+)\s+(.+)$", line)
        if m:
            title = m.group(2).strip()
            title_lower = title.lower()

            if title_lower in known_lower:
                # Known TOC entry → use correct level
                original_name, target_level = known_lower[title_lower]
                new_line = f"{'#' * target_level} {title}"
                if new_line != line:
                    old_level = len(m.group(1))
                    if target_level > old_level:
                        demoted += 1
                        demoted_entries.append(title)
                    elif target_level < old_level:
                        promoted += 1
                        promoted_entries.append(title)
                fixed_lines.append(new_line)
                found_toc_entries.add(title_lower)
            else:
                # NOT in TOC → demote to plain text (OCR noise)
                # But keep it if it's short and looks like a real heading
                if len(title) > 80 or any(c in title for c in ['"', "'", "·", "www.", ":"]):
                    fixed_lines.append(title)  # plain text
                    demoted += 1
                    demoted_entries.append(title[:50])
                else:
                    # Unknown but plausible heading → h3 default
                    fixed_lines.append(f"### {title}")
                    if line != f"### {title}":
                        demoted += 1
                        demoted_entries.append(title)
                found_toc_entries.add(title_lower)
            continue

        # Check for Part markers in plain text → promote to heading
        part_match = re.match(r"^PART\s*(\d+)", line.strip(), re.IGNORECASE)
        if part_match:
            part_num = part_match.group(1)
            # Find matching part in TOC by number
            matched = False
            for key, (name, level) in known_lower.items():
                # Match "part N" in the key where N is the same number
                key_num_match = re.search(r"part\s*(\d+)", key)
                if key_num_match and key_num_match.group(1) == part_num:
                    fixed_lines.append(f"{'#' * level} {name}")
                    promoted += 1
                    promoted_entries.append(name)
                    found_toc_entries.add(key)
                    matched = True
                    break
            if not matched:
                fixed_lines.append(line)
            continue

        # Check for TOC entries that exist as plain text lines
        # Only promote if not already found as a heading (avoid duplicates)
        stripped = line.strip()
        stripped_lower = stripped.lower()
        if (stripped_lower in known_lower and stripped
                and not stripped.startswith("#")
                and stripped_lower not in found_toc_entries):
            original_name, target_level = known_lower[stripped_lower]
            fixed_lines.append(f"{'#' * target_level} {original_name}")
            promoted += 1
            promoted_entries.append(original_name)
            found_toc_entries.add(stripped_lower)
            continue

        fixed_lines.append(line)

    # Report missing TOC entries (not found anywhere)
    missing = []
    for key, (name, level) in known_lower.items():
        if key not in found_toc_entries:
            missing.append(name)

    fix_report = {
        "demoted": demoted,
        "promoted": promoted,
        "escaped_hash_numbers": escaped,
        "demoted_entries": demoted_entries[:20],
        "promoted_entries": promoted_entries[:20],
        "missing_toc_entries": missing,
        "total_toc_entries": len(all_known),
        "matched_toc_entries": len(found_toc_entries),
    }

    return "\n".join(fixed_lines), fix_report


def make_slug(text: str) -> str:
    """Create a filesystem-safe slug from text."""
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_]+", "_", slug.strip())
    return slug[:50]


def cmd_convert(args):
    """Phase 1: Convert PDF to merged markdown."""
    pdf_path = args.pdf_path
    output_dir = Path(args.output_dir)
    model = args.model
    mode = args.mode

    if not os.path.isfile(pdf_path):
        print(f"ERROR: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    api_key = get_api_key()
    page_count = get_page_count(pdf_path)
    book_name = Path(pdf_path).stem
    book_slug = make_slug(book_name)
    use_async = page_count > MAX_SYNC_PAGES if page_count > 0 else False

    # Cost estimate
    print(f"\n{'='*60}")
    print(f"  PDF: {pdf_path}")
    print(f"  Pages: {page_count if page_count > 0 else 'unknown'}")
    print(f"  Mode: {mode}")
    print(f"  Model: {model}")
    print(f"  API: {'async' if use_async else 'sync'}")
    print(f"  Output: {output_dir}")
    print(f"{'='*60}\n")

    if not args.confirm:
        print("Dry run complete. Add --confirm to execute the API call.")
        # Still write a minimal manifest for the estimate
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "pdf_path": str(pdf_path),
            "page_count": page_count,
            "api_mode": mode,
            "api_model": model,
            "sync_or_async": "async" if use_async else "sync",
            "status": "estimate_only",
        }
        (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
        return

    # Execute API call
    output_dir.mkdir(parents=True, exist_ok=True)

    if use_async:
        api_result = call_async_api(pdf_path, api_key, model, mode)
    else:
        api_result = call_sync_api(pdf_path, api_key, model, mode)

    elements = api_result.get("elements", [])
    cat_field = detect_category_field(elements)
    print(f"  Elements: {len(elements)} (field: '{cat_field}')")

    # Extract figures
    figure_map = extract_figures(elements, cat_field, output_dir, book_slug)
    print(f"  Figures extracted: {len(figure_map)}")

    # Build headings.json
    headings = build_headings_json(elements, cat_field)
    headings_path = output_dir / "headings.json"
    headings_path.write_text(json.dumps(headings, indent=2, ensure_ascii=False))
    print(f"  Headings: {len(headings)}")

    # Assemble merged markdown
    markdown = assemble_markdown(elements, cat_field, figure_map)

    # Apply TOC-based heading fix if provided
    heading_fix_report = None
    if args.toc:
        toc_path = Path(args.toc)
        if toc_path.exists():
            toc_data = json.loads(toc_path.read_text())
            print(f"\n  Applying TOC heading fix ({sum(len(v) for v in toc_data.values() if isinstance(v, dict))} entries)...")
            markdown, heading_fix_report = fix_headings_with_toc(markdown, toc_data)
            markdown = escape_hash_numbers(markdown)
            print(f"  Promoted: {heading_fix_report['promoted']}, Demoted: {heading_fix_report['demoted']}")
            if heading_fix_report["missing_toc_entries"]:
                print(f"  Missing: {heading_fix_report['missing_toc_entries']}")
        else:
            print(f"  WARNING: TOC file not found: {toc_path}", file=sys.stderr)
    else:
        # Still escape #N) even without TOC
        markdown = escape_hash_numbers(markdown)

    merged_path = output_dir / "merged.md"
    merged_path.write_text(markdown, encoding="utf-8")
    print(f"  Merged markdown: {len(markdown)} chars")

    # Verification
    verification = verify(elements, cat_field, markdown, figure_map, output_dir, page_count)
    print(f"\n  Verification: {'PASS' if verification['passed'] else 'FAIL'}")
    for w in verification.get("warnings", []):
        print(f"    WARNING: {w}")

    # Write manifest
    manifest = {
        "pdf_path": str(pdf_path),
        "book_name": book_name,
        "book_slug": book_slug,
        "page_count": page_count,
        "api_mode": mode,
        "api_model": model,
        "sync_or_async": "async" if use_async else "sync",
        "total_elements": len(elements),
        "category_field": cat_field,
        "status": "completed",
        "output_files": {
            "merged_md": str(merged_path),
            "headings_json": str(headings_path),
            "assets_dir": str(output_dir / "assets"),
        },
        "verification": verification,
    }
    if heading_fix_report:
        manifest["heading_fix"] = heading_fix_report
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    print(f"\n  Output written to: {output_dir}")
    print(f"  Manifest: {manifest_path}")

    # Print JSON manifest to stdout for Claude Code parsing
    print("\n---MANIFEST_JSON---")
    print(json.dumps(manifest, ensure_ascii=False))


def cmd_fix_headings(args):
    """Fix headings in existing output using TOC data."""
    output_dir = Path(args.fix_headings)
    merged_path = output_dir / "merged.md"
    manifest_path = output_dir / "manifest.json"

    if not merged_path.exists():
        print(f"ERROR: merged.md not found in {output_dir}", file=sys.stderr)
        sys.exit(1)

    toc_path = args.toc
    if not toc_path:
        print("ERROR: --toc is required with --fix-headings", file=sys.stderr)
        sys.exit(1)

    toc_data = json.loads(Path(toc_path).read_text())
    markdown = merged_path.read_text(encoding="utf-8")

    print(f"  Fixing headings using TOC: {toc_path}")
    print(f"  TOC entries: {sum(len(v) for v in toc_data.values() if isinstance(v, dict))}")

    fixed_md, fix_report = fix_headings_with_toc(markdown, toc_data)

    # Also escape #N) patterns
    fixed_md = escape_hash_numbers(fixed_md)

    merged_path.write_text(fixed_md, encoding="utf-8")
    print(f"  Promoted: {fix_report['promoted']}")
    print(f"  Demoted: {fix_report['demoted']}")
    print(f"  Escaped #N): {fix_report['escaped_hash_numbers']}")
    if fix_report["missing_toc_entries"]:
        print(f"  Missing TOC entries: {fix_report['missing_toc_entries']}")

    # Update manifest with fix report
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        manifest["heading_fix"] = fix_report
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    # Rebuild headings.json from fixed markdown
    headings = []
    for i, line in enumerate(fixed_md.split("\n")):
        m = re.match(r"^(#+)\s+(.+)$", line)
        if m:
            headings.append({
                "index": i,
                "level": len(m.group(1)),
                "text": m.group(2).strip(),
                "page": 0,
            })
    (output_dir / "headings.json").write_text(
        json.dumps(headings, indent=2, ensure_ascii=False)
    )
    print(f"  Updated headings.json: {len(headings)} headings")

    print("\n---FIX_REPORT_JSON---")
    print(json.dumps(fix_report, ensure_ascii=False))


def cmd_split(args):
    """Phase 2: Split merged markdown based on heading pattern."""
    source_dir = Path(args.split_from)
    output_dir = Path(args.output_dir)

    merged_path = source_dir / "merged.md"
    headings_path = source_dir / "headings.json"
    manifest_path = source_dir / "manifest.json"

    if not merged_path.exists():
        print(f"ERROR: merged.md not found in {source_dir}", file=sys.stderr)
        sys.exit(1)

    merged_md = merged_path.read_text(encoding="utf-8")
    headings = json.loads(headings_path.read_text()) if headings_path.exists() else []
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    parts = split_markdown(
        merged_md, headings,
        pattern=args.split_pattern,
        split_on_h1=args.split_on_h1,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    book_name = manifest.get("book_name", "document")

    split_files = []
    for i, part in enumerate(parts):
        title = part["title"]
        safe_title = re.sub(r"[/:*?\"<>|]", "", title)
        filename = f"{book_name} - {safe_title}.md"
        filepath = output_dir / filename
        filepath.write_text(part["content"], encoding="utf-8")
        split_files.append({"title": title, "filename": filename, "path": str(filepath)})
        print(f"  Created: {filename} ({len(part['content'])} chars)")

    # Copy assets if they exist
    source_assets = source_dir / "assets"
    if source_assets.exists():
        dest_assets = output_dir / "assets"
        dest_assets.mkdir(exist_ok=True)
        for png in source_assets.glob("*.png"):
            dest = dest_assets / png.name
            dest.write_bytes(png.read_bytes())

    # Write split manifest
    split_manifest = {
        "source_dir": str(source_dir),
        "book_name": book_name,
        "split_pattern": args.split_pattern,
        "split_on_h1": args.split_on_h1,
        "parts": split_files,
        "total_parts": len(split_files),
    }
    (output_dir / "split_manifest.json").write_text(
        json.dumps(split_manifest, indent=2, ensure_ascii=False)
    )

    print(f"\n  Split into {len(split_files)} files in {output_dir}")
    print("\n---SPLIT_MANIFEST_JSON---")
    print(json.dumps(split_manifest, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown using Upstage Document Parse API"
    )
    parser.add_argument("pdf_path", nargs="?", help="Path to PDF file")
    parser.add_argument("--output-dir", "-o", default="/tmp/pdf2md_output",
                        help="Output directory")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="API model name")
    parser.add_argument("--mode", default=DEFAULT_MODE,
                        choices=["auto", "standard", "enhanced"],
                        help="Parse mode (default: auto)")
    parser.add_argument("--confirm", action="store_true",
                        help="Execute API call (without this, only shows estimate)")

    # TOC-based heading fix
    parser.add_argument("--toc", help="Path to toc.json for heading hierarchy fix")
    parser.add_argument("--fix-headings",
                        help="Fix headings in existing output dir using --toc")

    # Split mode
    parser.add_argument("--split-from", help="Split from existing output directory")
    parser.add_argument("--split-pattern", help="Split on h1 headings matching this pattern")
    parser.add_argument("--split-on-h1", action="store_true",
                        help="Split on every h1 heading")

    args = parser.parse_args()

    if args.fix_headings:
        cmd_fix_headings(args)
    elif args.split_from:
        cmd_split(args)
    elif args.pdf_path:
        cmd_convert(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
