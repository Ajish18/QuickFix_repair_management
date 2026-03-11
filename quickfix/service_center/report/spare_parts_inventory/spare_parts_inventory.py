# Copyright (c) 2026, ajish and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data()
	summary=get_summary(data)
	return columns, data, None, None, summary

def get_columns():
	return [
		{
			"label": _("Part Name"),
			"fieldname": "part_name",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Part Code"),
			"fieldname": "part_code",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Device Type"),
			"fieldname": "compatible_device_type",
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"label": _("Stock Qty"),
			"fieldname": "stock_quantity",
			"fieldtype": "Int",
			"width": 150,
		},
		{
			"label": _("Reorder Level"),
			"fieldname": "reorder_level",
			"fieldtype": "Int",
			"width": 150,
		},
		{
			"label": _("Unit Price"),
			"fieldname": "unit_cost",
			"fieldtype": "Currency",
			"width": 150,
		},
		{
			"label": _("Margin %"),
			"fieldname": "margin",
			"fieldtype": "Percent",
			"width": 150,
		},
		{
			"label":_("Total Value"),
			"fieldname": "total_value",
			"fieldtype": "Currency",
			"width":150
		}
	]


def get_data():
	data=frappe.get_list("Spare Part",
					  [
						  "part_name",
						  "part_code",
						  "compatible_device_type",
						  "stock_quantity",
						  "reorder_level",
						  "unit_cost",
						  "selling_price",
					  ])
	for i in data:
		if(i["selling_price"]):
			margin=(i["selling_price"]-i["unit_cost"])/i["selling_price"] * 100
		else:
			margin=0
		total_value=i["stock_quantity"]*i["unit_cost"]
		i["total_value"]=total_value
		i["margin"]=margin
	return data

def get_summary(data):
	total_parts=0
	below_order=0
	total_inventory_value=0
	for i in data:
		total_parts+=i["stock_quantity"]
		if(i["stock_quantity"]<i["reorder_level"]):
			below_order+=1
		total=i["stock_quantity"]*i["unit_cost"]
		total_inventory_value+=total
	
	return[
		{
			"label":"Total Parts",
			"value": total_parts
		},
		{
			"label":"Below Order",
			"value":below_order
		},
		{
			"label":"Total Inventory Value",
			"value":total_inventory_value
		}
	]