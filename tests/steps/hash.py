import time

from behave import given, when, then

from helpers import (
    job_id_from,
    hash_from,
    validate_response_status,
    validate_sha512_base64_hash,
)

#########
# Given #
#########


@given("a valid password value")
def step_get_valid_password_value(context):
    context.password = get_valid_password_value()


password_count = 0


def get_valid_password_value():
    global password_count
    password_count += 1
    return f"unique-valid-password-value-{password_count}"


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


########
# When #
########


@when("a hash is created for that value")
def step_create_hash(context):
    context.response = context.client.create_hash(context.password)


@when("the hash for that job ID is retrieved")
def step_retrieve_hash(context):
    context.response = context.client.get_hash(context.job_id)


@when("two separate hashes are created for that value")
def step_get_job_ids_for_two_hashes(context):
    context.job_ids = get_job_ids_for_newly_created_hashes(
        context.client, 2, context.password
    )


def get_job_ids_for_newly_created_hashes(client, hashes_count, password):
    return [job_id_from(client.create_hash(password)) for _ in range(hashes_count)]


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
