import gitlab
from utils import get_gitlab_connection

gl = get_gitlab_connection()

# Fetch all projects
projects = gl.projects.list(all=True)

# Iterate through each project and fetch deploy keys
for project in projects:
    try:
        deploy_keys = project.keys.list()

        if not deploy_keys:
            continue

        print(f"Deploy keys for project {project.name}:")
        for key in deploy_keys:
            print(f"- {key.id} . {key.title}: {key.key}")

        print("")
    except gitlab.exceptions.GitlabGetError as e:
        print(f"Failed to get deploy keys for project {project.name}: {e}")

print("Deploy keys retrieval completed.")