import frappe


def validate_technician(doc, method):
	if doc.status == "In Repair" and not doc.assigned_technician:
		frappe.throw("Technician not assigned yet")


def log_login(login_manager):
	frappe.get_doc({"doctype": "Audit Log", "user": frappe.session.user, "action": "Login"}).insert(
		ignore_permissions=True
	)


def log_logout(login_manager):
	frappe.get_doc({"doctype": "Audit Log", "user": frappe.session.user, "action": "Logout"}).insert(
		ignore_permissions=True
	)
