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