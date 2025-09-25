@integrations
Feature: Crawl integration tests (with Google Custom Search API)

    Scenario: Google search with valid API key, CX, query, and start
        Given a valid query and start
        And a valid API key
        And a valid CX
        When I run the google search
        Then result should be valid

    @test
    Scenario: Google search with invalid API key
        Given a valid query and start
        And a valid CX
        But an invalid API key
        When I run the google search
        Then result should be invalid

    Scenario: Google search with invalid CX
        Given a valid query and start
        And a valid API key
        But an invalid CX
        When I run the google search
        Then result should be invalid

    Scenario: Google search with invalid query
        Given a valid start
        And a valid API key
        And a valid CX
        But an invalid query
        When I run the google search
        Then result should be invalid

    Scenario: Google search with invalid start (1-100)
        Given a valid query
        And a valid API key
        And a valid CX
        But an invalid start
        When I run the google search
        Then result should be invalid
        