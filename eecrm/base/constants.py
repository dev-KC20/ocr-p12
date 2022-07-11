""" constants values used by eecrm that are less sensitive in regards of data security


"""
from rest_framework.permissions import SAFE_METHODS
from datetime import datetime
import zoneinfo

API_VERSION = "1"
PHONE_NOT_VALID = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
HELLO_WORLD = "* ***  Hello, it all starts here *** *"
SOMETHING_WRONG = "Something went wrong-please try again"
TYPE_ERROR = "Type error, pls check."
INDEX_ERROR = "Index error, pls check."
KEY_ERROR = "Key error, pls check."
# admin site for employee creation & update
ADMIN_SITE_HEADER = "Epic Event CRM Admin Panel"
ADMIN_SITE_TITLE = "EE crm"
ADMIN_SITE_INDEX_TITLE = "Employee CRUD"
# User & Employee model
APPS_VERBOSE_NAME = "Employees"
USER_EXTERNAL = "E"
USER_SALES = "S"
USER_SUPPORT = "A"
USER_MANAGEMENT = "M"
EMPLOYEEE_DEPARTMENT = [
    (USER_EXTERNAL, "Partenaire"),
    (USER_SALES, "Commercial"),
    (USER_SUPPORT, "Assistance"),
    (USER_MANAGEMENT, "Gestion"),
]
SALES_ENABLED_DEPARTMENT = [USER_SALES, USER_MANAGEMENT]
SUPPORT_ENABLED_DEPARTMENT = [USER_SUPPORT, USER_MANAGEMENT]
# request check
EDIT_DELETE_METHODS = ["PUT", "PATCH", "DELETE"]
EDIT_METHODS = ["PUT", "PATCH"]
CREATE_METHODS = ["POST"]
READ_METHODS = SAFE_METHODS
# logging
SERVER_LOGGER = "eecrm"
# testing
TEST_COMPANY_NAME_1 = "The great loop"
TEST_CONTRACT_NAME_1 = "The blue contract"
TEST_CONTRACT_AMOUNT = 125
TEST_USERNAME_SALES = "johncherokee"
TEST_USERNAME_CLIENT = "mollymallone"
TEST_SECRET_PASSWORD = "thetopsecretpass"
# TEST_USER_ID = 1
tzinfo=zoneinfo.ZoneInfo(key="Europe/Paris")
TEST_PAYMENT_DUE = datetime(2023, 7, 11, 15, 29, 27, 929520, tzinfo=tzinfo)