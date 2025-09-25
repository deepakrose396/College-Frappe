import frappe

@frappe.whitelist(allow_guest=True)
def get_departments():
    return frappe.get_all(
        "Department",
        fields=["name", "department", "fees", "program"]
    )
