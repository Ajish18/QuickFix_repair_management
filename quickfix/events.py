import frappe

def validate_technician(doc,method):
		if doc.status=="In Repair" and not doc.assigned_technician:
			frappe.throw("Technician not assigned yet")