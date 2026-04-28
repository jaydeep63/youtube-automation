import os, json, hashlib, pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy import VideoFileClip
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

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

def detect_content_type(filename):
    """Detect content type from video filename"""
    fname_lower = filename.lower()
    
    # Content type keywords mapping
    content_types = {
        "gaming": {"keywords": ["gameplay", "game", "valorant", "fortnite", "pubg", "minecraft", "gta", "elden", "fps", "moba"], "type": "Gaming"},
        "unboxing": {"keywords": ["unboxing", "unbox", "opening", "reveal"], "type": "Unboxing"},
        "review": {"keywords": ["review", "tested", "honest", "thoughts"], "type": "Product Review"},
        "mukbang": {"keywords": ["mukbang", "eating", "asmr", "food"], "type": "Mukbang"},
        "vlog": {"keywords": ["vlog", "daily", "day in my", "routine", "vlogging"], "type": "Vlog"},
        "tutorial": {"keywords": ["tutorial", "how to", "guide", "tips", "learn", "diy"], "type": "Tutorial"},
        "shorts": {"keywords": ["short", "quick", "clip", "moment"], "type": "Short"},
    }
    
    for content_key, content_info in content_types.items():
        for keyword in content_info["keywords"]:
            if keyword in fname_lower:
                return content_key, content_info["type"]
    
    # Default to generic content
    return "generic", "Content"

def detect_category(filename):
    fname_lower = filename.lower()
    for key, details in CATEGORIES.items():
        if key in fname_lower:
            return key, details
    # Return default category if no match found
    content_type_key, content_type_name = detect_content_type(filename)
    
    default_category = {
        "title_suffix": "Highlights",
        "primary_keyword": f"{content_type_name} Highlights",
        "secondary_keywords": ["viral", "trending", "highlights", "must watch"],
        "description_intro": f"Check out this amazing {content_type_name.lower()}! 🎬",
        "description_body": f"Don't miss this incredible {content_type_name.lower()} video. Like, comment, and subscribe for more content!",
        "hashtags_list": [f"#{content_type_name.replace(' ', '')}", "#Trending", "#Highlights", "#MustWatch"],
        "tags": [content_type_name, "Trending", "Highlights"]
    }
    return "default", default_category

def generate_hashtags(category_key):
    """Generate SEO-optimized hashtags from category data"""
    if category_key in CATEGORIES:
        hashtags = CATEGORIES[category_key].get("hashtags_list", [])
    else:
        hashtags = CATEGORIES["default"].get("hashtags_list", []) if "default" in CATEGORIES else ["#Trending", "#Highlights"]
    return " ".join(hashtags)

def check_ollama_available():
    """Check if Ollama is running on localhost:11434"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def generate_title_with_ollama(filename, category_key, template_type="long_form"):
    """Generate title using Ollama AI"""
    try:
        category = CATEGORIES.get(category_key, {})
        primary_keyword = category.get("primary_keyword", "Video Highlights")
        title_suffix = category.get("title_suffix", "Highlights")
        content_type_key, content_type_name = detect_content_type(filename)
        
        prompt = f"""Generate a YouTube video title for a {content_type_name} video.
Filename: {filename}
Type: {title_suffix}
Keywords to include: {primary_keyword}, YouTube SEO
Requirements:
- Maximum 60 characters
- Include primary keyword at the start
- Be catchy and engaging
- Include emojis if appropriate

Generate ONLY the title, nothing else."""
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=30
        )
        
        if response.status_code == 200:
            title = response.json().get("response", "").strip()
            # Clean up title
            title = title.replace("\n", "").replace("Title: ", "")
            if len(title) > 60:
                title = title[:57] + "..."
            return title
        else:
            return None
    except Exception as e:
        print(f"Ollama generation error: {e}")
        return None

def generate_description_with_ollama(filename, category_key):
    """Generate description using Ollama AI"""
    try:
        category = CATEGORIES.get(category_key, {})
        title_suffix = category.get("title_suffix", "Highlights")
        hashtags = generate_hashtags(category_key)
        content_type_key, content_type_name = detect_content_type(filename)
        
        prompt = f"""Generate a YouTube video description for a {content_type_name} video.
