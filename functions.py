from enum import Enum
from tempfile import NamedTemporaryFile

from qrcode import QRCode # type: ignore
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from qrcode.image.pure import PyPNGImage
from qrcode.image.svg import SvgPathImage


class QRCodeErrorCorrection(str, Enum):
    LOW = "L"
    MEDIUM = "M"
    QUARTILE = "Q"
    HIGH = "H"


class QRCodeOutputFormat(str, Enum):
    PNG = "png"
    SVG = "svg"


class QRCodeGenerator():
    """
    _summary_
    """
    @property
    def data(self):
        return getattr(self, "_data") 
    
    @data.setter
    def data(self, value):
        self._data = value

    # Error Correction handlers
    

    @property
    def _error_correction_constants(self):
         return {
             QRCodeErrorCorrection.LOW: ERROR_CORRECT_L,
             QRCodeErrorCorrection.MEDIUM: ERROR_CORRECT_M,
             QRCodeErrorCorrection.QUARTILE: ERROR_CORRECT_Q,
             QRCodeErrorCorrection.HIGH: ERROR_CORRECT_H,
         }
    
    @property
    def error_correction(self):
        return getattr(self, "_error_correction")
    
    @error_correction.setter
    def error_correction(self, value):
        if value not in QRCodeErrorCorrection:
            raise ValueError("Value not in Enum ErrorCorrection")
        
        self._error_correction = value

    def get_error_correction_constant(self):
        return self._error_correction_constants.get(self.error_correction)
    
    # OutputFormat handlers
    @property
    def _output_format_classes(self):
        return {
            QRCodeOutputFormat.PNG: PyPNGImage,
            QRCodeOutputFormat.SVG: SvgPathImage
        }

    @property
    def output_format(self):
        return getattr(self, "_output_format")
    
    @output_format.setter
    def output_format(self, value):
        if value not in QRCodeOutputFormat:
            raise ValueError("Value not in Enum OutputFormat")
        
        self._output_format = value
        
    def get_output_format_class(self):
        return self._output_format_classes.get(self.output_format)
    
    def get_output_format_mimetype(self):
        mime = f'image/{self.output_format.lower()}'

        if self.output_format == QRCodeOutputFormat.SVG:
            mime = f'{mime}+xml'

        return mime

    # Default methods
    def __init__(
        self, 
        data, 
        error_correction=QRCodeErrorCorrection.MEDIUM, 
        output_format=QRCodeOutputFormat.PNG
    ) -> None:
        self.data = data
        self.error_correction = error_correction
        self.output_format = output_format

    def get_img(self):
        qr = QRCode(
            error_correction=self.get_error_correction_constant(),
            image_factory=self.get_output_format_class()
            # box_size=10,
            # border=4,
        )

        qr.add_data(self.data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        return img
    
    async def get_stream(self, chunksize=512):
        with NamedTemporaryFile("w+b", suffix=f".{self.output_format}") as f:
            self.get_img().save(f)

            f.flush()
            f.seek(0)

            while True:
                data = f.read(chunksize)

                if not data:
                    break

                yield data
