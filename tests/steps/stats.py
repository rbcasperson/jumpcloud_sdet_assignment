import math
import time

from behave import given, when, then

from helpers import get_valid_password_value


#########
# Given #
#########


@given("{hash_count} hashes have been successfully created")
def step_create_hashes(context, hash_count):
    create_hashes(context.client, int(hash_count))


def create_hashes(client, count):
    for _ in range(count):
        client.create_hash(get_valid_password_value())


@given("the average time for creating {hash_count} hashes")
def step_calculate_average_hash_creation_time(context, hash_count):
    context.average_hash_creation_time = get_average_hash_creation_time(
        context.client, int(hash_count)
    )


def get_average_hash_creation_time(client, count):
    if count == 0:
        return 0

    start = time.time()
    create_hashes(client, count)
    total_time = time.time() - start
    # Convert returned time to milliseconds to match the /stats response
    return round((float(total_time) / count) * 1000, 2)


########
# When #
########


@when("hash statistics are gathered")
def step_gather_stats(context):
    context.response = context.client.get_stats()


########
# Then #
########


@then("the response content should say that {hash_count} requests have been made")
def step_validate_statistics(context, hash_count):
    validate_statistics_count(context.response, int(hash_count))


def validate_statistics_count(response, hash_count):
    assert int(response.json()["TotalRequests"]) == hash_count


@then(
    "the average time in the response content should be close to the given average time"
)
def step_validate_average_time(context):
    validate_average_time_is_close(context.response, context.average_hash_creation_time)


def validate_average_time_is_close(response, average_time):
    average_time_from_response = float(response.json()["AverageTime"])
    tolerance = 0.01
    msg = (
        "The average hash creation time from the response was not accurate: "
        f"{average_time_from_response} should have been within {tolerance * 100}% of {average_time}"
    )
    assert math.isclose(average_time, average_time_from_response, rel_tol=0.01), msg
