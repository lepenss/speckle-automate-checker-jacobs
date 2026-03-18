
from src.spreadsheet import read_rules_from_spreadsheet
from src.rule_processor import validate_rule_structure
from src.helpers import speckle_print

rules_directory = "./rules/rules_MSD/"

# Load rules and run validation
grouped_rules, messages = read_rules_from_spreadsheet(f"{rules_directory}rules.csv")

errors = []

for rule_id, rule_group in grouped_rules:
    try:
        validate_rule_structure(rule_group)
    except ValueError as e:
        error_message = f"Rule {rule_id} validation error: {str(e)}"
        speckle_print(error_message)
        errors.append(error_message)

# After loop: if any errors occurred → raise one combined exception
if errors:
    raise ValueError(
        "Some rule groups failed validation:\n" +
        "\n".join(errors)
    )
