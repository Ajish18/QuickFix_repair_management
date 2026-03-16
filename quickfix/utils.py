import base64
import json
from io import BytesIO

import frappe
import qrcode
from frappe.utils import add_months, get_first_day, get_last_day, getdate, now, today


def get_shop_name():
	settings = frappe.get_single("Quickfix Settings")
	return settings.shop_name


def filter_job_id(value):
	return f"JOB#{value}"


def generate_qr(data):
	img = qrcode.make(data)
	buffer = BytesIO()
	img.save(buffer, format="PNG")
	return base64.b64encode(buffer.getvalue()).decode()


def check_low_stock():
	frappe.log_error("Scheduler Started", "Low Stock Test")
	last_run = frappe.db.get_value(
		"Audit Log", {"action": "low_stock_check", "timestamp": ["like", today() + "%"]}, "name"
	)
	if last_run:
		frappe.log_error("Already ran today")
		return

	low_stock_items = frappe.get_all(
		"Spare Part", filters={"stock_quantity": ["<", 5]}, fields=["name", "stock_quantity"]
	)

	for item in low_stock_items:
		frappe.log_error(f"Low stock: {item.name}, Quantity: {item.stock_quantity}")

	frappe.get_doc(
		{"doctype": "Audit Log", "action": "low_stock_check", "timestamp": frappe.utils.now()}
	).insert(ignore_permissions=True)

	frappe.db.commit()


def generate_monthly_revenue_report():
	report = frappe.get_doc("Report", "Monthly Revenue Report")
	instance = frappe.get_doc(
		{"doctype": "Prepared Report", "report_name": report.name, "status": "Queued", "filters": "{}"}
	)

	instance.insert(ignore_permissions=True)
	frappe.enqueue(
		"frappe.core.doctype.prepared_report.prepared_report.generate_report",
		queue="long",
		prepared_report=instance.name,
	)


def fail_background_job():
	frappe.log_error("Testing job failure", "Job Failure Test")
	raise Exception("This is a deliberate job failure for testing")


def cancel_old_draft_jobcard():
	frappe.db.sql("""update `tabJob Card` set status="Cancelled" where docstatus=0 Limit 1000""")
	frappe.db.commit()


def create_bulk_audit_log():
	log = []
	for i in range(100):
		log.append(
			(
				f"AUDITS-{i}",  # name
				"Job Card",  # doctype_name
				f"JOB-{i}",  # document_name
				"bulk_insert",  # action
				"Administrator",  # user
				now(),  # timestamp
			)
		)

	frappe.db.bulk_insert(
		"Audit Log",
		fields=["name", "doctype_name", "document_name", "action", "user", "timestamp"],
		values=log,
	)

	frappe.db.commit()
