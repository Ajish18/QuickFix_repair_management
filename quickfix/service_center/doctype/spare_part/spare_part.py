# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SparePart(Document):
	def autoname(self):
		id=self.part_code.upper() +frappe.model.naming.make_autoname("-PART-.YYYY-.####")
		self.name = id
	def validate(self):
		if self.selling_price < self.unit_cost:
			frappe.throw("Selling Price should be greater than Unit Cost")
