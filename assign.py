import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
from PIL import Image
import PyPDF2

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
filename=""
file_type=" "
file_size=" "


#files = UploadSet('files', extensions=('pdf','jpg'))
#configure_uploads(app, files)
#patch_request_class(app)  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    flag=0
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        mean=""
        image_size=""
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            result = request.form
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            file_ctime=os.path.getctime('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
            file_ctime = datetime.datetime.fromtimestamp(file_ctime)
            file_mtime=os.path.getmtime('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
            file_mtime = datetime.datetime.fromtimestamp(file_mtime)
            if filename[-3:] =='jpg':
                file_type='jpg'
                image = Image.open('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
                image_size=image.size
                width, height = image_size
                total = 0
                for i in range(0, width):
                     for j in range(0, height):
                              total += image.getpixel((i,j))[0]
                mean = total / (width * height)
                
               
            elif filename[-3:].lower() =='pdf':
                file_type='pdf'
                file_info=os.stat('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
                file_sizebytes=file_info.st_size
                check=open('C:\\x-zone\\UC\\CLOUD\\project\\'+filename,"rb")
                reader = PyPDF2.PdfFileReader(check) 
                file_numpages=reader.getNumPages()
                check.close()
                totalWords = 0
                #for i in range(file_numpages):
                #   text = extractData(reader, i)
                #   totalWords+=getWordCount(text)
                #numOflines = 0
                #with open(reader,'rb') as f:
                #   for line in f:
                  #    numOflines = numOflines + 1


            elif filename[-3:].lower() =='jpeg':
                file_type='jpeg'
                image = Image.open('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
                image_size=image.size
                image_size=image.size
                width, height = image_size
                total = 0
                for i in range(0, width):
                     for j in range(0, height):
                              total += image.getpixel((i,j))[0]
                mean = total / (width * height)

            elif filename[-3:].lower() =='png':
                file_type='png'
                image = Image.open('C:\\x-zone\\UC\\CLOUD\\project\\'+filename)
                image_size=image.size
                image_size=image.size
                width, height = image_size
                total = 0
                for i in range(0, width):
                     for j in range(0, height):
                              total += image.getpixel((i,j))[0]
                mean = total / (width * height)

            for key,value in result.items():
                    if key=="file_size":
                        file_size=value

                            


    else:
        filename=" "
        file_type=" "
        file_size=" "
        file_ctime=""
        file_mtime=""
        image_size=""
        mean=" "
        file_sizebytes=""
        file_numpages=""
        totalWords=""
    return render_template("hi.html",filename=filename,totalWords=totalWords,file_type=file_type,file_size=file_size,mean=mean,file_ctime=file_ctime,file_numpages=file_numpages,file_mtime=file_mtime,image_size=image_size,file_sizebytes=file_sizebytes)
  


	
from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/delete/<filename>')
def delete_file(filename):
     file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
     os.remove(file_path)
     
     return redirect(url_for('upload_file'))

def getWordCount(data):
    data=data.split()
    return len(data)

if __name__ == '__main__':
    app.run(debug=TRUE)
