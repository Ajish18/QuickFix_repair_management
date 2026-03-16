import frappe


def before_uninstall():
	count = frappe.db.count("Job Card", {"docstatus": 1})
	if count > 0:
		frappe.throw("Submitted Jobcards exist. Please Cancel to Uninstall the app.")
