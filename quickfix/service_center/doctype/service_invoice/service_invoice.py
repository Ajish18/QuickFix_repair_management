# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	def before_submit(self):
		if self.payment_status=="Unpaid":
			frappe.throw("Status must be paid, to submit the payment")
