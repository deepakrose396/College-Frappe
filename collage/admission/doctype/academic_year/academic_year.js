// Copyright (c) 2025, deeps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Year", {
    validate(frm) {
        if (frm.doc.is_current) {  // if current is checked
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Academic Year",
                    filters: {
                        is_current: 1
                    },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        const existing = r.message[0].name;

                        // If existing record is not the current one
                        if (existing !== frm.doc.name) {
                            frappe.msgprint(__("Current academic year already present"));
                            frappe.validated = false; // prevent saving
                        }
                    }
                }
            });
        }
    }
});

