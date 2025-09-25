# Copyright (c) 2025, deeps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentApplicant(Document):
	def before_save(self):
		if self.paid == 1:
			self.status = "Applied"
		elif self.paid == 0:
			self.status = "Payment Pending"
