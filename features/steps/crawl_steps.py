from behave import given, when, then
import src.biomfg_crawler.crawl as crawl
from requests.exceptions import HTTPError


# Scenario: Google search with valid API key, CX, query, and start

@given("a valid query and start")
def step_given_valid_query_start(context):
    context.query = "valid query"
    context.start = 1

@given("a valid query")
def step_given_valid_query(context):
    context.query = "valid query"

@given("a valid start")
def step_given_valid_start(context):
    context.start = 1

@given("a valid API key")
def step_given_valid_api_key(context):
    context.api_key = context.api_key

@given("a valid CX")
def step_given_valid_cx(context):
    context.cx = context.cx

@given("an invalid CX")
def step_given_invalid_cx(context):
    context.cx = "INVALID_CX"

@given("an invalid API key")
def step_given_invalid_api_key(context):
    context.api_key = "INVALID_API_KEY"

@given("an invalid query")
def step_given_invalid_query(context):
    context.query = ""

@given("an invalid start")
def step_given_invalid_start(context):
    context.start = 92

@when("I run the google search")
def step_when_run_google_search(context):
    try:
        context.result = crawl.google_search(context.api_key, context.cx, context.query, context.start)
        context.is_valid = True
    except HTTPError as e:
        context.result = f"HTTPError: {e.response.status_code} {e.response.reason}"
        context.is_valid = False
    except Exception as e:
        context.result = str(e)
        context.is_valid = False

@then("result should be valid")
def step_then_result_should_be_valid(context):
    print("Result: ", context.result)
    assert context.is_valid, f"Expected valid result, but got error: {context.result}"

@then("result should be invalid")
def step_then_result_should_be_invalid(context):
    print("Result: ", context.result)
    assert not context.is_valid, f"Expected invalid result, but got valid: {context.result}"
