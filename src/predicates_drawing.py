"""Defines mappings between spreadsheet predicates and rule methods."""

from src.rules import PropertyRules

# Mapping of input predicates to the corresponding methods in PropertyRules
PREDICATE_DRAWING_METHOD_MAP = {
    "is unique in drawing": PropertyRules.is_unique_in_drawing.__name__,
}
