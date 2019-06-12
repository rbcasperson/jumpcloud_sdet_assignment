Feature: Shutdown
  The server should be able to shut down via API request.

  Background:
    Given a freshly started server

  Scenario: The server can be shut down
    When the server is shut down via an API request
    Then the server should no longer be accessible

  Scenario: In progress hash creation requests are completed before shutdown
    When the server is shut down right after a new hash creation request is made
    Then the hash creation should complete before the server is shut down

  Scenario: New hash creation requests are rejected after a shutdown is initiated
    When the server is shut down right before a new hash creation request is made
    Then the new hash creation request should be rejected
