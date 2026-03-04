# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QuickfixSettings(Document):
	def on_update(self):
		# doc = frappe.get_doc("QuickFix Settings", "QuickFix Settings")
		# threshold = doc.low_stock_alert_enabled
		threshold = frappe.db.get_single_value("QuickFix Settings", "low_stock_alert_enabled")
		# print("Threshold value:", threshold)
