import re

#
# Client Helpers
#


def job_id_from(create_hash_response):
    return int(create_hash_response.content)


def hash_from(get_hash_response):
    return str(get_hash_response.content.decode())


def get_job_ids_for_newly_created_hashes(client, hashes_count, password):
    return [job_id_from(client.create_hash(password)) for _ in range(hashes_count)]


#
# Test Helpers
#

password_count = 0


def get_valid_password_value():
    global password_count
    password_count += 1
    return f"unique-valid-password-value-{password_count}"


# Ideally, this would be much more expanded to accept codes as string, ints, or a range,
# and to expand the error message further for maximum usefulness.
def validate_response_status(actual_code, expected_code):
    assert (
        actual_code == expected_code
    ), f"Expected code {expected_code}, but received code {actual_code}."


def validate_sha512_base64_hash(hash):

    assert re.match(
        r"^[A-Za-z0-9+/]{86}==$", hash
    ), f"{hash} is not a valid base64 encoded SHA512 hash."
