import frappe


def after_install():

	device_types = frappe.get_list(
		"Device Type",
	)

	for device in device_types:
		if not frappe.db.exists("Device Type", device):
			frappe.get_doc({"doctype": "Device Type", "device_type": device}).insert(ignore_permissions=True)

	if not frappe.db.exists("QuickFix Settings", "QuickFix Settings"):
		frappe.get_doc(
			{
				"doctype": "QuickFix Settings",
				"shop_name": "QuickFix Repair Center",
				"manager_email": "admin@quickfix.com",
				"default_labour_charge": 500,
				"low_stock_alert_enabled": 1,
			}
		).insert(ignore_permissions=True)

	frappe.msgprint("QuickFix app installed successfully")
