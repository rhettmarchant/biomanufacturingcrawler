@partial
Feature: Query unit tests

    Scenario Outline: Chemical queries are built from chemical names, synonyms, and abbreviations
        Given a chemical's <name> <synonyms> and <abbreviations>
        When I build the chemical query from the chemical information
        Then the chemical query should be <expected_query>

        Examples:
            | name            | synonyms                      | abbreviations | expected_query                                                                    |
            | empty           | empty                         | empty         | empty                                                                             |
            | polylactic_acid | empty                         | empty         | polylactic acid                                                                 |
            | polylactic_acid | polylactide                   | empty         | ("polylactic acid" OR "polylactide")                                              |
            | polylactic_acid | polylactide,poly(lactic)_acid | empty         | ("polylactic acid" OR "polylactide" OR "poly(lactic) acid")                       |
            | polylactic_acid | empty                         | PLA           | ("polylactic acid" OR "PLA")                                                      |
            | polylactic_acid | empty                         | PLA,PL_acid   | ("polylactic acid" OR "PLA" OR "PL acid")                                         |
            | polylactic_acid | polylactide,poly(lactic)_acid | PLA,PL_acid   | ("polylactic acid" OR "polylactide" OR "poly(lactic) acid" OR "PLA" OR "PL acid") |

    Scenario Outline: Keywords are built into search terms
        Given a dictionary of keywords with the categories <method> <volume> <production> and <feedstock>
        When I build the search terms from the keywords
        Then the search terms should be <expected_terms>

        Examples:
            | method                                   | volume                     | production                                            | feedstock                                   | expected_terms                                                                                                                                                                                                                                       |
            | biomanufacturing,bioreactor,fermentation | ton,tons,tonnes,metric_ton | production_capacity,annual_production,annual_capacity | corn,sugar,sugarcane,biomass,starch,glucose | ("biomanufacturing" OR "bioreactor" OR "fermentation"), ("ton" OR "tons" OR "tonnes" OR "metric ton"), ("production capacity" OR "annual production" OR "annual capacity"), ("corn" OR "sugar" OR "sugarcane" OR "biomass" OR "starch" OR "glucose") |
            | biomanufacturing,bioreactor,fermentation | ton,tons,tonnes,metric_ton | production_capacity,annual_production,annual_capacity | empty                                       | ("biomanufacturing" OR "bioreactor" OR "fermentation"), ("ton" OR "tons" OR "tonnes" OR "metric ton"), ("production capacity" OR "annual production" OR "annual capacity")                                                                           |
            | biomanufacturing,bioreactor,fermentation | ton,tons,tonnes,metric_ton | empty                                                 | empty                                       | ("biomanufacturing" OR "bioreactor" OR "fermentation"), ("ton" OR "tons" OR "tonnes" OR "metric ton")                                                                                                                                                |
            | empty                                    | empty                      | empty                                                 | empty                                       | empty                                                                                                                                                                                                                                                |

    Scenario Outline: Search terms are combined with a chemical query to form a google query
        Given a chemical query <chemical_query>
        And a list of search terms <search_terms>
        When I build the google query from the search terms and chemical query
        Then the google query should be <expected_query>

        Examples:
            | chemical_query                       | search_terms                                                                                         | expected_query                                                                                                                                    |
            | ethanol                              | ("biomanufacturing"_OR_"bioreactor"_OR_"fermentation"),("ton"_OR_"tons"_OR_"tonnes"_OR_"metric_ton") | ethanol AND ("biomanufacturing" OR "bioreactor" OR "fermentation") AND ("ton" OR "tons" OR "tonnes" OR "metric ton")                              |
            | ("polylactic_acid"_OR_"polylactide") | ("biomanufacturing"_OR_"bioreactor"_OR_"fermentation"),("ton"_OR_"tons"_OR_"tonnes"_OR_"metric_ton") | ("polylactic acid" OR "polylactide") AND ("biomanufacturing" OR "bioreactor" OR "fermentation") AND ("ton" OR "tons" OR "tonnes" OR "metric ton") |
            | ethanol                              | empty                                                                                                | ethanol                                                                                                                                           |
            | empty                                | empty                                                                                                | empty                                                                                                                                             |