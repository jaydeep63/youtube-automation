import os, json, hashlib, pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Load environment variables from .env file
load_dotenv()

# Load config
with open("config.json") as f:
    config = json.load(f)

SCAN_FOLDER = config["scan_folder"]
PRIVACY = config["privacyStatus"]
META = config["youtube_metadata"]
CATEGORIES = config.get("categories", {})

LOG_FILE = "uploaded_log.json"

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            return json.load(f)
    return {}

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def checksum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def get_resolution(path):
    clip = VideoFileClip(path)
    return clip.size  # (width, height)

def detect_category(filename):
    fname_lower = filename.lower()
    for key, details in CATEGORIES.items():
        if key in fname_lower:
            return details["title_suffix"], details["tags"]
    return "General Gameplay", ["Valorant", "Gaming", "FPS"]

def get_metadata(filename, resolution):
    if resolution == (1920, 1080):
        template = META["long_form"]
    elif resolution == (1080, 1920):
        template = META["shorts"]
    else:
        template = META["long_form"]

    category_suffix, category_tags = detect_category(filename)
    title = template["title_template"].replace("{filename}", filename).replace("{category}", category_suffix)
    description = template["description_template"].replace("{category}", category_suffix)
    tags = list(set(template["tags"] + category_tags))
    return title, description, tags

def youtube_auth():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None
    
    # Create client_secret.json from environment variables if it doesn't exist
    if not os.path.exists("client_secret.json"):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        project_id = os.getenv("GOOGLE_PROJECT_ID")
        
        if not all([client_id, client_secret, project_id]):
            raise ValueError(
                "Missing credentials. Please set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, "
                "and GOOGLE_PROJECT_ID in your .env file or environment variables."
            )
        
        # Create client_secret.json from environment variables
        client_secret_data = {
            "installed": {
                "client_id": client_id,
                "project_id": project_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"]
            }
        }
        
        with open("client_secret.json", "w") as f:
            json.dump(client_secret_data, f)
        print("✓ Generated client_secret.json from environment variables")
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(youtube, path, title, description, tags):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags
            },
            "status": {"privacyStatus": PRIVACY}
        },
        media_body=MediaFileUpload(path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"Uploaded {path} → Video ID: {response['id']}")
    return response["id"]

# Placeholders for FB/IG
def upload_to_facebook(path, metadata):
    print("TODO: Implement Facebook upload")

def upload_to_instagram(path, metadata):
    print("TODO: Implement Instagram upload")

def main():
    youtube = youtube_auth()
    log = load_log()

    for file in os.listdir(SCAN_FOLDER):
        if not file.endswith(".mp4"):
            continue
        path = os.path.join(SCAN_FOLDER, file)
        cs = checksum(path)
        if cs in log:
            continue
        resolution = get_resolution(path)
        title, description, tags = get_metadata(file, resolution)
        print(f"Detected file: {file}")
        print(f"Resolution: {resolution}")
        print(f"Category: {title}")
        vid_id = upload_to_youtube(youtube, path, title, description, tags)
        log[cs] = {"filename": file, "video_id": vid_id}
        save_log(log)

if __name__ == "__main__":
    main()
