from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Upload your PDF to /uploadpdf"}

@app.post("/uploadpdf/")
async def create_upload_file(file: UploadFile = File(...)):
    pdfFileObj = await file.read()  # creating a pdf file object
    images = convert_from_bytes(pdfFileObj)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Correct location for Docker

    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)

    return {"filename": file.filename, "content": text}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
