from flask import Flask, request, send_file, render_template, after_this_request, abort
import os
import uuid
import io
import requests
from PIL import Image
import img2pdf
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cloudinary Configuration with error checking
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

# Debug: Print if credentials are loaded
if not cloud_name or not api_key or not api_secret:
    print("⚠️ WARNING: Cloudinary credentials not found in environment!")
    print(f"  CLOUDINARY_CLOUD_NAME: {cloud_name}")
    print(f"  CLOUDINARY_API_KEY: {api_key}")
    print(f"  CLOUDINARY_API_SECRET: {api_secret}")
    print("Make sure .env file exists in project root with your credentials!")
else:
    print(f"✅ Cloudinary configured successfully!")
    print(f"   Cloud Name: {cloud_name}")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)


def make_unique_path(filename, suffix):
    root, _ = os.path.splitext(filename)
    safe_root = os.path.basename(root)
    return os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{safe_root}{suffix}")


def powerpoint_to_pdf(input_path, output_path):
    try:
        import pythoncom
        from win32com.client import Dispatch

        pythoncom.CoInitialize()
        powerpoint = Dispatch("PowerPoint.Application")
        presentation = powerpoint.Presentations.Open(
            os.path.abspath(input_path), False, False, False
        )
        presentation.SaveAs(os.path.abspath(output_path), 32)
        presentation.Close()
        powerpoint.Quit()
    except Exception as exc:
        raise RuntimeError(
            "PowerPoint conversion failed. Make sure PowerPoint is installed and the file is a valid PPT/PPTX."
        ) from exc


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return {"success": False, "error": "No file uploaded."}, 400

    f = request.files["file"]
    if not f.filename:
        return {"success": False, "error": "Please choose a file."}, 400

    conv_type = request.form.get("conversion", "")
    input_path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(input_path)
    output_path = None

    try:
        ext = os.path.splitext(f.filename)[1].lower()

        if conv_type == "pdf_to_word":
            if ext != ".pdf":
                return {"success": False, "error": "Please upload a PDF file."}, 400
            output_path = make_unique_path(f.filename, ".docx")
            from pdf2docx import Converter
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()

        elif conv_type == "word_to_pdf":
            if ext not in [".doc", ".docx"]:
                return {"success": False, "error": "Please upload a Word file."}, 400
            output_path = make_unique_path(f.filename, ".pdf")
            from docx2pdf import convert
            convert(input_path, output_path)

        elif conv_type == "ppt_to_pdf":
            if ext not in [".ppt", ".pptx"]:
                return {"success": False, "error": "Please upload a PPT file."}, 400
            output_path = make_unique_path(f.filename, ".pdf")
            powerpoint_to_pdf(input_path, output_path)

        elif conv_type == "image_to_pdf":
            if ext not in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]:
                return {"success": False, "error": "Please upload an image file."}, 400
            output_path = make_unique_path(f.filename, ".pdf")
            with open(output_path, "wb") as out:
                out.write(img2pdf.convert(input_path))

        elif conv_type == "jpg_to_png":
            if ext not in [".jpg", ".jpeg"]:
                return {"success": False, "error": "Please upload a JPG file."}, 400
            output_path = make_unique_path(f.filename, ".png")
            Image.open(input_path).save(output_path)

        elif conv_type == "png_to_jpg":
            if ext != ".png":
                return {"success": False, "error": "Please upload a PNG file."}, 400
            output_path = make_unique_path(f.filename, ".jpg")
            Image.open(input_path).convert("RGB").save(output_path)

        else:
            return {"success": False, "error": "Conversion type not supported."}, 400

        # Upload converted file to Cloudinary
        try:
            upload_result = cloudinary.uploader.upload(
                output_path,
                resource_type="auto",
                public_id=os.path.splitext(os.path.basename(output_path))[0],
                overwrite=True
            )
            cloudinary_url = upload_result['secure_url']
            
            return {
                "success": True,
                "download_url": cloudinary_url,
                "filename": os.path.basename(output_path),
                "cloudinary_public_id": upload_result['public_id']
            }
        except Exception as upload_exc:
            return {"success": False, "error": f"Cloudinary upload failed: {str(upload_exc)}"}, 500

    except Exception as exc:
        return {"success": False, "error": str(exc)}, 500

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if output_path and os.path.exists(output_path):
            os.remove(output_path)


@app.route("/download/<path:public_id>")
def download(public_id):
    """
    Download file from Cloudinary by redirecting to the secure URL
    """
    try:
        # Get resource from Cloudinary
        resource = cloudinary.api.resource(public_id)
        download_url = resource.get('secure_url')
        
        if not download_url:
            abort(404)
        
        # Get the file and send it
        import requests
        response = requests.get(download_url)
        
        if response.status_code == 200:
            return send_file(
                io.BytesIO(response.content),
                as_attachment=True,
                download_name=os.path.basename(download_url)
            )
        else:
            abort(404)
    except Exception:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
