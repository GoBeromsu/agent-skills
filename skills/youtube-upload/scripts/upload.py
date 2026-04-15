# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client>=2.0", "google-auth>=2.0", "google-auth-oauthlib>=1.0"]
# ///
"""
Upload a video to YouTube via Data API v3 with OAuth 2.0.

Usage:
    python upload.py INPUT.mp4 --title "..." --description "..." --tags "tag1,tag2"
    python upload.py INPUT.mp4 --title "..." --thumbnail /tmp/thumb.jpg
    python upload.py --auth-only   # Initial OAuth setup (no upload)

Outputs JSON to stdout on success:
    {"video_id": "...", "youtube_url": "..."}

Credential paths (configurable via env vars):
    YT_CREDENTIALS_PATH  ~/.config/youtube-upload/credentials.json
    YT_TOKEN_PATH         ~/.config/youtube-upload/token.json

First-time setup:
    1. Enable YouTube Data API v3 in Google Cloud Console
    2. Create OAuth client ID (Desktop app) and download JSON
    3. Save as ~/.config/youtube-upload/credentials.json
    4. Run: python upload.py --auth-only
    5. Complete consent in browser

NOTE: Unverified API projects (created after 2020-07-28) restrict uploads to
private visibility. Default privacy is 'private' for safety.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Allow HTTP redirect for localhost OAuth callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

DEFAULT_CREDENTIALS = Path("~/.config/youtube-upload/credentials.json").expanduser()
DEFAULT_TOKEN = Path("~/.config/youtube-upload/token.json").expanduser()


def get_credentials(credentials_path: Path, token_path: Path):
    """Load or create OAuth 2.0 credentials for YouTube upload."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            token_path.write_text(creds.to_json())
            return creds
        except Exception as e:
            print(f"Token refresh failed: {e}. Re-authenticating...", file=sys.stderr)

    # New auth flow
    if not credentials_path.exists():
        print(
            f"ERROR: OAuth credentials not found at {credentials_path}\n"
            "Download from Google Cloud Console -> APIs & Services -> Credentials\n"
            "Save as: ~/.config/youtube-upload/credentials.json",
            file=sys.stderr,
        )
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
    creds = flow.run_local_server(port=0)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json())
    print(f"Token saved to {token_path}", file=sys.stderr)

    return creds


def upload_video(youtube, video_path: str, title: str, description: str,
                 tags: list, privacy: str, category_id: str = "22",
                 language: str = None):
    """Upload video with resumable upload. Returns video_id."""
    from googleapiclient.http import MediaFileUpload

    snippet = {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": category_id,
    }

    if language:
        snippet["defaultLanguage"] = language
        snippet["defaultAudioLanguage"] = language

    body = {
        "snippet": snippet,
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=5 * 1024 * 1024,  # 5MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload progress: {pct}%", file=sys.stderr, flush=True)

    return response["id"]


def set_thumbnail(youtube, video_id: str, thumbnail_path: str):
    """Set custom thumbnail for an uploaded video."""
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
    print(f"Thumbnail set for {video_id}", file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument("input", nargs="?", help="Video file path (mp4)")
    parser.add_argument("--title", required=False, help="Video title")
    parser.add_argument("--description", required=False, default="", help="Video description")
    parser.add_argument("--tags", required=False, default="", help="Comma-separated tags")
    parser.add_argument("--privacy", default="public",
                        choices=["private", "unlisted", "public"],
                        help="Privacy status (default: private)")
    parser.add_argument("--category-id", default="22",
                        help="YouTube category ID (default: 22 = People & Blogs)")
    parser.add_argument("--thumbnail", default=None,
                        help="Path to custom thumbnail JPEG (1280x720)")
    parser.add_argument("--language", default=None,
                        help="Spoken language code (e.g., 'en', 'ko'). Sets both "
                             "defaultLanguage and defaultAudioLanguage.")
    parser.add_argument("--localizations", default=None,
                        help='JSON string of localizations, e.g., '
                             '\'{"ko": {"title": "...", "description": "..."}}\'')
    parser.add_argument("--update", default=None, metavar="VIDEO_ID",
                        help="Update an existing video (no upload). Use with "
                             "--localizations and/or --language.")
    parser.add_argument("--auth-only", action="store_true",
                        help="Run OAuth flow only, no upload")
    args = parser.parse_args()

    credentials_path = Path(
        os.environ.get("YT_CREDENTIALS_PATH", str(DEFAULT_CREDENTIALS))
    ).expanduser()
    token_path = Path(
        os.environ.get("YT_TOKEN_PATH", str(DEFAULT_TOKEN))
    ).expanduser()

    creds = get_credentials(credentials_path, token_path)

    if args.auth_only:
        print("OAuth setup complete. Token saved.", file=sys.stderr)
        print(json.dumps({"status": "auth_complete", "token_path": str(token_path)}))
        return

    from googleapiclient.discovery import build

    youtube = build("youtube", "v3", credentials=creds)

    # Update mode: modify existing video (localizations, language, thumbnail)
    if args.update:
        video_id = args.update
        updates = {}

        if args.language or args.localizations:
            resp = youtube.videos().list(part="snippet,localizations", id=video_id).execute()
            if not resp.get("items"):
                print(f"ERROR: Video not found: {video_id}", file=sys.stderr)
                sys.exit(1)

            item = resp["items"][0]

            if args.language:
                snippet = item["snippet"]
                snippet["defaultLanguage"] = args.language
                snippet["defaultAudioLanguage"] = args.language
                youtube.videos().update(
                    part="snippet",
                    body={"id": video_id, "snippet": snippet}
                ).execute()
                print(f"Language set: {args.language}", file=sys.stderr, flush=True)

            if args.localizations:
                localizations = json.loads(args.localizations)
                existing = item.get("localizations", {})
                existing.update(localizations)
                youtube.videos().update(
                    part="localizations",
                    body={"id": video_id, "localizations": existing}
                ).execute()
                print(f"Localizations set: {list(localizations.keys())}", file=sys.stderr, flush=True)

        if args.thumbnail:
            set_thumbnail(youtube, video_id, args.thumbnail)

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        output = {"status": "updated", "video_id": video_id, "youtube_url": youtube_url}
        print(json.dumps(output, ensure_ascii=False))
        return

    # Upload mode
    if not args.input:
        print("ERROR: Video file path required (or use --auth-only / --update)", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not args.title:
        print("ERROR: --title is required for upload", file=sys.stderr)
        sys.exit(1)

    if args.thumbnail and not os.path.exists(args.thumbnail):
        print(f"ERROR: Thumbnail not found: {args.thumbnail}", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading: {os.path.basename(args.input)}", file=sys.stderr, flush=True)

    tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]

    video_id = upload_video(
        youtube,
        args.input,
        args.title,
        args.description,
        tags_list,
        args.privacy,
        args.category_id,
        language=args.language,
    )

    if args.thumbnail:
        set_thumbnail(youtube, video_id, args.thumbnail)

    # Apply localizations if provided
    if args.localizations:
        localizations = json.loads(args.localizations)
        youtube.videos().update(
            part="localizations",
            body={"id": video_id, "localizations": localizations}
        ).execute()
        print(f"Localizations set: {list(localizations.keys())}", file=sys.stderr, flush=True)

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Upload complete: {youtube_url}", file=sys.stderr, flush=True)

    output = {"video_id": video_id, "youtube_url": youtube_url}
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
