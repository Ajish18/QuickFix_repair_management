import frappe

@frappe.whitelist()
def get_job_summary():
    return {
        "message": "Hello from QuickFix",
        "status": "Working"
    }