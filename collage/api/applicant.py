import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def submit_student_applicant(first_name, last_name, email, phone, department, program, paid, academic_year):
    status = ""
    if (paid == 1):
            status = "Applied"
    elif (paid == 0):
        status = "Payment Pending"
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
            "academic_year": academic_year,
            "status":status
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


@frappe.whitelist()
def get_applicants():
    """Fetch all applicants"""
    user_email = frappe.session.user
    if user_email == "Guest":
        frappe.throw(_("You must be logged in to access this data"))

    applicants = frappe.db.get_all(
        "Student Applicant",
        fields=["first_name", "last_name", "email", "phone", "department", "program", "paid", "academic_year","status","name"],
    )

    if not applicants:
        frappe.throw(_("No applicant records found for {0}").format(user_email))

    return applicants


@frappe.whitelist()
def update_applicant(email, status):
    """Update the applicant status"""
    try:
        applicant_list = frappe.get_all("Student Applicant", filters={"email": email}, limit=1)
        if not applicant_list:
            frappe.throw(_("Applicant not found"))

        applicant_doc = frappe.get_doc("Student Applicant", applicant_list[0].name)
        print("Before status changed", applicant_doc.status)

        # Use set to mark as changed
        applicant_doc.set("status", status)
        print("After status changed", applicant_doc.status)

        applicant_doc.save()  # Administrator user, no ignore_permissions needed
        frappe.db.commit()

        print("After db commit", applicant_doc.status)
        if applicant_doc.status == "Selected":
            # Create Student record
            if not frappe.db.exists("Student", {"email": email}):
                student = frappe.get_doc({
                    "doctype": "Student",
                    "first_name": applicant_doc.first_name,
                    "last_name": applicant_doc.last_name,
                    "email": applicant_doc.email,
                    "phone": applicant_doc.phone,
                    "department": applicant_doc.department,
                    "program": applicant_doc.program,
                    "academic_year": applicant_doc.academic_year,
                    "application_date": applicant_doc.application_date
                })
                student.insert()
                frappe.db.commit()
                frappe.get_doc("User", email).add_roles("Student")
                return {"message": "Applicant status updated successfully and student record created"}
        return {"message": "Applicant status updated successfully"}

    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="Update Applicant Status Failed")
        return {"message": f"Failed to update applicant status: {str(e)}"}
