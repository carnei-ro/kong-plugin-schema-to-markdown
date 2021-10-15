import sys
import requests


def get_schemas_dict(kong_schema_endpoint, plugin_name):
    try:
        r = requests.get(kong_schema_endpoint + plugin_name)
    except:
        print(
            f"Could not reach {kong_schema_endpoint}{plugin_name} - Try arguments '{plugin_name}' 'http://<my-kong>:<admin-endpoint>/schemas/plugins'")
        sys.exit(1)

    if r.status_code != 200:
        print(
            f"Could not reach {kong_schema_endpoint}{plugin_name} - Try arguments '{plugin_name}' 'http://<my-kong>:<admin-endpoint>/schemas/plugins'")
        sys.exit(1)

    config = [f for f in r.json()['fields'] if 'config' in f.keys()]
    return config[0]['config']['fields']
