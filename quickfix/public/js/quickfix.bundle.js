frappe.ui.form.on("*", {
	refresh(frm) {
		if (frappe.boot.quickfix_shop_name) {
			frm.page.set_title(frappe.boot.quickfix_shop_name);
		}
	},
});

// console.log("QuickFix Desk Script Loaded");
