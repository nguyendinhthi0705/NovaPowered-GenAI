from io import BytesIO
import base64

class ImageProcessor:
    """Handles image processing operations"""
    
    @staticmethod
    def get_bytesio_from_bytes(image_bytes):
        image_io = BytesIO(image_bytes)
        return image_io
        
    @staticmethod
    def get_base64_from_bytes(image_bytes):
        resized_io = BytesIO(image_bytes)
        img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
        return img_str
        
    @staticmethod
    def get_bytes_from_file(file_path):
        with open(file_path, "rb") as image_file:
            file_bytes = image_file.read()
        return file_bytes