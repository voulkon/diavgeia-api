from diavgeia_api.models import DictionaryValuesResponse


def test_dictionary_schema(specific_dictionarys_result, one_dictionarys_name):
    assert isinstance(specific_dictionarys_result, DictionaryValuesResponse)
    assert specific_dictionarys_result.name == one_dictionarys_name
    assert specific_dictionarys_result.items and specific_dictionarys_result.items[
        0
    ].uid.startswith("fektype_")


def test_all_dictionaries_schema(all_dictionaries_result):
    ...
    # TODO: Assertions
