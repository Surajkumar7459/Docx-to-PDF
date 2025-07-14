from flask import Flask, request, send_file
import os, subprocess, uuid

app = Flask(__name__)

@app.route('/')
def home():
    return 'DOCX to PDF Conversion API'

@app.route('/convert', methods=['POST'])
def convert_docx_to_pdf():
    if 'file' not in request.files:
        return 'No file uploaded.', 400

    uploaded_file = request.files['file']
    if not uploaded_file.filename.endswith('.docx'):
        return 'Only .docx files are allowed.', 400

    uid = str(uuid.uuid4())
    input_path = f"/tmp/{uid}.docx"
    output_path = f"/tmp/{uid}.pdf"

    uploaded_file.save(input_path)

    try:
        subprocess.run([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', '/tmp',
            input_path
        ], check=True)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Conversion failed: {str(e)}", 500
    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True)
