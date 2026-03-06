import frappe

def get_shop_name():
    settings = frappe.get_single("Quickfix Settings")
    return settings.shop_name

def filter_job_id(value):
    return f"JOB#{value}"