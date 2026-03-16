import frappe
from frappe.utils import add_months, get_first_day, get_last_day, today


def execute(filters=None):

	first_day = get_first_day(add_months(today(), -1))
	last_day = get_last_day(add_months(today(), -1))

	columns = [
		{
			"label": "Invoice",
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Service Invoice",
			"width": 150,
		},
		{"label": "Customer", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
		{"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 150},
		{"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 150},
	]

	data = frappe.db.sql(
		"""
        SELECT
            name,
            customer_name,
            total_amount,
            invoice_date
        FROM `tabService Invoice`
        WHERE
            docstatus = 1
            AND payment_status = 'Paid'
            AND invoice_date BETWEEN %s AND %s
    """,
		(first_day, last_day),
		as_dict=True,
	)

	total_revenue = sum(d["total_amount"] for d in data)

	summary = [{"value": total_revenue, "label": "Total Revenue", "datatype": "Currency"}]

	return columns, data, None, None, summary
