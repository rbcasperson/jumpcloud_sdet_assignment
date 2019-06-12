Feature: Stats
  Statistics for hash creation should be present and accurate.

  Scenario Outline: Statistics can be retrieved and are accurate
    Given a freshly started server
    And <hash-count> hashes have been successfully created
    When hash statistics are gathered
    Then the response status should be 'OK'
    And the response content should contain accurate statistics

    Examples:
      | hash-count |
      | 0          |
      | 1          |
      | 10         |
