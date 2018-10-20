import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import datetime
import PIL
from PIL import Image
import threading
import PyPDF2
import time
from flask import send_from_directory

UPLOAD_FOLDER = '/storage'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])
DIR_PATH=os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DIR_PATH+UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
filename=""
file_type=" "
file_size=" "

def pdf_count(filename,file_numpages):
	file_path=app.config['UPLOAD_FOLDER']+'/'+filename
	totalwords=0
	num_lines=0
	d=[]
	for i in range(file_numpages):
		text=extractData(file_path,i)
		totalwords += getWordCount(text)
		num_lines += text.count("\n")
        time.sleep(1)
        d.append(totalwords)
        d.append(num_lines)
        pdffileobj= open(file_path,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        d.append(pdfreader.getPage(0).mediaBox)
        pdffileobj.close()
        return d

def extractData(file_path,i):
        pdffileobj=open(file_path,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        pageobj=pdfreader.getPage(i)
        data=pageobj.extractText()
        pdffileobj.close()
        return data

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("storage", filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    file_path=''
    flag=0
    d=[]
    file_new=""
    filename=""
    if request.method == 'POST':
        file_type=filename[-3:].lower()
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        try:
              file = request.files['file']
        except:
              return render_template("size_limit.html")
        mean=""
        image_size=""
        d=[]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            result = request.form
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) 
            file_ctime=os.path.getctime(app.config['UPLOAD_FOLDER']+'/'+filename)
            file_ctime = datetime.datetime.fromtimestamp(file_ctime)
            file_mtime=os.path.getmtime(app.config['UPLOAD_FOLDER']+'/'+filename)
            file_mtime = datetime.datetime.fromtimestamp(file_mtime)
            t=threading.Thread(target=wait_worker,args=(filename,))
            t.start()

            
            if filename[-3:].lower() =='pdf':
                d=[]
                file_type=filename[-3:].lower()
                file_info=os.stat(app.config['UPLOAD_FOLDER']+'/'+filename)
                file_sizebytes=file_info.st_size
                check=open(app.config['UPLOAD_FOLDER']+'/'+filename,"rb")
                reader = PyPDF2.PdfFileReader(check) 
                file_numpages=reader.getNumPages()
                d=pdf_count(filename,file_numpages)
                check.close()
                
                #timer_five_mins(filename)
                #for i in range(file_numpages):
                #   text = extractData(reader, i)
                #   totalWords+=getWordCount(text)
                #numOflines = 0
                #with open(reader,'rb') as f:
                #   for line in f:
                  #    numOflines = numOflines + 1


            else :
                file_type=filename[-3:].lower()
                image = Image.open(app.config['UPLOAD_FOLDER']+'/'+filename)
                file_info=os.stat(app.config['UPLOAD_FOLDER']+'/'+filename)
                file_sizebytes=file_info.st_size
                image_size=image.size
                width, height = image_size
                file_new=filename+'n'
                file_path='../'+'storage/'+filename
                # getThumb(filename,file_new)
                total = 0
                for i in range(0, width):
                     for j in range(0, height):
                              total += image.getpixel((i,j))[0]
                mean = total / (width * height)
                file_numpages=""

    else:
        filename=" "
        file_type=" "
        file_ctime=""
        file_mtime=""
        image_size=""
        mean=" "
        file_sizebytes=""
        file_numpages=""
        totalWords=""

    return render_template("hi.html",file_path=file_path,filename=filename,d=d,file_type=file_type,mean=mean,file_ctime=file_ctime,file_numpages=file_numpages,file_mtime=file_mtime,image_size=image_size,file_sizebytes=file_sizebytes)
  


	

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory("storage", filename)


@app.route('/delete/<filename>')
def delete_file(filename):
     file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
     
     try:
        os.remove(file_path)
     except :
        pass  
     return redirect(url_for('upload_file'))

def getWordCount(data):
    data=data.split()
    return len(data)

def wait_worker(filename):
    time.sleep(300);
    path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if(os.path.isfile(path)):
       os.remove(path)
    return

if __name__ == '__main__':
    app.run(debug=TRUE)

