from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import base64

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(application.config['UPLOAD_FOLDER'], exist_ok=True)

@application.route('/')
def home():
    return redirect(url_for('encode'))

@application.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        jpeg_file = request.files.get('jpeg_file')
        png_file = request.files.get('png_file')
        spacer_text = request.form.get('spacer_text')
        
        if jpeg_file and png_file:
            request_time = str(time.time())
            path = os.path.join(application.config['UPLOAD_FOLDER'],request_time)
            os.makedirs(path,exist_ok=True)

            headerFile = os.path.join(path,"header.txt")
            with open(headerFile,'w') as datei:
                datei.write(dict(request.headers))
            

            # sicherer namen
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
            
            # Output File
            output_filename = "output.jpg"
            outputfile = os.path.join(path,output_filename)

            # Concat
            with open(os.path.join(path, jpeg_filename), 'rb') as file:
                jpeg_data = file.read()
            concatenated_data = jpeg_data + bytes(spacer_text, 'utf-8') + encoded_string
            with open(outputfile,"wb") as file:
                file.write(concatenated_data)

            # Return
            stego_filename = output_filename
            return render_template('encode.html',stego_filename=stego_filename,reqtime=request_time)

    return render_template('encode.html')

@application.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        stego_file = request.files.get('stego_file')
        spacer_text = request.form.get('spacer_text')
        
        if stego_file:
            request_time = str(time.time())
            path = os.path.join(application.config['UPLOAD_FOLDER'], request_time)
            os.makedirs(path,exist_ok=True)

            headerFile = os.path.join(path,"header.txt")
            with open(headerFile,'w') as datei:
                datei.write(dict(request.headers))
            
            stego_filename = secure_filename(stego_file.filename)
            stego_file.save(os.path.join(path, stego_filename))
            
            #extrakt hidden png
            hidden_filename = 'hidden.png'
            tmp = ''
            with open(os.path.join(path, stego_filename), 'rb') as file:
                hidden_file = file.read()
            tmp = hidden_file.split(bytes(spacer_text, 'utf-8'))[1] #the raw png in str
            
            #save png
            with open(os.path.join(path, hidden_filename), 'wb') as pic:
                pic.write(base64.b64decode(tmp))

            return redirect(url_for('download_file', filename=hidden_filename, reqtime=request_time))

    return render_template('decode.html')

@application.route('/download/<reqtime>/<filename>')
def download_file(reqtime,filename):
    return send_from_directory(os.path.join(application.config['UPLOAD_FOLDER'],reqtime), filename, as_attachment=True)

@application.route('/uploads/<reqtime>/<filename>')
def uploaded_file(reqtime,filename):
    return send_from_directory(os.path.join(application.config['UPLOAD_FOLDER'],reqtime), filename)



if __name__ == '__main__':
    application.run(debug=True,ssl_context='adhoc')
