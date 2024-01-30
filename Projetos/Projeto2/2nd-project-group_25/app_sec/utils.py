from io import BytesIO
from base64 import b64encode
from cryptography.fernet import Fernet

import qrcode

def get_b64encoded_qr_image(data):
    """
    Converts data into encoded QR image.

    Parameters:
    data (bytes|str): Raw data to be encoded as QR image.

    Returns:
    str: QR image.
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)
    return b64encode(buffered.getvalue()).decode("utf-8")
