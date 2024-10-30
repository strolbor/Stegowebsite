from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import base64

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
            path = os.path.join(app.config['UPLOAD_FOLDER'],request_time)
            os.makedirs(path,exist_ok=True)

            # sicher namen
            jpeg_filename = secure_filename(jpeg_file.filename)
            png_filename = secure_filename(png_file.filename)


            # TxT Speichern
            spacerTXT = os.path.join(path,"spacer.txt")
            with open(spacerTXT, 'w', encoding='utf-8') as datei:
                datei.write(spacer_text)

            # Bilder speichern
            jpeg_path = os.path.join(path, jpeg_filename)
            jpeg_file.save(jpeg_path)

            png_name = os.path.join(path, png_filename)
            png_file.save(png_name)
            
            # Encode
            encoded_string = None
            with open(png_name,"rb") as b64file:
                encoded_string = base64.b64encode(b64file.read())
            
            png_nameb64 = png_name+".b64"
            with open(png_name+".b64","wb") as file:
                file.write(encoded_string)

            # Einbetten
            ## cat coverfile.jpg spacer.txt secret_msg_in.b64 > output.jpg
            output_filename = "output.jpg"
            outputfile = os.path.join(path,output_filename)
            cmd = f"cat {jpeg_path} {spacerTXT} {png_nameb64} > {outputfile}"
            #print(cmd)
            os.system(cmd)

            # Return
            stego_filename = output_filename
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




"""Dies ist für decode notwenig. Um Scapel zu konfigurieren."""
def txt_datei_zu_hex(dateipfad):
    with open(dateipfad, 'rb') as datei:
        hex_output = datei.read().hex()
        escaped_string = ''.join(f'\\x{byte:02x}' for byte in bytes.fromhex(hex_output))
        print(hex_output) # Ausgabe:  42420a
        print(escaped_string)  # Ausgabe: \x42\x42\x0a
        out = [hex_output,escaped_string]
        return out


if __name__ == '__main__':
    app.run(debug=True)
