
import frappe
from frappe.model.document import Document

class EmailSent(Document):
    def before_save(self):
        try:
           
            if not frappe.db.exists("User", self.email):
               
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": self.email,
                    "first_name": self.first_name,
                    "send_welcome_email": 1,
                    "roles": [
                        {
                            "role": "DBCY-ADMIN"
						}
					] 
                })
                user.insert()
                frappe.db.commit()
                frappe.msgprint(f"User {self.first_name} created successfully!")
            else:
                frappe.msgprint(f"User with email {self.email} already exists.")
        except Exception as e:
            frappe.throw(f"Error while creating user: {str(e)}")
