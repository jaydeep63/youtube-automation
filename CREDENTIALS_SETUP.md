# Secure Credentials Setup Guide

## Overview
This project uses environment variables to securely store API credentials instead of committing them to Git.

## File Structure

- **`.env`** - Your actual credentials (⚠️ **NEVER commit this**)
- **`.env.example`** - Template showing required variables (safe to commit)
- **`client_secret.json.example`** - Template file showing the format (safe to commit)
- **`client_secret.json`** - Auto-generated at runtime from `.env` (never committed)

## Setup Instructions

### 1. Get Your Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 Desktop Application** credentials
5. Download the JSON file

### 2. Fill in Your `.env` File

Edit `.env` and replace the placeholder values:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-actual-client-secret
GOOGLE_PROJECT_ID=your-project-id
```

### 3. Run Your Script

The script will automatically:
- ✓ Read credentials from `.env`
- ✓ Generate `client_secret.json` at runtime
- ✓ Never store secrets in Git

## Security Best Practices

✅ **DO:**
- Store real credentials in `.env`
- Add `.env` to `.gitignore` (already done)
- Rotate credentials regularly
- Use separate credentials for dev/prod

❌ **DON'T:**
- Commit `.env` to Git
- Share `.env` file with others
- Hardcode credentials in code
- Upload `.env` to public repositories

## For Team Members

1. Copy `.env.example` to `.env`
2. Ask project maintainer for actual credentials
3. Fill in `.env` with provided values
4. Keep `.env` private!

## Troubleshooting

**"Missing credentials" error?**
- Make sure `.env` file exists in the same directory as `uploader.py`
- Verify all three variables are set: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_PROJECT_ID`

**Module not found `dotenv`?**
- Install with: `pip install python-dotenv`
