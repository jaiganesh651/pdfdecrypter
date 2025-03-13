from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from pypdf import PdfReader, PdfWriter
import os

app = Flask(__name__)
app.secret_key = 'secret_key_for_flashing_messages'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the file and password
        pdf_file = request.files['pdf_file']
        password = request.form['password']

        if not pdf_file.filename.endswith('.pdf'):
            flash('Invalid file format. Please upload a PDF file.', 'danger')
            return redirect(request.url)

        # Save the uploaded PDF
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
        pdf_file.save(pdf_path)

        # Load the PDF
        reader = PdfReader(pdf_path)

        # Check if the PDF is encrypted
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                decrypted_path = os.path.join(UPLOAD_FOLDER, 'decrypted.pdf')
                with open(decrypted_path, 'wb') as decrypted_pdf:
                    writer.write(decrypted_pdf)

                flash('PDF decrypted successfully!', 'success')
                return send_file(decrypted_path, as_attachment=True)

            except Exception as e:
                flash('Invalid password or error in decryption.', 'danger')
        else:
            flash('The PDF is not encrypted.', 'info')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
