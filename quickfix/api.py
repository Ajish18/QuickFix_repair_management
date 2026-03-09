import frappe


@frappe.whitelist()
def get_job_summary():
    return {
        "message": "Hello from QuickFix",
        "status": "Working"
    }

@frappe.whitelist()
def share_job_card(job_card_name, user_email):

    frappe.share.add(
        doctype="Job Card",
        name=job_card_name,
        user=user_email,
        read=1,
        write=0,
        share=0
    )
    return f"Job Card {job_card_name} shared with {user_email}"

@frappe.whitelist()
def qf_manager_acess():
    frappe.only_for("QF Manager")


@frappe.whitelist()
def error_test():
    return 1/0

@frappe.whitelist()
def test_permission(job_card_name):
    doc=frappe.get_doc("Job Card", job_card_name)
    doc.check_permission("read")
    return doc.as_dict()

from frappe.query_builder import DocType
from datetime import timedelta
@frappe.whitelist()
def get_overdue_jobs():

    JC = DocType("Job Card")

    seven_days_ago = frappe.utils.now_datetime() - timedelta(days=1)

    result = (
        frappe.qb.from_(JC)
        .select(
            JC.name,
            JC.customer_name,
            JC.assigned_technician,
            JC.creation
        )
        .where(
            (JC.status.isin(["Pending Diagnosis", "In Repair"])) &
            (JC.creation < seven_days_ago)
        )
        .orderby(JC.creation, order=frappe.qb.asc)
        .run(as_dict=True)
    )

    return result

@frappe.whitelist()
def transfer_job(from_tech, to_tech):
    try:
        frappe.db.sql("""
            UPDATE `tabJob`
            SET assigned_technician = %s
            WHERE assigned_technician = %s
            AND status IN ('Pending Diagnosis', 'In Repair')
        """, (to_tech, from_tech))
        frappe.db.commit()
        return "Transfer successful"

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
            message=str(e),
            title="Transfer Job Failed"
        )
        raise

@frappe.whitelist()
def get_job_cards_unsafe():
    return frappe.get_all(
        "Job Card",
        fields="*"
    )

@frappe.whitelist()
def get_job_cards_safe():
    user = frappe.session.user

    records = frappe.get_list(
        "Job Card",
        fields=[
            "name",
            "customer_name",
            "device_type",
            "status",
            "payment_status",
            "customer_phone",
            "customer_email"
        ]
    )

    # Managers see everything
    if "QF Manager" in frappe.get_roles(user):
        return records

    # Others → hide sensitive fields
    for r in records:
        r.pop("customer_phone", None)
        r.pop("customer_email", None)

    return records

def job_ready_email(job_card_name):
    job_card=frappe.get_value(
        "Job Card",
        job_card_name,
        ["customer_email","customer_name","device_type"],
        as_dict=True
        )
    frappe.sendmail(
        recipients=job_card.customer_email,
        subject=(f"Your device is ready for delivery - Job Card {job_card.name}"),
        message=(f"""Dear {job_card.customer_name},
                 <br><br>Your {job_card.device_type} has been repaired and is ready for pickup.
                 <br><br>Thank you for choosing our service!<br><br>
                 Best regards,
                 <br>QuickFix Service Center""")
    )

def send_urgent_alert(job_card, manager):
    frappe.sendmail(
        recipients=manager,
        subject=f"Urgent Alert: Job Card {job_card} is unassigned",
        message=f"""Dear Manager,
                 <br><br>Job Card {job_card} has been marked as Urgent but is currently unassigned.
                 <br><br>Please assign a technician as soon as possible to avoid delays.
                 <br><br>Best regards,<br>QuickFix System"""    
    )

@frappe.whitelist()
def custom_get_count(doctype, filters=None, debug=False, cache=False):
    log = frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doctype,
        "action": "count_queried",
        "user": frappe.session.user
    })

    log.insert(ignore_permissions=True)
    frappe.db.commit()

    from frappe.client import get_count
    return get_count(doctype, filters, debug, cache)

# Property setter
def property_setter():
    print("Property setter")
    frappe.make_property_setter({
        "doctype": "Job Card",
        "fieldname": "remarks",
        "property": "bold",
        "value": 1,
        "property_type": "Check"
    })