☁️ Cloud File Converter
A simple cloud-based file upload and conversion system built using Python.
This project allows users to upload files, process/convert them, and store them using Cloudinary cloud storage.

🚀 Features
📁 Upload files through web interface
🔄 File conversion functionality (PDF, Word, PPT, Images)
☁️ Cloud storage integration (Cloudinary)
🔐 Secure handling of files
🌐 Simple and user-friendly UI
📥 Direct download links from cloud

🛠️ Tech Stack
Backend: Python (Flask)
Frontend: HTML, CSS
Cloud: Cloudinary
Libraries: Cloudinary SDK, Flask, pdf2docx, Pillow

📂 Project Structure
cloud-file-converter/
│
├── app.py
├── requirements.txt
├── .env (create this file)
└── templates/ 
    └── index.html

⚙️ Installation & Setup

1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/cloud-file-converter.git
cd cloud-file-converter
```

2️⃣ Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

☁️ Cloudinary Configuration

### Step 1: Create Cloudinary Account
- Go to [https://cloudinary.com/](https://cloudinary.com/)
- Click "Sign Up For Free"
- Create an account (use email or Google/GitHub)

### Step 2: Get Your Credentials
- After signup, you'll see your Dashboard
- Look for "Account Details" section
- Copy these three values:
  - **Cloud Name** (under "Account Details")
  - **API Key** (under "Account Details")
  - **API Secret** (under "Account Details") - Keep this SECRET!

### Step 3: Create .env File
Create a `.env` file in the project root directory with your Cloudinary credentials:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**⚠️ Important:** Never commit `.env` to GitHub. Add it to `.gitignore`:
```
.env
```

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

📸 How It Works
1. User selects conversion type from dropdown
2. User uploads a file through the web interface
3. Backend converts the file using appropriate libraries
4. Converted file is automatically uploaded to Cloudinary
5. User receives a direct download link from Cloudinary
6. Local temporary files are automatically cleaned up

✨ Supported Conversions
- 📄 PDF ↔️ Word (DOCX)
- 🎯 Word → PDF
- 📊 PPT/PPTX → PDF
- 🖼️ Image → PDF
- 🎨 JPG ↔️ PNG

🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main web interface |
| `/convert` | POST | Convert and upload file |
| `/download/<public_id>` | GET | Download from Cloudinary |

🚀 Deploying to Production

### Option 1: Deploy on Render
1. Push your code to GitHub
2. Go to [https://render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Set environment variables (CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET)
6. Deploy!

### Option 2: Deploy on Railway
1. Go to [https://railway.app](https://railway.app)
2. Connect GitHub
3. Create new project
4. Add environment variables
5. Deploy!

### Option 3: Deploy on Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
heroku config:set CLOUDINARY_CLOUD_NAME=xxx CLOUDINARY_API_KEY=xxx CLOUDINARY_API_SECRET=xxx
```

📌 Future Improvements
- 🔐 User authentication & login
- 📊 Dashboard for file tracking and history
- ⚡ Batch file conversion
- 🌍 Support for more file formats
- 📈 File conversion analytics
- 💾 Storage quota management

🐛 Troubleshooting

**Problem:** "ModuleNotFoundError: No module named 'cloudinary'"
**Solution:** Run `pip install -r requirements.txt`

**Problem:** "CLOUDINARY_CLOUD_NAME is not set"
**Solution:** Make sure `.env` file exists with correct values in project root

**Problem:** "PowerPoint conversion failed"
**Solution:** On Windows, install Microsoft Office. On Mac/Linux, alternative libraries needed

**Problem:** Files not uploading to Cloudinary
**Solution:** Check your API credentials in .env file

📚 Resources
- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)

👩‍💻 Author
Varshitha

⭐ Acknowledgements
- Cloudinary for cloud storage
- Flask for web framework
- Open-source community

📜 License
This project is for educational purposes.
