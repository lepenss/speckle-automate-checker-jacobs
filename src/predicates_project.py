"""Defines mappings between spreadsheet predicates and rule methods."""

from src.rules import PropertyRules

# Mapping of input predicates to the corresponding methods in PropertyRules
PREDICATE_PROJECT_METHOD_MAP = {
    "is unique in project": PropertyRules.is_unique_in_project.__name__,
}