Video type: {title_suffix}
Filename: {filename}
Hashtags to include: {hashtags}

Requirements:
- First line should be engaging and summarize the video
- 2-3 sentences of body text
- Include the hashtags
- Maximum 4900 characters
- Professional but conversational tone

Generate ONLY the description, nothing else."""
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=30
        )
        
        if response.status_code == 200:
            description = response.json().get("response", "").strip()
            description = description.replace("Description: ", "")
            return description
        else:
            return None
    except Exception as e:
        print(f"Ollama generation error: {e}")
        return None

def optimize_title_seo(template, filename, category_key):
    """Optimize title with front-loaded primary keywords for better SEO"""
    if category_key in CATEGORIES:
        category = CATEGORIES[category_key]
        primary_keyword = category.get("primary_keyword", "Video Highlights")
        title_suffix = category.get("title_suffix", "Highlights")
    else:
        primary_keyword = "Video Highlights"
        title_suffix = "Highlights"
    
    # Replace placeholders - primary keywords front-loaded for SEO
    title = template.replace("{primary_keyword}", primary_keyword)
    title = title.replace("{category}", title_suffix)
    title = title.replace("{filename}", filename)
    
    # Keep title under 60 chars for optimal YouTube display
    if len(title) > 60:
        title = title[:57] + "..."
    
    return title

def optimize_description_seo(template, category_key):
    """Create SEO-optimized description with keyword placement"""
    if category_key in CATEGORIES:
        category = CATEGORIES[category_key]
        description_intro = category.get("description_intro", "Check out this amazing content!")
        description_body = category.get("description_body", "Like, comment, and subscribe for more!")
        secondary_keywords = category.get("secondary_keywords", [])
    else:
        description_intro = "Check out this amazing content!"
        description_body = "Like, comment, and subscribe for more!"
        secondary_keywords = []
    
    hashtags = generate_hashtags(category_key)
    
    # Build description with strategic keyword placement
    description = template.replace("{description_intro}", description_intro)
    description = description.replace("{description_body}", description_body)
    description = description.replace("{hashtags}", hashtags)
    
    # Add secondary keywords naturally in description
    if secondary_keywords and len(description) < 4900:  # YouTube limit is 5000
        keywords_text = f"\nKeywords: {', '.join(secondary_keywords[:5])}"
        description = description.replace("{hashtags}", keywords_text + "\n\n{hashtags}").replace("{hashtags}", hashtags)
    
    return description

def get_metadata(filename, resolution):
    """Generate metadata with SEO optimization and category-specific templates"""
    # Determine video format (long_form or shorts)
    if resolution == (1920, 1080):
        template_type = "long_form"
    elif resolution == (1080, 1920):
        template_type = "shorts"
    else:
        template_type = "long_form"

    template = META[template_type]
    category_key, category_details = detect_category(filename)
    
    # Check if Ollama should be used
    use_ollama = config.get("use_ollama", False)
    ollama_available = False
    
    if use_ollama:
        ollama_available = check_ollama_available()
        if ollama_available:
            print(f"✓ Ollama found. Generating AI title and description...")
        else:
            print("✗ Ollama not running. Falling back to templates.")
    
    # Generate title (AI or template)
    if use_ollama and ollama_available:
        title = generate_title_with_ollama(filename, category_key, template_type)
        if title is None:
            title = optimize_title_seo(template["title_template"], filename, category_key)
    else:
        title = optimize_title_seo(template["title_template"], filename, category_key)
    
    # Generate description (AI or template)
    if use_ollama and ollama_available:
        description = generate_description_with_ollama(filename, category_key)
        if description is None:
            description = optimize_description_seo(template["description_template"], category_key)
    else:
        description = optimize_description_seo(template["description_template"], category_key)
    
    # Combine tags: template tags + category tags + secondary keywords as tags
    tags = list(set(template["tags"] + category_details.get("tags", [])))
    
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
