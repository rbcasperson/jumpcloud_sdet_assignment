from behave import when, then
import requests

from helpers import get_valid_password_value, job_id_from, hash_from


########
# When #
########


@when("the server is shut down via an API request")
def step_shut_down_server_with_api(context):
    context.response = try_to_shut_down_with_api(context.client)


def try_to_shut_down_with_api(client):
    try:
        return client.shut_down()
    except requests.exceptions.ConnectionError:
        raise AssertionError("The server was shut down before it returned a response.")


@when("the server is shut down right after a new hash creation request is made")
def step_start_hash_creation_before_shutdown(context):
    context.job_id = start_hash_creation_before_shutdown(context.client)


def start_hash_creation_before_shutdown(client):
    job_id = job_id_from(client.create_hash(get_valid_password_value()))
    try_to_shut_down_with_api(client)
    return job_id


@when("the server is shut down right before a new hash creation request is made")
def step_start_shutdown_before_has_creation(context):
    try_to_shut_down_with_api(context.client)


########
# Then #
########


@then("the server should no longer be accessible")
def step_validate_service_inaccessible(context):
    validate_service_inaccessible(context.client)


def validate_service_inaccessible(client):
    try:
        client.get_stats()
    except requests.exceptions.ConnectionError:
        pass
    else:
        raise AssertionError("The server appears to be still working.")


@then("the hash creation should complete before the server is shut down")
def step_validate_hash_completed_before_shut_down(context):
    validate_hash_completed_before_shut_down(context.client, context.job_id)


def validate_hash_completed_before_shut_down(client, job_id):
    # Temporary while polling isn't necessary
    try:
        assert hash_from(client.get_hash(job_id)), "No hash could be accessed"
    except requests.exceptions.ConnectionError:
        raise AssertionError("The server shut down before the hash was created.")
    validate_service_inaccessible(client)


@then("the new hash creation request should be rejected")
def step_ensure_new_hash_cannot_be_created(context):
    # If the server can't be accessed, then the create hash request can't even be made
    validate_service_inaccessible(context.client)
