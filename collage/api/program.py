# collage/api/program.py
import frappe

@frappe.whitelist(allow_guest=True)
def get_programs():
    return frappe.get_all(
        "Program List",
        fields=["name", "program_name", "duration"]
    )
