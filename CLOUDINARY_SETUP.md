# 🚀 Cloudinary Integration Guide - Step by Step

This guide will help you integrate Cloudinary with your Cloud File Upload project.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Create Cloudinary Account](#step-1-create-cloudinary-account)
3. [Step 2: Get API Credentials](#step-2-get-api-credentials)
4. [Step 3: Setup Environment Variables](#step-3-setup-environment-variables)
5. [Step 4: Install Dependencies](#step-4-install-dependencies)
6. [Step 5: Run the Application](#step-5-run-the-application)
7. [Step 6: Test the Upload Feature](#step-6-test-the-upload-feature)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, make sure you have:
- Python 3.7 or higher installed
- Git (optional, for version control)
- A web browser
- A valid email address for Cloudinary signup

---

## Step 1: Create Cloudinary Account

### 1.1 Visit Cloudinary Website
- Open your browser and go to: **https://cloudinary.com/**

### 1.2 Click "Sign Up For Free"
- Look for the "Sign Up" button on the homepage
- Click it to start the registration process

### 1.3 Register Your Account
You can register using:
- **Email + Password** (traditional method)
- **Google Account** (fastest option)
- **GitHub Account**

**Recommended:** Use Google or GitHub for faster setup

### 1.4 Verify Email (if needed)
- Check your email for a verification link
- Click the link to verify your account
- You'll be redirected to the Cloudinary Dashboard

---

## Step 2: Get API Credentials

Once you're logged into Cloudinary Dashboard:

### 2.1 Locate Account Details
1. In the top right corner, click your **profile icon**
2. Select **Account Settings** or **Dashboard**
3. You should see a section called **"API Keys"** or **"Account Details"**

### 2.2 Find Your Credentials
You need to copy these **three values**:

```
1. Cloud Name: (looks like: d1a2b3c4d)
2. API Key:    (looks like: 123456789012345)
3. API Secret: (looks like: abcdef1234567890_XXXXX)
```

**⚠️ IMPORTANT:** 
- **Never share your API Secret publicly**
- **Never commit it to GitHub**
- Treat it like a password

### 2.3 Screenshot Location
The Account Details section typically shows:
- Cloud Name (top of dashboard)
- API Key (in a table)
- API Secret (in the same table, marked with visibility toggle)

---

## Step 3: Setup Environment Variables

### 3.1 Create .env File
In your project root directory (where `app.py` is located), create a new file named:
```
.env
```

### 3.2 Add Your Credentials
Copy the following template and paste your actual credentials:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Example (with made-up values):**
```env
CLOUDINARY_CLOUD_NAME=d1a2b3c4d
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdef1234567890_XXXXX
```

### 3.3 Verify .gitignore
Make sure your `.gitignore` file includes:
```
.env
```

This prevents accidental upload of your credentials to GitHub.

---

## Step 4: Install Dependencies

### 4.1 Open Terminal/Command Prompt
Navigate to your project directory:
```bash
cd Cloud-file-upload
```

### 4.2 Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

### 4.3 Install Requirements
```bash
pip install -r requirements.txt
```

This will install:
- ✅ flask
- ✅ cloudinary
- ✅ pdf2docx
- ✅ pillow
- ✅ img2pdf
- ✅ docx2pdf
- ✅ python-dotenv
- ✅ requests

---

## Step 5: Run the Application

### 5.1 Start Flask Server
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 5.2 Open in Browser
- Open your web browser
- Go to: **http://localhost:5000**

You should see the Cloud File Converter interface!

---

## Step 6: Test the Upload Feature

### 6.1 Test the Conversion
1. Select a conversion type from the dropdown (e.g., "PDF → Word")
2. Click "Upload File"
3. Choose a sample file (e.g., a PDF file)
4. Click "⚡ Convert"

### 6.2 Verify Upload
- Wait for conversion to complete
- You should see a download link appear
- The download link is a **Cloudinary URL** ✨
- Click the download link to verify it works

### 6.3 Check Cloudinary Dashboard
1. Go to your Cloudinary Dashboard
2. Click **Media Library**
3. You should see your uploaded converted file!

---

## How It Works - Under the Hood

```
User Upload
    ↓
File Conversion (Local)
    ↓
Upload to Cloudinary (Cloud)
    ↓
Get Cloudinary Secure URL
    ↓
Return URL to User
    ↓
User Downloads from Cloudinary
    ↓
Local Files Auto-Deleted ✨
```

### Key Benefits of Cloudinary:
✅ **No local storage needed** - Files go to the cloud
✅ **Automatic cleanup** - Temp files deleted after upload
✅ **Secure URLs** - HTTPS protected links
✅ **CDN Integration** - Fast downloads globally
✅ **Free Tier** - 25 GB of storage + 25 GB monthly uploads

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'cloudinary'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "CLOUDINARY_CLOUD_NAME is not set"
**Solution:**
1. Check if `.env` file exists in project root
2. Verify the file contains all three credentials
3. Make sure there are no typos in variable names
4. Restart Flask server after adding `.env`

### Error: "Cloudinary upload failed"
**Solution:**
1. Verify API credentials are correct in `.env`
2. Go to Cloudinary Dashboard → Account Settings
3. Check API Key and API Secret
4. Make sure you're not exceeding free tier limits

### File Conversion Works but Download Fails
**Solution:**
1. Check internet connection
2. Verify Cloudinary API Key is correct
3. Check file size (Cloudinary free tier: 100 MB per file)
4. Check browser console for errors (F12 → Console)

### PowerPoint Conversion Fails (Windows)
**Solution:**
1. Install Microsoft Office (or LibreOffice)
2. Make sure PowerPoint is installed correctly
3. Try with a simpler .pptx file first

### 404 Error on Download
**Solution:**
1. File may have been deleted from Cloudinary
2. Check Media Library in Cloudinary Dashboard
3. Verify the file was uploaded successfully

---

## Advanced Configuration

### Environment-Specific Settings
Create different `.env` files for different environments:

```bash
# Development
.env.development
CLOUDINARY_CLOUD_NAME=your_dev_cloud

# Production
.env.production
CLOUDINARY_CLOUD_NAME=your_prod_cloud
```

### Upload Presets
For enhanced security, create Upload Presets in Cloudinary:

1. Go to **Dashboard → Settings → Upload**
2. Create a new **Upload Preset**
3. Set restrictions (file size, format, etc.)
4. Use in app.py:
```python
cloudinary.uploader.upload(
    file_path,
    upload_preset='your_preset_name'
)
```

---

## Security Best Practices

⚠️ **DO:**
- ✅ Keep API Secret private
- ✅ Use environment variables
- ✅ Add .env to .gitignore
- ✅ Use HTTPS in production
- ✅ Validate file types on backend

❌ **DON'T:**
- ❌ Commit .env to GitHub
- ❌ Share API keys in messages/chat
- ❌ Expose secrets in client-side code
- ❌ Use hardcoded credentials
- ❌ Allow unlimited file uploads

---

## Next Steps

### Deploy to Cloud (Production)
After testing locally, deploy to:
- **Render.com** (recommended for Flask)
- **Railway.app**
- **Heroku**
- **PythonAnywhere**

See **README.md** for deployment instructions!

### Enhance Your App
- Add user authentication
- Add file upload history
- Add batch conversions
- Add email notifications
- Add payment processing

---

## Useful Links

| Resource | URL |
|----------|-----|
| Cloudinary Docs | https://cloudinary.com/documentation |
| Cloudinary Python SDK | https://cloudinary.com/documentation/cloudinary_sdks#python |
| Flask Documentation | https://flask.palletsprojects.com |
| Python-dotenv Docs | https://python-dotenv.readthedocs.io |

---

## Support & Help

If you encounter issues:
1. Check Cloudinary Dashboard for API usage
2. Review browser console (F12) for errors
3. Check Flask terminal for error messages
4. Visit Cloudinary Documentation
5. Check GitHub Issues (if applicable)

---

**Happy coding! 🎉**
