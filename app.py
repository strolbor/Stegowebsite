from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

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
        
        if jpeg_file and png_file:
            request_time = str(time.time())
            os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'],request_time),exist_ok=True)

            # Bilder Speichern
            jpeg_filename = secure_filename(jpeg_file.filename)
            png_filename = secure_filename(png_file.filename)


            # TxT Speichern
            txt_filename = os.path.join(app.config['UPLOAD_FOLDER'],request_time,"spacer.txt")
            with open(txt_filename, 'w', encoding='utf-8') as datei:
                datei.write(spacer_text)


            jpeg_file.save(os.path.join(app.config['UPLOAD_FOLDER'],request_time, jpeg_filename))
            png_file.save(os.path.join(app.config['UPLOAD_FOLDER'],request_time, png_filename))
            
            #return redirect(url_for('decode'))
            stego_filename = png_filename
            return render_template('encode.html',stego_filename=stego_filename,reqtime=request_time)

    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        stego_file = request.files.get('stego_file')
        spacer_text = request.form.get('spacer_text')
        
        if stego_file:
            
            stego_filename = secure_filename(stego_file.filename)
            stego_file.save(os.path.join(app.config['UPLOAD_FOLDER'], stego_filename))
            
            hidden_file = "dummy_hidden_file.png"  # Platzhalter für den versteckten Dateinamen
            
            return redirect(url_for('download_file', filename=hidden_file))

    return render_template('decode.html')

@app.route('/download/<reqtime>/<filename>')
def download_file(reqtime,filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],reqtime), filename, as_attachment=True)

@app.route('/uploads/<reqtime>/<filename>')
def uploaded_file(reqtime,filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'],reqtime), filename)



if __name__ == '__main__':
    app.run(debug=True)
