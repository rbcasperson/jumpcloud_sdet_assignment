Feature: Shutdown
  The server should be able to shut down via API request.

  Background:
    Given a freshly started server

  @positive
  @quarantined @BUG-3
  Scenario: The server can be shut down via API
    When the server is shut down via an API request
    Then the response status should be 'OK'
    And the server should no longer be accessible

  # This scenario is affected by both BUG-1 and BUG-3.
  # BUG-1 makes this scenario difficult to implement
  # since there is no asynchronous activity working in the API
  @positive
  @quarantined @BUG-3 @BUG-1
  Scenario: In progress hash creation requests are completed before shutdown
    When the server is shut down right after a new hash creation request is made
    Then the hash creation should complete before the server is shut down

  # This scenario passes despite BUG-1,
  # but with the asynchronous logic fixed,
  # this test can be expanded to cover more scenarios with in-progress hash creation.
  @positive
  Scenario: New hash creation requests are rejected after a shutdown is initiated
    When the server is shut down right before a new hash creation request is made
    Then the new hash creation request should be rejected
