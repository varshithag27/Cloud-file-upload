from flask import Flask, request, send_file, render_template, after_this_request, abort
import os
import uuid
from PIL import Image
import img2pdf

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

        return {
            "success": True,
            "download_url": f"/download/{os.path.basename(output_path)}",
            "filename": os.path.basename(output_path),
        }

    except Exception as exc:
        return {"success": False, "error": str(exc)}, 500

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)


@app.route("/download/<filename>")
def download(filename):
    safe_name = os.path.basename(filename)
    output_path = os.path.join(UPLOAD_FOLDER, safe_name)
    if not os.path.exists(output_path):
        abort(404)

    @after_this_request
    def remove_file(response):
        try:
            if os.path.exists(output_path):
                os.remove(output_path)
        except Exception:
            pass
        return response

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
