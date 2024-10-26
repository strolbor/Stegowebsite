from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Erstelle den Upload-Ordner, falls er nicht existiert
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return redirect(url_for('encode'))

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        jpeg_file = request.files.get('jpeg_file')
        png_file = request.files.get('png_file')
        spacer_text = request.form.get('spacer_text')
        
        # Dateien speichern, falls hochgeladen
        if jpeg_file and png_file:
            jpeg_filename = secure_filename(jpeg_file.filename)
            png_filename = secure_filename(png_file.filename)
            jpeg_file.save(os.path.join(app.config['UPLOAD_FOLDER'], jpeg_filename))
            png_file.save(os.path.join(app.config['UPLOAD_FOLDER'], png_filename))
            
            # Hier kommt der Platzhalter für den Stego-Befehl
            # z.B. stego_encode(jpeg_filename, png_filename, spacer_text)

            return redirect(url_for('decode'))
        
    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        stego_file = request.files.get('stego_file')
        spacer_text = request.form.get('spacer_text')
        
        # Datei speichern und mit Spacer-Text verarbeiten, falls hochgeladen
        if stego_file:
            stego_filename = secure_filename(stego_file.filename)
            stego_file.save(os.path.join(app.config['UPLOAD_FOLDER'], stego_filename))
            
            # Hier kommt der Platzhalter für den Stego-Befehl
            # z.B. hidden_file = stego_decode(stego_filename, spacer_text)
            hidden_file = "dummy_hidden_file.png"  # Platzhalter für den versteckten Dateinamen
            
            return redirect(url_for('download_file', filename=hidden_file))

    return render_template('decode.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
