import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def submit_student_applicant(first_name, last_name, email, phone, department, program, paid, academic_year):
    try:
        # Create Student Applicant
        student_doc = frappe.get_doc({
            "doctype": "Student Applicant",
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "department": department,
            "program": program,
            "paid": paid,
            "academic_year": academic_year
        })
        student_doc.insert(ignore_permissions=True)

        # Create User if not exists
        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "send_welcome_email": 1,
                "roles": [
                    {"role": "Applicant"}
                ]
            })
            user.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "success": True,
            "message": "Student Applicant submitted successfully. Welcome email sent to applicant.",
            "data": student_doc.name
        }

    except Exception as e:
        # Rollback DB changes if error
        frappe.db.rollback()

        # Log error for debugging
        frappe.log_error(message=frappe.get_traceback(), title="Student Applicant Submission Failed")

        return {
            "success": False,
            "message": f"Failed to submit application: {str(e)}"
        }


@frappe.whitelist()
def get_my_applicant():
    """Fetch only the logged-in user's applicant record"""
    user_email = frappe.session.user
    if user_email == "Guest":
        frappe.throw(_("You must be logged in to access this data"))

    applicant = frappe.db.get_value(
        "Student Applicant",
        {"email": user_email},
        ["first_name", "last_name", "email", "phone", "department", "program", "paid", "academic_year","status"],
        as_dict=True,
    )

    if not applicant:
        frappe.throw(_("No applicant record found for {0}").format(user_email))

    return applicant


@frappe.whitelist()
def update_my_applicant(data: dict):
    """Update the logged-in user's applicant record"""
    import json
    if isinstance(data, str):
        data = json.loads(data)

    user_email = frappe.session.user
    if user_email == "Guest":
        frappe.throw(_("You must be logged in to update your data"))

    doc = frappe.get_doc("Student Applicant", {"email": user_email})

    for field, value in data.items():
        if hasattr(doc, field):
            setattr(doc, field, value)

    doc.save(ignore_permissions=False)
    frappe.db.commit()

    return {"message": "Profile updated successfully"}