# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class JobCard(Document):
	def validate(self):
		self.validate_phone()
		self.validate_technician()
		self.calculate_total_price()
		self.get_labour_charge()
	
	def before_submit(self):
		self.check_quantity()
		self.check_ready_for_delivery()
	
	def on_submit(self):
		self.update_stock()
		self.create_service_invoice()
		self.job_ready_notification()
		self.send_customer_mail()


	def validate_phone(self):
		if len(str(self.customer_phone)) != 10:
			frappe.throw("Phone number must be 10 digits long.")
	
	def validate_technician(self):
		if self.status=="In Repair" and not self.assigned_technician:
			frappe.throw("Technician not assigned yet")
	
	def calculate_total_price(self):
		sum=0
		for row in self.parts_used:
			row.total_price=row.quantity*row.unit_price
			sum+=row.total_price
		self.parts_total=sum
	
	def get_labour_charge(self):
		self.labour_charge=frappe.db.get_single_value("Quickfix Settings","default_labour_charge")
		self.final_amount=self.parts_total+self.labour_charge
	
	def check_ready_for_delivery(self):
		if self.status!="Ready for Delivery":
			frappe.throw("Job Card id not ready for delivery yet.")
	
	def check_quantity(self):
		for row in self.parts_used:
			qty=frappe.db.get_value("Spare Part", row.part,"stock_quantity")
			if(row.quantity>qty):
				frappe.throw(f"{row.part} only {qty} quantity available")
	
	def update_stock(self):
		for row in self.parts_used:
			qty=frappe.db.get_value("Spare Part", row.part,"stock_quantity")
			new_qty=qty-row.quantity
			frappe.db.set_value("Spare Part", row.part, "stock_quantity", new_qty)
		#ignore_permissions=True is not neccessary because frappe.db.set_value() doesn't check permissions, it directly update in database.
		#But if we use frappe.set_value() it checks permission and we need to use 
	
	def create_service_invoice(self):
		frappe.get_doc({
			"doctype": "Service Invoice",
			"job_card": self.name,
			"invoice_date": nowdate(),
			"labour_charge": self.labour_charge,
			"parts_total": self.parts_total,
			"total_amount": self.final_amount,
		}).insert(ignore_permissions=True)
	
	def job_ready_notification(self):
		frappe.publish_realtime(
			"job_ready",
			{
				"message": f"Job Card {self.name} is ready for delivery.",
			},
			user=self.owner
		)
	def send_customer_mail(self):
		frappe.enqueue("quickfix.api.job_ready_email",
				  job_card_name=self.name,
				  queue="short",
				  timeout=300)
	
	def on_cancel(self):
		frappe.db.set_value("Job Card", self.name, "status", "Cancelled")
		self.revert_stock()
		self.cancel_service_invoice()
	
	def revert_stock(self):
		for row in self.parts_used:
			qty=frappe.db.get_value("Spare Part", row.part,"stock_quantity")
			new_qty=qty+row.quantity
			frappe.db.set_value("Spare Part", row.part, "stock_quantity", new_qty)
	
	def cancel_service_invoice(self):
		doc=frappe.db.get_value("Service Invoice", {"job_card": self.name}, "name")
		if doc:
			service_invoice=frappe.get_doc("Service Invoice",doc)
			if service_invoice.docstatus==1:
				service_invoice.cancel()
			# elif service_invoice.docstatus==0:
			# 	service_invoice.submit()
			# 	service_invoice.cancel()

	def on_trash(self):
		if self.status!="Cancelled" and self.status!="Draft":
			frappe.throw("Cannot delete this Job Card")
			
	# def on_update(self):
	# 	self.save()