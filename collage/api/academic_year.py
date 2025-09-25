import frappe


@frappe.whitelist(allow_guest = True)
def get_academic():
    return frappe.get_all(
        "Academic Year",
        fields=["name","academic_year"],
        filters={'is_current': '1'}
    )