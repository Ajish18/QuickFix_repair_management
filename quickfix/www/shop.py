import frappe
from quickfix.utils import get_shop_name

def get_context(context):
    context.shop_name = get_shop_name()
    context.message = "Welcome to our service center"