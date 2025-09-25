from behave import given, when, then
import src.biomfg_crawler.query as query


#Scenario Outline: Chemical queries are built from chemical names, synonyms, and abbreviations

@given("a chemical's {name} {synonyms} and {abbreviations}")
def step_given_chemical_info(context, name, synonyms, abbreviations):
    context.name = '' if name == "empty" else name.replace("_", " ")
    context.synonyms = None if synonyms == "empty" else [syn.strip().replace("_", " ") for syn in synonyms.split(",")]
    context.abbreviations = None if abbreviations == "empty" else [abbr.strip().replace("_", " ") for abbr in abbreviations.split(",")]

@when("I build the chemical query from the chemical information")
def step_when_generate_chemical_query(context):
    context.chemical_query = query.generate_chemical_query(context.name, context.synonyms, context.abbreviations)

@then("the chemical query should be {expected_query}")
def step_then_chemical_query_should_be(context, expected_query):
    if expected_query == "empty":
        expected_query = None
    else:
        expected_query = expected_query.replace("_", " ")
    assert context.chemical_query == expected_query, f"Expected chemical query '{expected_query}', but got '{context.chemical_query}'."


#Scenario Outline: Keywords are built into search terms

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
    if expected_terms == "empty":
        expected_terms_list = []
    else:
        expected_terms_list = expected_terms.strip("[").strip("]").replace("_", " ").split(", ")
    assert context.search_terms == expected_terms_list, f"Expected search terms '{expected_terms_list}', but got '{context.search_terms}'."


# Scenario Outline: Search terms are combined with a chemical query to form a google query

@given("a chemical query {chemical_query}")
def step_given_chemical_query(context, chemical_query):
    if chemical_query == "empty":
        context.chemical_query = ""
    else:
        context.chemical_query = chemical_query.replace("_", " ")

@given("a list of search terms {search_terms}")
def step_given_search_terms(context, search_terms):
    if search_terms == "empty":
        context.search_terms = []
    else:
        context.search_terms = search_terms.replace("_", " ").split(",")

@when("I build the google query from the search terms and chemical query")
def step_when_generate_google_query(context):
    context.google_query = query.generate_google_query(context.chemical_query, context.search_terms)

@then("the google query should be {expected_query}")
def step_then_google_query_should_be(context, expected_query):
    if expected_query == "empty":
        expected_query = ""
    else:
        expected_query = expected_query.replace("_", " ")
    assert context.google_query == expected_query, f"Expected Google query '{expected_query}', but got '{context.google_query}'."