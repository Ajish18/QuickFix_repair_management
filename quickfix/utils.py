import frappe
import qrcode
import base64
from io import BytesIO

def get_shop_name():
    settings = frappe.get_single("Quickfix Settings")
    return settings.shop_name

def filter_job_id(value):
    return f"JOB#{value}"

def generate_qr(data):
    img=qrcode.make(data)
    buffer=BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


