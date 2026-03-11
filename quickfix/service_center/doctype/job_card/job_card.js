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
    setup(frm) {
        frm.set_query("assigned_technician", function () {
            return {
                filters: {
                    status: "Active",
                    specialization: frm.doc.device_type
                }
            };
        });
    },
    // colur code
    refresh(frm){
        if (frm.doc.status === "Open") {
            frm.dashboard.add_indicator("Open", "yellow");
        }
        if(frm.doc.status === "In Repair") {
            frm.dashboard.add_indicator("In Repair", "blue");
        }
        if(frm.doc.status === "Pending Diagnosis") {
            frm.dashboard.add_indicator("Pending Diagnosis", "red");
        }
        if (frm.doc.status === "Ready for Delivery") {
            frm.dashboard.add_indicator("Ready for Delivery", "orange");
        }
        if (frm.doc.status === "Delivered") {
            frm.dashboard.add_indicator("Delivered", "green");
        }
        // delivered button
        if (frm.doc.status === "Ready for Delivery" && frm.doc.docstatus===1){
            frm.add_custom_button("Mark as Delivered", function(){
                frappe.call({
                    method: "quickfix.service_center.doctype.job_card.job_card.mark_as_delivered",
                    args: {
                        job_card_name: frm.doc.name
                    },
                    callback: function() {
                        frappe.msgprint("Job marked as delivered.");
                        frm.reload_doc();
                    }
                })
            })
        }
        // shop name
        if (frappe.boot.quickfix_shop_name) {

            frm.set_intro("Shop: " + frappe.boot.quickfix_shop_name);

        }
        frm.add_custom_button("Reject Job", function() {
            let dialog = new frappe.ui.Dialog({
                title: "Reject Job",
                fields: [
                    {
                        label: "Rejection Reason",
                        fieldname: "reason",
                        fieldtype: "Small Text",
                        reqd: 1
                    }
                ],
                primary_action_label: "Reject",
                primary_action(values) {
                    frappe.msgprint("Job rejected: " + values.reason);
                    dialog.hide();
                }
            });
            dialog.show();
        });
        if(frm.doc.docstatus != 1){
        frm.add_custom_button("Transfer Technician", function () {
        frappe.prompt(
            [
                {
                    label: "New Technician",
                    fieldname: "technician",
                    fieldtype: "Link",
                    options: "Technician",
                    reqd: 1,
                }
            ],
        function (values) {
            frappe.confirm("Are you sure you want to transfer technician?", function () {
                frappe.call({
                    method: "quickfix.service_center.doctype.job_card.job_card.transfer_technician",
                    args: {
                        job_card_name: frm.doc.name,
                        technician: values.technician
                    },
                    callback: function () {
                        frm.set_value("assigned_technician", values.technician);
                        frm.trigger("assigned_technician");
                        frm.reload_doc()
                    }
                });
            });
        },
        "Transfer Technician",
        "Transfer"
    );
    });
        }
    
    },

    device_type(frm) {
        if (frm.doc.assigned_technician) {
            frappe.db.get_value("Technician", frm.doc.assigned_technician,"specialization").then((r) => {
                if(r.specialization !== frm.doc.device_type){
                    frappe.msgprint("Selected technician does not specialize in the device type.");
                    frm.set_value("assigned_technician", null);
                }
            });
        }
        else{
            return;
        }
    },
    onload(frm) {
        frappe.realtime.on("job_ready", (data) => {
            frappe.show_alert(data.message, 5);
        });
    },
    // validate(frm){
    //     console.log("1 server response received");
    //     frappe.call({
    //         method: "quickfix.service_center.doctype.job_card.job_card.check_validate",
    //         args: {
    //             job: frm.doc.name
    //         },
    //         callback: function(r) {
    //             console.log("3server response received");
    //             if (!r.message) {
    //                 frappe.msgprint("Invalid job card.");
    //             }
    //         }
    //     });
    //     console.log("2 validate finished");
    // }
    assigned_technician(frm) {
        if (frm.doc.assigned_technician) {
            frappe.db.get_doc("Technician", frm.doc.assigned_technician)
                .then((tech) => {
                    if (tech.specialization !== frm.doc.device_type) {
                        frappe.msgprint("Technician specialization does not match device type");
                        frm.set_value("assigned_technician", null);
                    }
                });
        }

    }
});
frappe.ui.form.on("Part Usage Entry", {
    quantity(frm,cdt,cdn){
        calculate_amount(frm,cdt,cdn);
    },
    part(frm,cdt,cdn){
        calculate_amount(frm,cdt,cdn);
    }
});

function calculate_amount(frm,cdt,cdn){
    let row = locals[cdt][cdn];
    if(row.quantity && row.unit_price){
        let total_price = row.quantity * row.unit_price;
        frappe.model.set_value(cdt, cdn, "total_price", total_price);
    }
}