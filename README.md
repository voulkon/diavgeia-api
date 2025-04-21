# Diavgeia API Client

A Python wrapper for the Diavgeia Open Data API

## Table of Contents
- [Diavgeia API Client](#diavgeia-api-client)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Overview](#overview)
    - [Examples](#examples)
    - [Decisions](#decisions)
    - [Organizations](#organizations)
    - [Types](#types)
    - [Dictionaries](#dictionaries)
    - [Search](#search)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)
## Features

Makes easy to:

- Fetch: 
   1) decisions (and their version log)
   2) organizations (with their respective: 
      1) units like "ΓΡΑΦΕΙΟ ΑΝΤΙΔΗΜΑΡΧΟΥ", 
      2) positions, like "Προϊστάμενος Διεύθυνσης", "Δήμαρχος", etc.
      3) specific signers
   3) types (of government actions, like "ΠΡΑΞΕΙΣ ΚΑΝΟΝΙΣΤΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ", "ΠΡΑΞΕΙΣ ΟΙΚΟΝΟΜΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ", etc.),
   4) dictionaries where various unique id's are explained, for example:
      1) "uid": "FEKTYPES" --> "label": "Τύποι τευχών ΦΕΚ"
- Search decisions using advanced criteria (like issue date - Ημερομηνία έκδοσης- or signer - Κωδικός υπογράφοντα -) and their combinations (both a specific signer and a specific date range)

## Installation

```bash
pip install diavgeia-api
```

## Usage

### Overview

As is described in [an example](examples/target_a_decision_and_learn_more.ipynb), right now there are these methods:

```bash
Available methods:
- get_a_decision: Return a specific decision's details.
- get_a_decisions_specific_version: Returns details of a specific version of a decision.
- get_a_decisions_version_log: Returns details of a specific version of a decision.
- get_a_types_details: Returns details of a type.
- get_a_types_summary: Returns a summary of a specific type.
- get_all_types: Returns all existing types.
- get_dictionaries: Return the list of available dictionaries.
- get_dictionary: Return all items for a specific dictionary.
- get_organization: Returns details of a specific organization.
- get_organization_positions: Returns positions of a specific organization.
- get_organization_signers: Returns signers of a specific organization.
- get_organization_units: Returns units of a specific organization.
- get_organizations: Returns a list of registered organizations.
- search_advanced: Search for decisions with advanced query syntax.
- search_decisions: Search for decisions with simple parameters.

```

### Examples

This package includes several examples to help you get started:

- [Target a specific decision](examples/target_a_decision_and_learn_more.ipynb) - Learn how to fetch information about a decision and related entities
- [Search for decisions](examples/search.ipynb) - Examples of using the search functionality
- [Work with organizations](examples/target_an_organization_and_find_its_decisions.ipynb) - Explore organization data

You can find all examples in the [examples folder](examples/).


### Decisions

```bash
from diavgeia_api import DiavgeiaClient

# Initialize client
client = DiavgeiaClient()

decision = client.get_a_decision("Ψ11446ΜΓΨ7-ΠΚΛ")
print(f"Subject: {decision.subject}")
print(f"Organization: {decision.organization.label}")
print(f"Decision date: {decision.issue_date}")
```

### Organizations

```bash
# Organizations example
organizations = client.get_organizations()
for org in organizations.organizations[:5]:
    print(f"{org.label} ({org.uid})")
```


### Types

```bash
# Types example
types = client.get_all_types()
for type_item in types.types[:5]:
    print(f"{type_item.label} ({type_item.uid})")

# Get details for a specific type
type_details = client.get_a_types_details("Β.1.3")
print(f"Type: {type_details.label}")
print(f"Description: {type_details.description}")
```

### Dictionaries

```bash
# Dictionaries example
dictionaries = client.get_dictionaries()
print("Available dictionaries:")
for dictionary in dictionaries.dictionaries[:5]:
    print(f"- {dictionary.label} (ID: {dictionary.uid})")

# Get items from a specific dictionary
org_category_dict = client.get_dictionary("ORG_CATEGORY")
print("\nOrganization categories:")
for item in org_category_dict.items[:5]:
    print(f"- {item.label} (ID: {item.uid})")

```

### Search

```bash
# Simple search example
search_results = client.search_decisions(
    term="προμήθεια υπολογιστών",
    date_from="2023-01-01",
    date_to="2023-12-31"
)

print(f"Found {search_results.info.total} decisions")
for decision in search_results.decisions[:3]:
    print(f"- {decision.subject[:50]}... (ΑΔΑ: {decision.ada})")

# Advanced search example
advanced_search = client.search_advanced(
    q="subject:(προμήθεια υπολογιστών) AND issueDate:[2023-01-01 TO 2023-12-31] AND organizationUid:6321",
    sort="issueDate:desc"
)

print(f"\nAdvanced search found {advanced_search.info.total} decisions")
for decision in advanced_search.decisions[:3]:
    print(f"- {decision.subject[:50]}... (ΑΔΑ: {decision.ada})")
    
```

## Testing

This project uses pytest for testing. To run the tests:

```bash
# Install development dependencies
poetry install --with dev

# Run the tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=diavgeia_api
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
