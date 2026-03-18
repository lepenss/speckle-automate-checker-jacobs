from specklepy.api.client import SpeckleClient

from helpers.validation import validate_model, validate_project

gate_result = dbutils.jobs.taskValues.get(
    taskKey="Test_Speckle_Webhook",
     key="gate", 
     default="")

print(gate_result)

if gate_result == "SKIP_REST":
    dbutils.notebook.exit("Skipped by gatekeeper")


client = SpeckleClient(host="https://ldd-emea.dev.jacobs.com/")

token = dbutils.secrets.get(scope="speckle-apps", key="dbx-webhook-token-dllpat")  # "dbx-webhook-token-mjtpat" / Replace with your token 
client.authenticate_with_token(token)

print(f"Authenticated as {client.account.userInfo.name}")

project_id = dbutils.jobs.taskValues.get(taskKey="Test_Speckle_Webhook", key="project_id", debugValue="57cc463580")
root_object_id = dbutils.jobs.taskValues.get(taskKey="Test_Speckle_Webhook", key="root_object_id", debugValue="5574c83730b848d1fd88723e1160dd5b")
model_id = dbutils.jobs.taskValues.get(taskKey="Test_Speckle_Webhook", key="model_id", debugValue="x")
version_id = dbutils.jobs.taskValues.get(taskKey="Test_Speckle_Webhook", key="version_id", debugValue="y")

# Validate project and model

rules_dir = "/Workspace/Shared/PandIDValidation_rules/rules_" + project_id + "/"

print("rules_dir = " + rules_dir)

validate_project(client, project_id, rules_directory=rules_dir)
models = client.model.get_models(project_id)
for model in models.items:
    print(f"Validating model: {model.name}")
    validate_model(client, project_id, model.id, model.name, rules_directory=rules_dir)