---
name: upstage-design
description: Use when designing slides, decks, presentations, marketing collateral, or any visual artifact that should match Upstage's corporate brand language. Provides the Solar Indigo design system — colors, typography, layout grid, components, and shape language extracted from the Upstage Company Intro deck. Triggers on "디자인", "design", "슬라이드", "slide", "deck", "발표자료", "브랜드", "brand", "PPT", "프레젠테이션", "presentation", "Upstage 색", "Solar Indigo".
---

# upstage-design

Upstage 코퍼레이트 디자인 시스템 레퍼런스. 슬라이드·발표자료·마케팅 자산·내부 도구 UI 등 Upstage 브랜드를 따르는 시각물을 만들 때 참조한다. 단일 voltage of **Solar Indigo (#5B52FF)** + 흰색/네이비 두 floor 캔버스 + lavender wash 보조 surface 가 핵심.

## When to use

- 슬라이드 / PPT / Keynote 덱 작성 또는 변환
- 마케팅 페이지·랜딩·보고서·배너 디자인
- 내부 도구 / 어드민 UI 의 색·타입·간격 토큰 결정
- "Upstage 다운" 비주얼이 필요한 모든 경우

## Hard rules

1. **단일 accent**: Solar Indigo `#5B52FF` 외 다른 브랜드 accent 추가 금지. 의미적 색(error/success 등)이 필요하면 채도를 indigo 보다 낮춰서 경쟁하지 않게.
2. **하드 코너 우선**: 전체 도형의 약 89% 사각형, 9% rounded(반경 ~12pt), 2% 원. soft corner 는 "discrete unit" 강조 시에만.
3. **그림자 사용 금지**: depth 는 surface(흰색·네이비·라벤더 wash) + 색 채도로만 표현.
4. **헤드라인 weight 700 고정**. 위계는 사이즈·색 대비로 만든다 (500/600 mid-weight 사용 금지).
5. **bilingual KO/EN** 폰트 스택 필수. fallback 에 `"맑은 고딕", "Malgun Gothic"` 또는 `Pretendard` 포함.
6. **lavender wash (#ECF0FF)** 가 흰 카드 + hairline 보더의 표준 대체. content card 에 1pt 회색 border 두지 말 것.

---

## Overview

Upstage is the canonical example of an enterprise-grade, document-AI presentation system — measured, technical, and built around a single voltage of indigo. The base canvas alternates between **pure white** (`{colors.canvas}` — #ffffff) for product and content slides and a **near-black navy** (`{colors.canvas-dark}` — #0D1320) for hero, section-break, and "before/after" framing slides. Headlines run in a deep ink-navy (`{colors.ink}` — #0D1320) on light surfaces and pure white (`{colors.on-dark}` — #ffffff) on dark surfaces. A single voltage of **Solar Indigo** (`{colors.primary}` — #5B52FF) carries every brand mark, every primary numeric stat, the vector wave graphic on the hero slide, the active step indicator on process diagrams, and the single accent rule that separates section bands.

Type runs **Arial** for headlines and **Calibri** for running body, with **Geist** appearing as a modern accent on numeric callouts and product wordmarks, and **Inter** as a tertiary fallback. There is no custom-licensed display face — the system trusts a workmanlike sans stack and lets color and layout do the differentiation. Headline weights sit at 700 across the board, but the actual size range is wide: hero numerics go up to ~37pt while content body holds at a tight 18pt, with table micro-text dropping to 7pt for dense pricing tables.

The shape language is **mostly hard**. Of every preset geometry in the deck, ~89% are pure rectangles, ~9% are rounded rectangles (used selectively for product cards, "Impact" callouts, and stepped pill labels), and ~2% are circles (icon plates, process-flow nodes). Hard corners on grid containers, soft corners only where the system is calling out a discrete unit of content. There are no hairline strokes around content cards on dark surfaces — separation comes from a lavender-wash fill (`{colors.surface-soft}` — #ECF0FF) instead.

**Key Characteristics:**

- Single accent color: `{colors.primary}` (#5B52FF — "Solar Indigo") carries the Upstage paper-plane wordmark, every primary stat number, the wave-cone hero graphic, active process steps, and the section-divider rule. Used scarcely on light slides — most content slides are 90% white + ink with one or two indigo moments — and as the dominant surface fill on accent slides.
- Workmanlike type stack: `Arial` for headlines, `Calibri` for body, with `Geist` and `Inter` as tertiary accents. No custom display face. Headline weights stay at 700; modesty in face is offset by aggressive size contrast (37pt hero vs 7pt micro).
- Two-floor canvas: a `{colors.canvas}` white floor for product and detail slides, and a `{colors.canvas-dark}` near-black navy floor (#0D1320) for hero / section-break / before-after framing slides. The deck reads as a "sandwich" — dark covers, white interior, dark transitions.
- Lavender-wash content bands: `{colors.surface-soft}` (#ECF0FF) is the signature secondary surface — every product feature card, comparison band, and AI Pack callout sits inside an indigo-tinted wash rather than a white card with a hairline border.
- Indigo fill stripes on tables: pricing and comparison tables alternate header rows in `{colors.primary}` (#5B52FF) and zebra-stripe content rows in `{colors.surface-soft}` (#ECF0FF). The result is far more saturated than typical enterprise SaaS.
- Cone / wave hero motif: the recurring section-break visual is a parametric ribbed cone in `{colors.primary}` over the dark canvas, suggesting "documents flowing into the model." It is the single recognizable brand graphic and replaces what would otherwise be a hero photograph.
- Three-tier weight ladder on stat callouts: a 37pt indigo number, a 22pt ink subhead, and a 9pt muted caption — repeated as the stat-callout pattern on the "Global AI Leader" slide.
- 4pt base spacing system, with major section padding at `{spacing.section}` (~64pt slide-edge margin) — denser than typical pitch decks because Upstage runs information-rich enterprise content (pricing, architecture, before/after grids) that demands cell density.

## Colors

### Brand & Accent

- **Solar Indigo** (`{colors.primary}` — #5B52FF): The single brand color. Used for the Upstage wordmark, primary stat numbers ("100+", "300만"), the cone/wave hero graphic, the active step in process flows, the section-divider rule, and the header-row fill on pricing tables. The most recognizable color in the deck.
- **Indigo Pressed** (`{colors.primary-pressed}` — #442AD8): The deeper saturation variant used on bullet markers, list discs, and selected-state indicators in the AI Pack pricing tables. Slightly more saturated than the primary.
- **Indigo Hover** (`{colors.primary-hover}` — #4F36F5): A mid-tone between primary and pressed, used for icon-fill on product feature plates inside the lavender bands.
- **Indigo Light** (`{colors.primary-light}` — #7578FF): A lighter parallel of the primary used on secondary nodes in process-flow diagrams and on de-emphasized stat callouts ("AI 정예팀" sub-stat).
- **Indigo Lift** (`{colors.primary-lift}` — #805CFB): A violet-leaning variant that appears only inside the cone/wave hero graphic as the inner ribs — never as a UI fill.

### Surface

- **Canvas** (`{colors.canvas}` — #ffffff): The default page floor for product, detail, comparison, and pricing slides. Roughly 60% of slide surface area.
- **Canvas Dark** (`{colors.canvas-dark}` — #0D1320): The near-black navy floor for hero, section-break, and before/after framing slides. Roughly 30% of slide surface area. Never pure black — the slight blue cast (#0D1320 vs #000000) keeps it warm enough to pair with the indigo accent without going cold.
- **Canvas Dark Lift** (`{colors.canvas-dark-lift}` — #0A0D14): A blacker variant of the dark canvas used as the recessed inner panel on the "BEFORE" half of comparison slides.
- **Canvas Dark Soft** (`{colors.canvas-dark-soft}` — #1E1F20): A slightly raised fill used on the dark hero slide as a behind-the-cone gradient anchor.
- **Surface Soft** (`{colors.surface-soft}` — #ECF0FF): The lavender wash. The single most distinctive surface in the system — used as the fill for every product feature band, AI Pack callout block, and comparison cell on white slides. Replaces what would be a white card with a hairline border in a typical enterprise deck.
- **Surface Soft Lift** (`{colors.surface-soft-lift}` — #F1F3FC): A paler variant of the lavender wash used on alternating zebra-stripe rows inside pricing tables.
- **Surface Periwinkle** (`{colors.surface-periwinkle}` — #DDE3FF): Mid-tone between Surface Soft and the primary lights — used inside table merge cells and on the "AI Workspace" platform layer band on the architecture slide.
- **Surface Neutral** (`{colors.surface-neutral}` — #F5F5F6): A non-tinted off-white used as a side-rail panel fill on the title slide and as a fallback fill where the lavender wash would compete with adjacent indigo content.
- **Surface Neutral Strong** (`{colors.surface-neutral-strong}` — #E9E8F0): A heavier neutral fill — used on the legal sub-band of the title slide and on muted disabled rows.

### Hairlines & Borders

- **Hairline** (`{colors.hairline}` — #D9D9D9): The default 1px border tone. Used sparingly — separator rules between table rows, the underline beneath the title-slide author block, and the thin divider between the BEFORE and AFTER columns on comparison slides.
- **Hairline Cool** (`{colors.hairline-cool}` — #CFCFD2): A slightly warmer variant used on dark-canvas surfaces where the default hairline would disappear into the navy.
- **Hairline Soft** (`{colors.hairline-soft}` — #D1D1DB): The lightest 1px tone, used for inner-table dividers between zebra rows where the lavender lift already provides most of the separation.

### Text

- **Ink** (`{colors.ink}` — #0D1320): The dominant text color on light surfaces. Display headlines, section titles, body paragraphs, and most inline body text. The same hex as `{colors.canvas-dark}` — Upstage uses one navy for both deep text and dark surface, deliberately collapsing the two roles.
- **Ink Strong** (`{colors.ink-strong}` — #000000): True black, used for hero headline runs that need the strongest possible weight (e.g., "Company Intro" title).
- **Body** (`{colors.body}` — #374151): A slate gray for running-text inside long-form product copy. Slightly cooler than ink, lighter weight, easier to read across multi-line paragraphs.
- **Body Soft** (`{colors.body-soft}` — #434C60): A second body tone used on captions and meta lines beneath stat callouts. Sits between Body and Muted.
- **Muted** (`{colors.muted}` — #4B5563): Sub-titles and muted helper copy on light surfaces. Tailwind-like slate-600.
- **Muted Soft** (`{colors.muted-soft}` — #84848C): Disabled or de-emphasized supporting text — caption-row fine print on the title slide ("Enterprise Business Service") and the small italic hardware/VAT disclaimer beneath pricing tables.
- **Muted Cool** (`{colors.muted-cool}` — #979CAE): The faintest text tone, used for in-graphic labels inside the Upstage AI Pack architecture diagram (where labels need to recede behind shaded blocks).
- **On Dark** (`{colors.on-dark}` — #ffffff): White text on the dark canvas (hero headlines, section-break titles).
- **On Primary** (`{colors.on-primary}` — #ffffff): White text on Solar Indigo fills (pricing-table header rows, active step indicators).

### Semantic & Accent

- **Mint** (`{colors.mint}` — #AFD89D): A muted sage-green used only on the architecture slide to highlight "Operating System" and "Device Hardware" partner-supplied layers — distinguishing them from Upstage's own indigo-tinted layers.
- **Mint Light** (`{colors.mint-light}` — #D2FF95): A brighter parallel of Mint, used on the same architecture diagram as the layer-edge highlight.
- **Lavender Mid** (`{colors.lavender-mid}` — #949CE5): A muted lavender used on outer rings of the cone/wave hero graphic — it never appears as a UI fill, only inside the recurring brand graphic.
- **Lavender Soft** (`{colors.lavender-soft}` — #6C6ED6): A periwinkle mid-tone between the primary and the muted-cool — used on secondary process-flow nodes.
- **Lavender Edge** (`{colors.lavender-edge}` — #A1B6FF): A pale edge tone for outer-ring strokes inside the hero graphic.

There are no error-red, success-green, or warning-yellow tokens in the deck — this is intentional. Upstage is a pitch deck, not an application, and semantic states only enter through the customer-screenshot mockups embedded inside product slides.

### Scrim

There is no global modal scrim — the deck is static — but the dark hero slides apply a subtle vertical gradient from `{colors.canvas-dark}` (#0D1320) at the top to `{colors.canvas-dark-lift}` (#0A0D14) at the bottom to seat the cone graphic.

## Typography

### Font Family

The system runs **Arial** for display headlines and **Calibri** for running body and table text. **Geist** appears as a modern accent on a small number of product wordmarks ("Document Parse", "Solar Pro") and large numeric callouts. **Inter** appears as a tertiary accent inside the architecture-diagram labels and the AI Pack feature card body. Fallbacks walk `Helvetica, system-ui, -apple-system, "맑은 고딕", "Malgun Gothic", sans-serif` — Korean glyph coverage is essential because the deck is bilingual KO/EN.

There is no separate display family — the variable mass comes from size and weight contrast, not from typeface change.

### Hierarchy

| Token | Size | Weight | Use |
|---|---|---|---|
| `{typography.display-xl}` | 37pt | 700 | Hero numerics on stat-callout slides ("Global AI Leader" headline split) |
| `{typography.display-lg}` | 31.5pt | 700 | Title-slide H1 ("Company Intro") |
| `{typography.display-md}` | 22.8pt | 700 | Section-break headlines ("문서를 이해하는 AI") and major slide titles |
| `{typography.display-sm}` | 21.4pt | 700 | Sub-section heads inside content slides ("왜 AI 도입이 어려울까요?") |
| `{typography.title-lg}` | 17.1pt | 700 | AI Pack product card titles ("AI Pack for RAG") |
| `{typography.title-md}` | 14.25pt | 700 | Sub-section titles inside lavender content bands ("지식 컬렉션", "Agent 생성") |
| `{typography.stat-display}` | ~10.7pt | 700 | Stat-callout numeric overlays inside the "100+" / "300만" tile system |
| `{typography.body-lg}` | 18pt | 400 | The default running-text inside product feature copy |
| `{typography.body-md}` | 9.5pt | 400 | Compact body copy inside dense lavender feature cards |
| `{typography.body-sm}` | 9.05pt | 400 | Table cells, caption rows, and secondary stat sub-labels |
| `{typography.body-xs}` | 8.55pt | 400 | Tertiary captions on the architecture diagram and "BEFORE/AFTER" comparison meta lines |
| `{typography.caption}` | 7.13pt | 700 | Pricing-table header labels and micro-tags inside dense table layouts |
| `{typography.micro}` | 6.17pt | 400 | The smallest legal disclaimer ("*워크스테이션에 한함, 연간 구독 가격 기준") |
| `{typography.button}` | 12pt | 700 | Title-slide author name ("전 수 민") and inline button-style labels |

### Principles

Headline weight stays uniform at 700 across the entire ladder — Upstage does not use a 500/600 mid-weight. The hierarchy comes entirely from size contrast and color contrast (indigo numbers vs ink labels) rather than from weight modulation.

The single typographically loud moment in the deck is the **"Global AI Leader"** stat-callout block on slide 4, where a 37pt indigo numeric pairs with a 22pt ink subhead and a 9pt muted caption — a 4× size ratio across three lines. This pattern is the deck's signature stat-display style.

Body copy holds at a tight 9–10pt across product feature cards, which is small for a deck meant to be projected — Upstage compensates with high contrast (deep ink on lavender wash) and short paragraph length (3–4 lines max per feature card).

### Note on Font Substitutes

If Arial and Calibri are unavailable, **Inter** is the closest open-source substitute for both — it carries Latin and CJK fallbacks gracefully. Calibri's slightly tighter cap height means body text in Inter should be set ~5% smaller to match perceived weight. **Pretendard** is the recommended substitute when Korean glyph coverage and Inter-like proportions are both required.

## Layout

### Spacing System

- **Base unit:** 4pt (with 8pt snap on most major increments).
- **Tokens:** `{spacing.xxs}` 2pt · `{spacing.xs}` 4pt · `{spacing.sm}` 8pt · `{spacing.md}` 12pt · `{spacing.base}` 16pt · `{spacing.lg}` 24pt · `{spacing.xl}` 32pt · `{spacing.xxl}` 48pt · `{spacing.section}` 64pt.
- **Slide-edge padding:** `{spacing.section}` (64pt) on left and right edges of the 16:9 slide; `{spacing.xxl}` (48pt) top and bottom — denser than a typical 80pt pitch-deck margin because Upstage runs information-heavy slides.
- **Card internal padding:** `{spacing.lg}` (24pt) inside the lavender feature bands; `{spacing.base}` (16pt) inside dense table cells; `{spacing.sm}` (8pt) inside stat-callout meta rows.
- **Gutters:** `{spacing.base}` (16pt) between feature cards in a 3- or 4-up grid; `{spacing.lg}` (24pt) between major content bands; `{spacing.xs}` (4pt) on dense table column dividers.

### Grid & Container

- **Slide aspect:** 16:9 (12.5" × 7" or 1280×720pt at standard render). All layouts are anchored to this aspect.
- **Two-column compare:** The dominant content layout — used on "BEFORE/AFTER," "Problem/Solution," and "Standard/Workstation pricing" slides. Columns split 50/50 with a 24pt central gutter, and the BEFORE/dark side typically uses `{colors.canvas-dark-lift}` while the AFTER/light side uses `{colors.canvas}`.
- **3-up product grid:** Used on "Why Upstage Differs" (slide 9) and "AI 도입의 어려움" (slide 7) — three lavender feature bands stacked horizontally, each holding an icon plate, a 14pt title, and a 9pt body excerpt.
- **4-up stat tile:** Used on "Global AI Leader" (slide 4) — a 2×2 stat grid where each cell holds a 37pt indigo number, a 22pt ink label, and a 9pt muted caption.
- **Architecture diagram:** Used on the AI Pack platform slide (slide 11) — a 4-row horizontal stack (Applications / AI Models / AI Platform / Operating System / Device Hardware) where each row is a full-width lavender band with embedded blocks. Always read top-to-bottom as a stack.
- **Pricing table:** 4-column layout (Product / Contract Term / Standard Price / Variant Price), with a Solar Indigo header row, lavender-wash zebra-stripe rows, and 7pt caption-style body text.

### Whitespace Philosophy

The deck deliberately runs denser than typical pitch decks — most content slides carry 6–10 distinct content elements rather than the 3–4 of a Sequoia-style template. The lavender wash absorbs visual noise that would otherwise come from card borders, so the page can hold more cells without feeling cramped. The contrast is between the dark hero slides (which run extremely sparse — just a headline and the cone graphic) and the light content slides (which run extremely dense), reinforcing the rhythm of "set up the question, then drown the audience in the answer."

## Elevation

The system has **essentially no shadows**. Depth is conveyed exclusively through:

- **Surface separation** — lavender wash (`{colors.surface-soft}` — #ECF0FF) lifting feature cards off the white canvas, and the dark canvas (`{colors.canvas-dark}` — #0D1320) recessing hero panels.
- **Color saturation** — Solar Indigo header rows on tables seat them visually above the zebra-stripe content rows.
- **Stroke-only borders** — where a content cell needs a stronger boundary (rare, mostly on the architecture slide), a 1pt `{colors.primary}` stroke encloses it instead of a shadow.

There is no `box-shadow` equivalent in the deck. Upstage's shape language relies on flat fills exclusively — a deliberate choice that reads as "technical precision" rather than the soft-elevation feel of a consumer marketplace.

## Components

### Title & Hero

**`title-slide`** — White canvas with a thin gray-blue rendered-cloud illustration on the left third (the only image-style element in the deck), the Upstage wordmark top-left at ~14pt, an "Company Intro" H1 at 31.5pt / 700 in `{colors.canvas-dark}`, and a 12pt author name + 9pt role caption beneath a 1pt `{colors.hairline}` underline rule. The rule is a recurring detail — Upstage uses thin author-block underlines as the title-slide signature.

**`hero-dark`** — Dark canvas (`{colors.canvas-dark}`) with the Upstage wordmark top-left in white, a 22.8pt / 700 white H1 set in two ragged-right lines on the left, and the cone/wave parametric graphic on the right anchored to the bottom-right. Used as the second slide and as section dividers throughout. The single most recognizable composition in the deck.

**`section-break`** — A thinner variant of `hero-dark` used between major content sections (e.g., "어려웠던 업무 자동화, 업스테이지로 쉬워집니다."). Same dark canvas, same wordmark anchor, but no cone graphic — instead a single Solar Indigo accent rule beneath the H1.

### Stat Callouts

**`stat-tile-display`** — The signature "Global AI Leader" pattern. A vertical stack of: a 37pt / 700 numeric in `{colors.primary}`, a 22pt / 700 ink label, and a 9pt / 400 `{colors.body-soft}` caption. Cells sit on the white canvas with no border or fill — separated only by a 24pt vertical gutter. The largest typographic moment in the deck.

**`stat-tile-inline`** — A compressed variant used inside lavender feature bands. 14pt / 700 indigo number, 9pt / 400 ink label on the same line. No caption row.

### Content Bands & Cards

**`feature-band-lavender`** — The signature content surface. A `{colors.surface-soft}` (#ECF0FF) full-width band with `{rounded.md}` corner clipping (~12pt radius), 24pt internal padding, holding a small icon plate top-left, a 14.25pt / 700 title, and a 9pt / 400 body paragraph. Used as the unit cell on every product-feature slide.

**`feature-card-product`** — A taller variant of `feature-band-lavender` used on slides 5 and 6 (Model Layer / Application Layer). Same lavender fill, same rounded corners, but with a screenshot or product wordmark embedded in the upper third and the description below.

**`compare-cell-before`** — A dark-canvas cell (`{colors.canvas-dark-lift}` — #0A0D14) with white text and an "BEFORE" tag at the top in 9pt muted-cool. Holds the problem statement in 18pt / 400 white text. Always paired with `compare-cell-after`.

**`compare-cell-after`** — A lavender-wash cell (`{colors.surface-soft}`) with ink text and an "Upstage 도입" tag at the top in 9pt indigo. Holds the resolved-state copy in 18pt / 400 ink text.

**`impact-callout`** — A small `{rounded.sm}` rounded-pill block with `{colors.primary}` (or `{colors.primary-pressed}`) fill, white "Impact" label in 7pt / 700 caps, anchored to the bottom-left of AI Pack product slides. The single most-repeated micro-component.

### Process & Flow

**`process-step-active`** — A circular `{colors.primary}` filled node with white inner number, sitting on a dotted indigo connector line. Used on slides 8 and 10 to represent the active step in the AI workflow.

**`process-step-inactive`** — Same circular geometry but with a `{colors.surface-periwinkle}` fill and ink number. Becomes active on the next slide via state change in the deck animation.

**`flow-connector`** — A thin 1pt indigo dotted rule connecting process steps. Always horizontal, always dotted, always Solar Indigo.

### Tables

**`pricing-table`** — The signature pricing layout used on slide 15. A 4-column table with a `{colors.primary}` header row carrying 7pt / 700 white caps labels, alternating row fills of `{colors.surface-soft}` and `{colors.surface-soft-lift}`, and 1pt `{colors.hairline-soft}` between cells. Body text holds at 7pt to fit the 4-column width without wrapping.

**`comparison-table`** — Used on slide 9 ("Upstage는 다릅니다"). A 2-column table with no header row, lavender-wash left column and white right column, separated by a 24pt central gutter and a single 1pt indigo accent rule. Holds Upstage feature claims paired with competitor or market-baseline rebuttals.

### Architecture Diagram

**`architecture-stack`** — Slide 11's signature platform diagram. A 5-row horizontal stack (Applications / AI Models / AI Platform / Operating System / Device Hardware), where each row is a full-width band tinted progressively cooler — Upstage-provided layers (top three) tint indigo via the lavender wash, partner-provided layers (bottom two) tint mint (`{colors.mint}` — #AFD89D) and neutral. Each band holds inline product wordmarks and partner logos as vector marks.

### Typography Components

**`section-rule`** — A 2pt `{colors.primary}` horizontal rule beneath section-break H1 titles. Always 100% the width of the H1 column, never the full slide width.

**`author-underline`** — A 1pt `{colors.hairline}` rule on the title slide separating the H1 from the author block. The single most subtle typographic detail in the deck.

**`badge-impact`** — A small `{rounded.sm}` rounded pill with `{colors.primary}` or `{colors.primary-pressed}` fill, holding "Impact" in 7pt / 700 white caps. Sits at the bottom-left of every AI Pack product slide.

### Iconography

Icons are flat 2pt-stroke line marks in `{colors.primary}` or `{colors.ink}` depending on background. There is no filled icon variant. Icon plates are square, never circular (matching the system's preference for hard corners), and sit at 24×24 or 32×32pt. Brand and partner logos appear as native vector marks at their native ratios — never reskinned to match the indigo palette.

## Responsive Behavior

This is a slide deck system, not a web layout, so "responsive behavior" is about render-fidelity across PowerPoint, Keynote, and PDF rather than viewport breakpoints.

| Render Target | Notes |
|---|---|
| PowerPoint / Native | The reference render. All custom illustrations (cone graphic, AI Pack architecture) are stored as PNGs at 2× the slide-render resolution to survive zoom and reflow. |
| Keynote Import | Calibri may substitute to Helvetica Neue — adjust body line-height up by ~3% to compensate for tighter Helvetica metrics. The Solar Indigo (#5B52FF) renders identically. |
| PDF Export | All lavender wash bands flatten cleanly; the cone graphic's outer rings (`{colors.lavender-soft}` and `{colors.lavender-edge}`) may posterize slightly if exported below 150 DPI — recommend 200 DPI for print-quality export. |
| 4:3 Re-aspect | Not supported. The deck is locked to 16:9 and the cone graphic and architecture stack will crop badly if forced to 4:3. Re-author rather than re-aspect. |
| Small Screen / Mobile View | Body text at 9pt becomes unreadable below tablet size. Recommend a separate "compact" variant of the content slides where body lifts to 12pt and feature bands stack 1-up rather than 3-up. |

### Density

- Stat callouts at 37pt / 700 are designed to read from the back of a 30-person conference room.
- Body text at 9pt / 400 is readable on a 1080p projector at 6m viewing distance — borderline on a laptop monitor at desk distance.
- Pricing-table micro at 7pt / 700 should be reflowed to a separate "supplement" slide when the deck is repurposed for in-person handout.

### Collapsing Strategy

- Two-column compare layouts collapse to single-column stack with the BEFORE block above the AFTER block.
- 4-up stat tiles collapse to 2×2 grid (already the default) and then to 1-up vertical stack at the smallest size.
- The 5-row architecture stack does not collapse — it is rebuilt as a vertical sequence of full-width slides if the original layout cannot hold.

## Known Gaps

- **Hover and interactive states:** A static deck has no hover or focus states; if these tokens are extended into a web product, the indigo pressed (`{colors.primary-pressed}` — #442AD8) is the natural hover/active variant and should carry over.
- **Error / success / warning tokens:** Not present in the deck. A semantic palette would need to be authored separately — recommend keeping any new red/green/amber tokens at lower saturation than the Solar Indigo so they do not compete with the brand.
- **Dark-mode lavender wash:** The lavender feature band (`{colors.surface-soft}` — #ECF0FF) does not have a paired dark-canvas variant in the captured slides. On the few dark-canvas content slides (slide 8), feature cells revert to the indigo primary fill instead — but a true dark-mode lavender (something around #1E1650 or #252343, both of which appear once each in the cone graphic gradient) would be a natural extension.
- **Loading / skeleton states:** Not applicable to a static deck.
- **Form components:** Buttons, inputs, dropdowns, and checkboxes are not present in the deck — they appear only inside embedded customer-screenshot mockups at low fidelity. Building a full UI kit on top of this design language would require authoring those primitives from scratch.
- **Motion / transition tokens:** PowerPoint slide transitions in the source file are default fades — there is no documented motion language. If extended into a web product, recommend a 200ms ease-out as the baseline timing to match the deck's overall measured pace.
- **Iconography library:** The deck draws icons from multiple sources (custom 2pt-stroke marks for product features, native partner logos for the architecture diagram, and Unicode glyphs like 漢 / あ / A for the multilingual product callout). A unified icon library is not captured here and would need to be authored.