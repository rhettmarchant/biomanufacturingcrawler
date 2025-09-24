from behave import given, when, then
import src.biomfg_crawler.query as query

@given("a dictionary of keywords with the categories {method} {volume} {production} and {feedstock}")
def step_given_keywords(context, method, volume, production, feedstock):
    context.source_data = {
        'Method': method.strip("[").strip("]").replace("_", " ").split(","),
        'Volume': volume.strip("[").strip("]").replace("_", " ").split(","),
        'Production': production.strip("[").strip("]").replace("_", " ").split(","),
        'Feedstock': feedstock.strip("[").strip("]").replace("_", " ").split(",")
    }
    if "empty" in context.source_data['Method']:
        del context.source_data['Method']
    if "empty" in context.source_data['Volume']:
        del context.source_data['Volume']
    if "empty" in context.source_data['Production']:
        del context.source_data['Production']
    if "empty" in context.source_data['Feedstock']:
        del context.source_data['Feedstock']

@when("I build the search terms from the keywords")
def step_when_build_search_terms(context):
    context.search_terms = query.generate_search_terms(context.source_data)

@then("the search terms should be {expected_terms}")
def step_then_search_terms_should_be(context, expected_terms):
    assert str(context.search_terms) == expected_terms, f"Expected search terms '{expected_terms}', but got '{context.search_terms}'."