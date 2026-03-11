// Copyright (c) 2026, ajish and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && column.fieldname === "stock_quantity" && data.stock_quantity <= data.reorder_level) {
			value = `<span style="background-color:red; color:white; display:block;">${value}</span>`;
		}
		
		return value;
	}
};