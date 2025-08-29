import json
# production synonyms AND chemical synonyms AND method synonyms AND volume synonyms

# read in a tsv, select a column, and write each row into a list of strings then create a query string with OR separating each word and double-quotes around each word
def import_search_terms_tsv(file):
    en_search_terms = {}
    zh_search_terms = {}
    search_terms = {}
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        rows = [line.split("\t") for line in lines]
        headers = [word.strip() for word in rows[0]]
        for colidx in range(0, len(headers)):
            search_terms[headers[colidx]] = []
            for rowidx in range(1, len(rows)):
                if not rows[rowidx][colidx].strip():
                    continue
                search_terms[headers[colidx]].append(rows[rowidx][colidx].strip())
        for header, column in search_terms.items():
            query = " OR ".join([f'"{word}"' for word in column])
            search_terms[header] = f"({query})"
    # Keys to extract
    en_keys = ["Method", "Volume", "Production", "Feedstock"]
    zh_keys = ["Method (ZH)", "Volume (ZH)", "Production (ZH)", "Feedstock (ZH)"]

    # Extract the items
    en_search_terms = {key: search_terms[key] for key in en_keys}
    zh_search_terms = {key: search_terms[key] for key in zh_keys}

    combined_terms = {'english': en_search_terms, 'chinese': zh_search_terms}
    return combined_terms

def import_chemical_names(file):
    en_search_terms = {}
    zh_search_terms = {}
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        rows = [line.split("\t") for line in lines]
        for chemical in rows[1:]:
            chemical_name = chemical[1].strip()
            if chemical[2].strip() == "":
                chemical_query = chemical_name
                en_search_terms[chemical_name] = f'"{chemical_query}"'
            else:
                chemical_query = " OR ".join([f'"{name}"' for name in chemical[1:3]])
                en_search_terms[chemical_name] = f'({chemical_query})'
        for chemical in rows[1:]:
            chemical_name = chemical[1].strip()
            if chemical[5].strip() == "":
                chemical_query = chemical[4].strip()
                zh_search_terms[chemical_name] = f'"{chemical_query}"'
            else:
                chemical_query = " OR ".join([f'"{name}"' for name in chemical[4:5]])
                zh_search_terms[chemical_name] = f'({chemical_query})'
    search_terms = {'english': en_search_terms, 'chinese': zh_search_terms}
    return search_terms

def generate_search_query(chemicals, search_terms, language):
    queries = {}
    lang_chemicals = chemicals[language]
    lang_search_terms = search_terms[language]
    search_query = " AND ".join([f'{value}' for key, value in lang_search_terms.items()])
    for name, query in lang_chemicals.items():
        queries[name] = f"{query} AND {search_query}"
    return queries

def export_to_tsv(queries, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for name, query in queries.items():
            f.write(f"{name}\t{query}\n")

if __name__ == "__main__":
    chemicals_tsv = 'August 2025 - GyG AI Screening Terms - Chemicals.tsv'
    queries_tsv = 'August 2025 - GyG AI Screening Terms - Queries.tsv'

    chemicals = import_chemical_names(chemicals_tsv)
    search_terms = import_search_terms_tsv(queries_tsv)

    en_searches = generate_search_query(chemicals, search_terms, 'english')
    print(json.dumps(en_searches, indent = 2))
    export_to_tsv(en_searches, 'August 2025 - GyG AI Queries - English.tsv')

    zh_searches = generate_search_query(chemicals, search_terms, 'chinese')
    print(json.dumps(zh_searches, indent = 2))
    export_to_tsv(zh_searches, 'August 2025 - GyG AI Queries - Chinese.tsv')
