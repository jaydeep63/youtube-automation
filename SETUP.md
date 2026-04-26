# 🚀 AI Title Generator - Setup & Usage Guide

## Quick Start (Easiest Method)

### First Time Setup
1. **Double-click `setup-aititle-gen.bat`** in the project folder
2. Let it run (first time: ~15-20 minutes due to model download)
3. Done! Setup is complete

### Every Time You Want to Upload
1. **Double-click `run-uploader.bat`** in the project folder
2. The script will:
   - ✓ Check if Ollama is running
   - ✓ Start Ollama if needed
   - ✓ Launch the uploader automatically
3. Just double-click and go! 🎉

## What Gets Installed?

- **Ollama** - Local AI engine (runs on your computer, no cloud)
- **Mistral Model** - AI model for generating titles (~4GB download)
- **Python Dependencies** - Required packages for the uploader

## Workflow Summary

```
┌─────────────────────────────────────────────┐
│  FIRST TIME ONLY                            │
│  Double-click: setup-aititle-gen.bat        │
│  (Takes ~15-20 minutes)                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  EVERY TIME YOU UPLOAD                      │
│  Double-click: run-uploader.bat             │
│  (Takes ~2-3 minutes per video)             │
└─────────────────────────────────────────────┘
```

## File Overview

| File | Purpose | Usage |
|------|---------|-------|
| `setup-aititle-gen.bat` | First-time setup installer | Run once to install everything |
| `run-uploader.bat` | Daily uploader launcher | Run every time you upload videos |
| `uploader.py` | Main uploader script | Do NOT run directly |
| `config.json` | Configuration file | Customize categories & metadata |
| `SETUP.md` | This guide | Reference when needed |

## Step-by-Step Setup (Manual Method)

If the batch file doesn't work, follow these steps:

### Step 1: Install Ollama
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Restart your computer (recommended)

### Step 2: Download Mistral Model
1. Open Command Prompt or PowerShell
2. Run: `ollama pull mistral`
3. Wait for download to complete (5-15 minutes, ~4GB)

### Step 3: Install Python Dependencies
1. Open Command Prompt in the project folder
2. Run: `.\.venv\Scripts\pip install -r requirements.txt`
3. Wait for installation to complete

### Step 4: Run the Uploader
1. Make sure Ollama is running
2. Run: `python uploader.py`

## Troubleshooting

### "Ollama not running" message
**Solution:** The `run-uploader.bat` will try to start it automatically. If it fails:
1. Make sure Ollama is installed (run `setup-aititle-gen.bat`)
2. Manually start Ollama from Windows Start Menu

### "Mistral model not found" during upload
**Solution:** Run `ollama pull mistral` in Command Prompt to manually download it.

### Python errors
**Solution:** Make sure you ran `setup-aititle-gen.bat` first to install dependencies.

### Setup script won't run
**Solution:** Try running as Administrator:
1. Right-click `setup-aititle-gen.bat` or `run-uploader.bat`
2. Select "Run as Administrator"

### Uploader says "use_ollama is false"
**Solution:** Edit `config.json` and change:
```json
"use_ollama": true   // Set to true to enable AI
```

## Configuration

Edit `config.json` to customize:

### Enable/Disable AI
```json
"use_ollama": true   // Set to false for template-based generation only
```

### Change Video Categories
```json
"categories": {
    "clutch": {
        "title_suffix": "Your Title Here",
        "primary_keyword": "Your Keyword",
        "secondary_keywords": ["keyword1", "keyword2"],
        ...
    }
}
```

### Change Scan Folder
```json
"scan_folder": "C:\\Path\\To\\Your\\Videos"
```

## Performance Notes

- **First run with Ollama:** ~5-10 seconds per video (model loading)
- **Subsequent runs:** ~2-3 seconds per video
- **Model size:** ~4GB (downloaded once)
- **CPU/GPU:** Works on any PC (no GPU needed, but GPU makes it faster)

## Data Privacy

✅ **All processing happens locally on your computer**
- No data sent to cloud
- No accounts needed
- Your videos stay private
- Model runs offline

## Common Questions

### Do I need to keep Ollama running all the time?
**No!** The `run-uploader.bat` will start it automatically when needed. Once you close the uploader, Ollama stops in the background.

### Can I use this without AI?
**Yes!** Set `"use_ollama": false` in `config.json` to use template-based generation instead.

### What if I have videos in different folders?
Edit `config.json` and change the `scan_folder` path to where your videos are located.

### How much internet does this use?
- **Setup:** ~4GB (Mistral model download, one-time only)
- **Uploads:** Same as YouTube (depends on video size)
- **During upload:** No extra internet needed beyond YouTube upload

### Can I run this on Mac or Linux?
Yes! Ollama works on Mac and Linux too. The batch files won't work, but you can:
1. Run setup steps manually
2. Run `python uploader.py` directly

## Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Make sure Ollama is installed: open Command Prompt and type `ollama`
3. Verify Python: open Command Prompt and type `python --version`
4. Check internet connection (needed only for first setup)
5. Try running as Administrator

## Next Steps

Once setup is complete:
1. ✅ Configure `config.json` with your video categories
2. ✅ Add your YouTube videos to the scan folder
3. ✅ Double-click `run-uploader.bat`
4. ✅ Enjoy AI-generated titles! 🎉

## Support Files

All necessary files are included in this folder:
- `setup-aititle-gen.bat` - Setup installer
- `run-uploader.bat` - Daily launcher  
- `uploader.py` - Main application
- `config.json` - Configuration
- `requirements.txt` - Python dependencies
