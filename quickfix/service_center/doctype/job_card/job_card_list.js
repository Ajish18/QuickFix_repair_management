frappe.listview_settings["Job Card"] = {
    add_fields: ["status", "final_amount", "priority"],
    has_indicator_for_draft: true,
    get_indicator: function(doc) {
        let colour_map = {
            "Pending Diagnosis":["Pending Diagnosis", "orange"],
            "Awaiting Customer Approval":["Awaiting Customer Approval", "yellow"],
            "In Repair":["In Repair", "pink"],
            "Ready for Delivery":["Ready for Delivery", "blue"],
            "Delivered":["Delivered", "green"],
            "Cancelled":["Cancelled", "red"]
        };
        return colour_map[doc.status];
    },
    button: {
        show: function(doc) {
            return doc.status === "In Repair";
        },
        get_label: function() {
            return "Mark Ready";
        },
        get_description: function() {
            return "Mark this job card as Ready for Delivery";
        },
        action: function(doc) {
            frappe.call({
                method: "quickfix.service_center.doctype.job_card.job_card.mark_ready_for_delivery",
                args: { job_card: doc.name },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.show_alert({
                            message: doc.name + " marked as Ready for Delivery",
                            indicator: "green"
                        });
                        frappe.model.reload_doc("Job Card", doc.name)
                        cur_list.refresh();
                    }
                }
            });
        }
    },
    formatters: {
        final_amount: function(value, df, doc) {
            return format_currency(value, "INR");
        },
        priority: function(value, df, doc) {
            let colour_map = {
                "Normal": "orange",
                "High":   "red",
                "Urgent": "green"
            };
            let color = colour_map[value];
            return `<span style="color:${color}; font-weight:bold;">${value}</span>`;
        }
    },
};