# my_app/api/user.py
import frappe

@frappe.whitelist()
def get_current_user():
    user = frappe.get_doc("User", frappe.session.user)
    return {
        "name": user.name,
        "email": user.email,
        "first_name": user.first_name,
        "roles": frappe.get_all("Has Role", filters={"parent": user.name}, pluck="role"),
    }
