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
    
    # Read client_secret.json and interpolate environment variables
    with open("client_secret.json", "r") as f:
        client_secret_content = f.read()
    
    # Replace environment variable placeholders
    client_secret_content = client_secret_content.replace("${GOOGLE_CLIENT_ID}", os.getenv("GOOGLE_CLIENT_ID", ""))
    client_secret_content = client_secret_content.replace("${GOOGLE_CLIENT_SECRET}", os.getenv("GOOGLE_CLIENT_SECRET", ""))
    client_secret_content = client_secret_content.replace("${GOOGLE_PROJECT_ID}", os.getenv("GOOGLE_PROJECT_ID", ""))
    
    # Validate that all env vars were replaced
    if "${" in client_secret_content:
        raise ValueError(
            "Missing environment variables. Please ensure GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, "
            "and GOOGLE_PROJECT_ID are set in your .env file."
        )
    
    # Write interpolated content to temporary file for authentication
    with open("client_secret_temp.json", "w") as f:
        f.write(client_secret_content)
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret_temp.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    
    # Clean up temporary file
    if os.path.exists("client_secret_temp.json"):
        os.remove("client_secret_temp.json")
    
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
