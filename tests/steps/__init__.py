"""Common step definitions that are used in multiple feature files."""
from behave import given, then
from requests import codes

from helpers import validate_response_status


#########
# Given #
#########


@given("a freshly started server")
def step_restart_server(context):
    context.client.restart()


########
# Then #
########


@then("the response status should be '{expected_code}'")
def step_validate_response_status(context, expected_code):
    validate_response_status(
        context.response.status_code, getattr(codes, expected_code)
    )
