# youtube-automation
Automation to upload videos to your socials from a folder in your local drive

# YouTube Automation Script

## Features
- Scans `H:\VALORANT\VALORANT` for new `.mp4` files.
- Detects resolution:  
  - 1920x1080 → Long-form video  
  - 1080x1920 → Shorts  
- Applies Valorant-themed metadata templates.
- Uploads via YouTube Data API v3.
- Prevents duplicates using `uploaded_log.json`.
- Placeholders for Facebook/Instagram integration.

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

1. Locate the `categories` section in `config.json`.
2. Add or edit categories. For example:
   ```json
   "ace": {
     "title_suffix": "Epic Ace Highlight",
     "tags": ["Valorant", "Ace", "Gaming", "FPS", "HighFrags"]
   }
3. Modify metadata templates to include {category}:
 "title_template": "Valorant Gameplay - {category} - {filename}"
4. Adjust descriptions to dynamically reflect the category:
 "description_template": "Full Valorant match highlights featuring {category}!"
5. Save and run the script. Example: match1_clutch.mp4 → Title becomes
Valorant Gameplay - Insane Clutch Kill - match1_clutch.mp4.



