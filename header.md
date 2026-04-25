# Code Section Explanations

## Config Loader
- Reads `config.json` for folder path, privacy settings, and metadata templates.
- Change `"scan_folder"` to point to a different directory.
- Adjust `"privacyStatus"` to `public`, `unlisted`, or `private`.

## OAuth2 Setup
- Uses `client_secret.json` from Google Cloud Console for authentication.
- Generates `token.pickle` after first login to avoid repeated sign-ins.
- Replace `client_secret.json` with your own credentials file.

## Resolution Detector
- Uses `moviepy` to detect video resolution.
- 1920x1080 → Long-form video metadata.
- 1080x1920 → Shorts metadata.
- Defaults to long-form if resolution doesn’t match.

## Metadata Templates
- Defined in `config.json` under `youtube_metadata`.
- Separate templates for long-form and shorts.
- Customize titles, descriptions, and tags to match your content style.

## Upload Log
- `uploaded_log.json` stores checksums of uploaded files.
- Prevents duplicate uploads by skipping files already logged.

## YouTube Upload
- Handles actual upload via YouTube Data API v3.
- Applies metadata and privacy settings.
- Prints video ID after successful upload.

## Facebook/Instagram Placeholders
- Functions `upload_to_facebook()` and `upload_to_instagram()` are stubbed.
- Currently log “TODO: Implement”.
- Ready for future integration without restructuring.
