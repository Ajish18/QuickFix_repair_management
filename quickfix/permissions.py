import frappe

def job_card_query(user):
    roles = frappe.get_roles(user)
    if "System Manager" in roles or user == "Administrator":
        return
    if "QF Technician" in roles:
        return f"""
        `tabJob Card`.assigned_technician IN (
            SELECT name FROM `tabTechnician`
            WHERE user = '{user}'
        )
        """
    return ""

import frappe
def has_permission(doc, user=None, permission_type=None):
    user = user or frappe.session.user
    if "QF Manager" in frappe.get_roles(user):
        return True
    if doc.job_card:
        payment_status = frappe.db.get_value(
            "Job Card",
            doc.job_card,
            "payment_status"
        )
        if payment_status != "Paid":
            return False
    return True