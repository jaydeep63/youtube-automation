# youtube-automation
Automation to upload videos to your socials from a folder in your local drive

# YouTube Automation Script

## Features
- Scans a configured folder (set once during setup) for new `.mp4` files.
- Detects resolution:  
  - 1920x1080 → Long-form video  
  - 1080x1920 → Shorts  
- **Auto-detects content type from video filename** (Gaming, Unboxing, Review, Mukbang, Vlog, Tutorial, etc.)
- Applies customizable metadata templates based on video category
- Uploads via YouTube Data API v3.
- Prevents duplicates using `uploaded_log.json`.
- Supports AI-powered title/description generation (via Ollama)
- Works with ANY video type and content

## Setup
1. Clone the repo.
2. Add your Google API `client_secret.json` to the repo root.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

---

## Register Your App in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `youtube-automation`).
3. Enable **YouTube Data API v3**:
   - Navigate to **APIs & Services → Library**.
   - Search for “YouTube Data API v3”.
   - Click **Enable**.
4. Create OAuth2 credentials:
   - Go to **APIs & Services → Credentials**.
   - Click **Create Credentials → OAuth client ID**.
   - Select **Desktop Application**.
   - Name it (e.g., `YouTubeUploader`).
   - Click **Create**.
5. Download the JSON file and save it as `client_secret.json` in your repo root.
6. On first run, the script will open a browser window for login. After granting permission, a `token.pickle` file will be created for future runs.

---

## Step‑by‑Step Example: Editing config.json for Multiple Categories

1. The `categories` section in `config.json` lets you define custom categories that match filename patterns.
2. Example: Add a category for "doom" gameplay:
   ```json
   "doom": {
     "title_suffix": "Doom Highlights",
     "primary_keyword": "Doom Gameplay",
     "tags": ["Doom", "Gaming", "FPS"]
   }
   ```
3. If your filename contains "doom" (e.g., `doom_gameplay.mp4`), this category will be used.
4. The app generates metadata dynamically based on the detected content type and category.
5. Example: `clutch_moment_gaming.mp4` → Uses the "clutch" category + "Gaming" content type detection.

## How It Works: Content Type Detection

The app detects the content type **from your video filename**, not the folder:

**Supported Content Types:**
- `gameplay`, `game`, `valorant`, `fortnite`, etc. → **Gaming**
- `unboxing`, `opening`, `reveal` → **Unboxing**
- `review`, `tested`, `honest` → **Product Review**
- `mukbang`, `eating`, `asmr` → **Mukbang**
- `vlog`, `daily`, `routine` → **Vlog**
- `tutorial`, `how to`, `guide`, `tips` → **Tutorial**
- `short`, `clip`, `moment` → **Short Video**

**Examples:**
- `my_gaming_session.mp4` → Detected as **Gaming**
- `iphone_unboxing_2024.mp4` → Detected as **Unboxing**
- `product_review_honest.mp4` → Detected as **Product Review**
- `mukbang_asmr.mp4` → Detected as **Mukbang**

## Configuration: Video Folder (Set Once)

Edit `config.json` and set `scan_folder` during first setup:
```json
{
  "scan_folder": "H:\\Videos\\MyContent",
  ...
}
```
The folder location is saved and won't change. Just drop videos into it and the app handles the rest!



