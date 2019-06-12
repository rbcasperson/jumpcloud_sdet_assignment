Feature: Stats
  Statistics for hash creation should be present and accurate.

  Background:
    Given a freshly started server

  Scenario Outline: Statistics can be retrieved and are accurate
    And <hash-count> hashes have been successfully created
    When hash statistics are gathered
    Then the response status should be 'OK'
    And the response content should say that <hash-count> requests have been made

    Examples:
      | hash-count |
      | 0          |
      | 1          |
      | 10         |

  @quarantined @BUG-2
  Scenario Outline: The average time to create a hash is recorded accurately
    Given the average time for creating <hash-count> hashes
    When hash statistics are gathered
    Then the average time in the response content should be close to the given average time

    Examples:
      | hash-count |
      | 0          |
      | 1          |
      | 10         |