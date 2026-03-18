
import os
from src.spreadsheet import read_rules_from_spreadsheet
from src.rule_processor import validate_rule_structure
from src.helpers import speckle_print

rules_root = "/Workspace/Shared/PandIDValidation_rules/"

all_errors = []


# Loop through folders inside rules_root
for folder_name in os.listdir(rules_root):
    folder_path = os.path.join(rules_root, folder_name)


    # Check only directories that contain a rules.csv
    rules_csv = os.path.join(folder_path, "rules.csv")
    if not os.path.isdir(folder_path) or not os.path.exists(rules_csv):
        continue

    speckle_print(f"🔍 Checking rules in folder: {folder_name}")


    try:
        grouped_rules, messages = read_rules_from_spreadsheet(rules_csv)
    except Exception as e:
        # Critical error reading spreadsheet
        error_msg = f"[{folder_name}] Failed to read rules.csv: {str(e)}"
        speckle_print(error_msg)
        all_errors.append(error_msg)
        continue

    # Validate rules
    for rule_id, rule_group in grouped_rules:
        try:
            validate_rule_structure(rule_group)
        except ValueError as e:
            error_msg = f"[{folder_name}] Rule {rule_id} validation error: {str(e)}"
            speckle_print(error_msg)
            all_errors.append(error_msg)

# Raise if errors accumulated
if all_errors:
    raise ValueError(
        "Some rule groups failed validation:\n" +
        "\n".join(all_errors)
    )

speckle_print("🎉 All rules validated successfully!")
