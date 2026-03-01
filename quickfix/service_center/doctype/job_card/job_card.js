// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Card", {
	onload(frm) {
        if(frm.is_new() || !frm.doc.labour_charge){
            labour_charge=frappe.db.get_single_value("Quickfix Settings", "default_labour_charge")
            .then((value) => {
                frm.set_value("labour_charge", value);
            });
        }
	},
});
