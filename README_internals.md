B2
Part A
frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) 
    - It list all the tables that contain word job.
    - [{'Field': 'name',
        'Type': 'varchar(140)',
        'Null': 'NO',
        'Key': 'PRI',
        'Default': None,
        'Extra': ''},
        {'Field': 'creation',
        'Type': 'datetime(6)',
        'Null': 'YES',
        'Key': 'MUL',
        'Default': None,
        'Extra': ''},]
        Tab prefix - In frappe all the doctypes are stored in db with the name prefix tab example tabJob Card.
frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True)
    column names- customer name, customer_email, customer_phone, alternate_phone_no,
                  device_type