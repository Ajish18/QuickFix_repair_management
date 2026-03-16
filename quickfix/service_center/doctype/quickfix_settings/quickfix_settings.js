// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quickfix Settings", {
	refresh(frm) {
		frm.add_custom_button("Monthly report", function () {
			frappe.call({
				method: "quickfix.service_center.doctype.quickfix_settings.quickfix_settings.enque_monthly_report",
				callback: function (r) {
					frappe.msgprint("Report generation started in background");
				},
			});
		});
	},
});
