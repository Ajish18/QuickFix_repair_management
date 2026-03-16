# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QuickfixSettings(Document):
	pass


@frappe.whitelist()
def enque_monthly_report():
	frappe.enqueue("quickfix.utils.generate_monthly_revenue_report", queue="long", timeout=600)
	frappe.msgprint("Job enqueued")
	return "Report starts generating"
