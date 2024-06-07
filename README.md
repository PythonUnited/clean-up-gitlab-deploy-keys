# Scripts to clean up Gitlab deploy keys

Install dependencies:

```sh
pip install -r requirements.txt
```

In the `src` directory copy `env-example` to .env` file, and edit to add Gitlab URL and API access token:

```sh
cp env-example .env
```

## Read deploy keys

```sh
python list_deploy_keys.py
```

Add numeric IDs of deploy keys which need to be delete to a file name 
`deploy_keys.txt`, each deploy key ID on a new line. 

## Delete deploy keys

```sh
python delete_deploy_keys.py
```

This script list the deploy keys which are about to be deleted and ask
for confirmation before deleting.
