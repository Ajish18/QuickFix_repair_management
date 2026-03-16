import frappe

from quickfix.service_center.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):
	def validate(self):
		super().validate()  # ALWAYS call super first
		# print("Custom validate called")
		self._check_urgent_unassigned()

	def _check_urgent_unassigned(self):
		if self.priority == "Urgent" and not self.assigned_technician:
			settings = frappe.get_single("Quickfix Settings")
			frappe.enqueue(
				"quickfix.api.send_urgent_alert", job_card=self.name, manager=settings.manager_email
			)

	# MRO-Method Resolution Order it searches for the class where the method is defined.
	# eg. class A:
	#       def test(self):
	#   class B(A):
	#       pass
	# b=B()
	# b.test() it will call test method of class B.
