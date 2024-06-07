import gitlab

from collections import defaultdict
from tqdm import tqdm

from utils import get_gitlab_connection


gl = get_gitlab_connection()

DEPLOY_KEYS_FILE = "deploy_keys.txt"

with open(DEPLOY_KEYS_FILE, "r") as file:
    deploy_key_ids = [line.strip() for line in file.readlines()]
    deploy_key_ids = list(map(int, deploy_key_ids))

print("=" * 80)
print(f"Found {len(deploy_key_ids)} deploy keys")
keys_per_project = defaultdict(list)

print("Retrieving all projects...")
projects = gl.projects.list(all=True)

print("Collecting projects belonging to deploy keys...")
for project in tqdm(projects):
    project_keys = [k.id for k in project.keys.list()]

    if not project_keys:
        continue

    for deploy_key_id in deploy_key_ids:
        if deploy_key_id not in project_keys:
            continue

        keys_per_project[deploy_key_id].append(project)

# Display the deploy keys which are about to be deleted
for deploy_key_id, projects in keys_per_project.items():
    print("-" * 80)
    print(f"Deploy key ID: {deploy_key_id}")

    for index, project in enumerate(projects):
        if index == 0:
            try:
                key = project.keys.get(deploy_key_id)
                print(f"{key.title} (ID: {deploy_key_id})")
            except gitlab.exceptions.GitlabGetError as e:
                print(f"Failed to retrieve deploy key {deploy_key_id}: {e}")
                continue

        print(f" - Project ID: {project.id}, Name: {project.name}")


print("=" * 80)
# Ask for confirmation to delete
confirm = input("Do you want to delete these deploy keys? (yes/no): ")

if confirm.lower() == "yes":
    # Delete each deploy key
    for deploy_key_id, projects in keys_per_project.items():
        for project in projects:
            try:
                project.keys.delete(deploy_key_id)
                print(
                    f"Deploy key {deploy_key_id} deleted successfully from project {project.id}."
                )
            except gitlab.exceptions.GitlabDeleteError as e:
                print(
                    f"Failed to delete deploy key {deploy_key_id} from project {project.id}: {e}"
                )
    print("\nDeploy key deletion process completed.")
else:
    print("\nDeploy key deletion aborted.")
