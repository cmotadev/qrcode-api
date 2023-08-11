from importlib.metadata import version

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from schemas import URLInput, TextInput, EmailInput
from functions import QRCodeGenerator, QRCodeErrorCorrection, QRCodeOutputFormat


async def get_qrcode(
    data, 
    error_correction: QRCodeErrorCorrection = QRCodeErrorCorrection.MEDIUM,
    output_format: QRCodeOutputFormat = QRCodeOutputFormat.PNG
):
    qr = QRCodeGenerator(data, error_correction, output_format)
    return StreamingResponse(qr.get_stream(), media_type=qr.get_output_format_mimetype())    


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/qrcode")
async def qrcode_version():
    qrcode = "qrcode"
    return {qrcode: version(qrcode)}

@app.post("/qrcode/from-text")
async def qrcode_from_text(
    data: TextInput, 
    error_correction: QRCodeErrorCorrection = QRCodeErrorCorrection.MEDIUM,
    output_format: QRCodeOutputFormat = QRCodeOutputFormat.PNG
):    
    return await get_qrcode(data.text, error_correction, output_format)


@app.post("/qrcode/from-url")
async def qrcode_from_url(
    data: URLInput, 
    error_correction: QRCodeErrorCorrection = QRCodeErrorCorrection.MEDIUM,
    output_format: QRCodeOutputFormat = QRCodeOutputFormat.PNG
):    
    return await get_qrcode(data.url, error_correction, output_format)

@app.post("/qrcode/from-email")
async def qrcode_from_email(
    data: EmailInput, 
    error_correction: QRCodeErrorCorrection = QRCodeErrorCorrection.MEDIUM,
    output_format: QRCodeOutputFormat = QRCodeOutputFormat.PNG
):    
    return await get_qrcode(data.email, error_correction, output_format)
