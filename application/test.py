from application import app
from flask import redirect, render_template, url_for,request,session
import secrets
import os
from . import util
import cv2
import pytesseract
import numpy as np
from .form import QRCodeData
from gtts import gTTS
@app.route("/")
def index():
    return render_template("index.html", title="Home Page")

@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method=="POST":
        sentence=""
        file=request.files.get("file")
        file_name,file_extension=file.filename.split(".")
        generated_filename=secrets.token_hex(20) + f".{file_extension}"
        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
        file.save(file_location)

        pytesseract.pytesseract.tesseract_cmd="C://Program Files//Tesseract-OCR//tesseract.exe"
        image= cv2.imread(file_location)
        image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        sentence = pytesseract.image_to_string(image_rgb)
        session["sentence"]=sentence
        #print(sentence)
        os.remove(file_location)
        return redirect("/decoded/")

    else:
        return render_template("upload.html",title='Upload')


@app.route("/decoded",methods=["POST","GET"])
def decoded():
    sentence = session.get("sentence")
    form=QRCodeData()
    if request.method=="POST":
        generated_audio=secrets.token_hex(10)+".mp4"
        text_data=form.data_field.data
        translate_to=form.language_field.data
        translated_txt=util.translate_txt(text_data,translate_to)
        print(text_data)
        print("translated",translated_txt)
        form.data_field.data=translated_txt
        tts=gTTS(translated_txt,lang=translate_to)
        file_location=os.path.join(app.config["AUDIO_FILE_UPLOAD"],generated_audio)
        tts.save(file_location)
        return render_template("decoded.html",title="Translation Completed",form=form,audio=True,file=generated_audio)
    else:
        form.data_field.data=sentence
        session["sentence"]=""
        return render_template("decoded.html",title="Translation Incomplete",form=form,audio=False)



from application import app
import fitz
from flask import redirect, render_template, url_for,request,session
import secrets
import os
from . import util
import cv2
import pytesseract
import numpy as np
from .form import QRCodeData
from gtts import gTTS
from flask import send_file
from PIL import Image

@app.route("/")
def index():
    return render_template("index.html", title="Home Page")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Update your upload route
@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        sentence = ""
        file = request.files.get("file")

        if file and allowed_file(file.filename):
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            generated_filename = secrets.token_hex(20) + f".{file_extension}"
            file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)
            file.save(file_location)

            # Extract text from different file formats
            if file_extension == 'pdf':
                text = extract_text_from_pdf(file_location)
            else:
                text = extract_text_from_image(file_location)

            session["sentence"] = text
            os.remove(file_location)
            return redirect("/decoded/")
        else:
            return "Invalid file format. Please upload a valid PDF or image file."

    else:
        return render_template("upload.html", title='Upload')

# Function to extract text from PDF
# Function to extract text from PDF in chunks
# Function to extract text from PDF with images and tables
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(pdf_file)
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Extracting text from text-based elements
        text += page.get_text("text")
        
        # Extracting text from images using Pytesseract OCR
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(image_bytes)
            
            # Perform OCR on the image using Pytesseract
            img_text = pytesseract.image_to_string(image)
            text += img_text
        
        # Clear page data to release memory
        page.clean_contents()
    
    pdf_document.close()
    return text


# Function to extract text from image using PyMuPDF
def extract_text_from_image(file_location):
    sentence = ""
    pytesseract.pytesseract.tesseract_cmd="C://Program Files//Tesseract-OCR//tesseract.exe"
    image = cv2.imread(file_location)
    
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Noise removal - apply GaussianBlur
    denoised_image = cv2.GaussianBlur(thresholded_image, (3, 3), 0)
    
    # Deskew the image
    # You may need to detect the skew angle and then correct it using affine transformation
    
    # OCR on the preprocessed image
    
    sentence = pytesseract.image_to_string(denoised_image)
    session["sentence"]=sentence
    return sentence

@app.route("/decoded",methods=["POST","GET"])
def decoded():
    sentence = session.get("sentence")
    form=QRCodeData()
    if request.method=="POST":
        
        text_data=form.data_field.data
        translate_to=form.language_field.data
        language,confidence=util.detect_language(text_data)
        translated_txt=util.translate_txt(text_data,translate_to)
        print(text_data)
        print("translated",translated_txt)
        form.language=language
        form.translated_field.data=translated_txt
        generated_audio=f"generated_audio_{secrets.token_hex(10)}.mp4"
        tts=gTTS(translated_txt,lang=translate_to)
        file_location=os.path.join(app.config["AUDIO_FILE_UPLOAD"],generated_audio)
        tts.save(file_location)
        translated_txt_filename = f"translated_text_{secrets.token_hex(10)}.txt"
        translated_txt_file_path = os.path.join(app.config["TXT_FILE_UPLOAD"],translated_txt_filename)
        with open(translated_txt_file_path, "w", encoding="utf-8") as file:
            file.write(translated_txt)
            os.remove(file_location)
          
        return render_template("decoded.html",title="Translation Completed",form=form,audio=generated_audio,translated_txt_filename=translated_txt_filename)
    else:
        form.data_field.data=sentence
        session["sentence"]=""
        return render_template("decoded.html",title="Translation Incomplete",form=form,audio=None,translated_txt_filename=None )
    
@app.route("/download/<translated_txt_filename>")
def download_file(translated_txt_filename):
    file_path = os.path.join(app.config["TXT_FILE_UPLOAD"], translated_txt_filename)
    return send_file(file_path, as_attachment=True)

