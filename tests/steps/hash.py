import time

from behave import given, when, then

from helpers import (
    job_id_from,
    hash_from,
    validate_response_status,
    validate_sha512_base64_hash,
    get_job_ids_for_newly_created_hashes,
    get_valid_password_value,
)

#########
# Given #
#########


@given("a valid password value")
def step_get_valid_password_value(context):
    context.password = get_valid_password_value()


@given("a job ID for a newly created hash")
def step_get_job_id_for_newly_created_hash(context):
    context.job_id = get_job_id_for_newly_created_hash(
        context.client, get_valid_password_value()
    )


def get_job_id_for_newly_created_hash(client, password):
    return job_id_from(client.create_hash(password))


@given("a job ID for a hash that was created more than {delay} seconds ago")
def step_get_job_id_after_delay(context, delay):
    context.job_id = get_job_id_for_newly_created_hash(
        context.client, get_valid_password_value()
    )
    time.sleep(int(delay))


@given("an invalid create hash payload that is {description}")
def step_get_invalid_payload(context, description):
    context.payload = get_invalid_create_hash_payload(description)


def get_invalid_create_hash_payload(description):
    if description == "empty":
        return ""
    elif description == "just a password value":
        return get_valid_password_value()
    else:
        raise ValueError(f"Invalid description: '{description}'")


@given("an invalid job ID that is {description}")
def step_get_invalid_job_id(context, description):
    context.job_id = get_invalid_job_id(description)


def get_invalid_job_id(description):
    if description == "a string":
        return "string"
    elif description == "a number":
        # This number is large enough to be confident the tests won't create that many hashes,
        # but ideally this would dynamically figure out how many hashes have been created already
        # and use a number higher than that.
        # For the sake of time, I did not implement that logic in this assignment.
        return 10000
    else:
        raise ValueError(f"Invalid description: '{description}'")


########
# When #
########


@when("a hash is created for that value")
def step_create_hash(context):
    password = getattr(context, "password", None)
    payload = getattr(context, "payload", None)
    context.response = context.client.create_hash(password=password, payload=payload)


@when("the hash for that job ID is retrieved")
def step_retrieve_hash(context):
    context.response = context.client.get_hash(context.job_id)


@when("two separate hashes are created for that value")
def step_get_job_ids_for_two_hashes(context):
    context.job_ids = get_job_ids_for_newly_created_hashes(
        context.client, 2, context.password
    )


########
# Then #
########


@then("the response content should contain a valid job ID")
def step_validate_job_id_in_response(context):
    validate_job_id_in_response(context.response)


def validate_job_id_in_response(response):
    try:
        int(response.content)
    except TypeError as e:
        raise AssertionError(
            "The response content did not include a valid job ID."
        ) from e


@then("the hash should not yet be retrievable")
def step_validate_hash_not_ready(context):
    validate_hash_not_ready(context.response)


def validate_hash_not_ready(response):
    # The 404 status code is hard-coded due to limitations of the
    # validate_response_status function.
    # Ideally, I would tell that function to expect a 4xx status.
    validate_response_status(response.status_code, 404)


@then("the response content should contain a valid hash")
def step_validate_valid_hash(context):
    validate_sha512_base64_hash(hash_from(context.response))


@then("both hashes should be exactly the same")
def step_validate_hash_values_are_the_same(context):
    validate_hash_values_are_the_same(context.client, context.job_ids)


def validate_hash_values_are_the_same(client, job_ids):
    unique_hash_strings = {hash_from(client.get_hash(job_id)) for job_id in job_ids}
    assert (
        len(unique_hash_strings) == 1
    ), f"The hashes are not exactly the same: {unique_hash_strings}"


@then("the response content should explain that the input is invalid")
def validate_response_content_says_invalid_input(context):
    assert "Malformed Input" in str(context.response.content)
