Feature: Hash
  Users should be able to create and retrieve hashes.

  @positive
  Scenario: A new hash can be created
    Given a valid password value
    When a hash is created for that value
    Then the response status should be 'OK'
    And the response content should contain a valid job ID

  @positive
  @quarantined @BUG-1
  Scenario: A job ID is returned for new hash creation before hash is ready
    Given a job ID for a newly created hash
    When the hash for that job ID is retrieved
    Then the hash should not yet be retrievable

  @positive
  Scenario: A created hash is retrievable after a period of time
    Given a job ID for a hash that was created more than 5 seconds ago
    When the hash for that job ID is retrieved
    Then the response status should be 'OK'
    And the response content should contain a valid hash

  @positive
  Scenario: Two hashes created from the same password value are the same
    Given a valid password value
    When two separate hashes are created for that value
    Then both hashes should be exactly the same

  @negative
  Scenario Outline: The API errors when creating a hash with an invalid payload
    Given an invalid create hash payload that is <description>
    When a hash is created for that value
    Then the response status should be 'BAD_REQUEST'
    And the response content should explain that the input is invalid

    Examples:
      | description           |
      | empty                 |
      | just a password value |

  @negative
  @BUG-4
  Scenario Outline: The API errors when a non-existent hash is retrieved
    Given an invalid job ID that is <description>
    When the hash for that job ID is retrieved
    Then the response status should be 'NOT_FOUND'

    Examples:
      | description           |
      | a string              |
      | a number              |
