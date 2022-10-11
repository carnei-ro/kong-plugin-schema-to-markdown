import sys
import requests


def _print_and_fail(kong_plugins_metadata_endpoint, plugin_name):
    print(
      f"Could not reach {kong_plugins_metadata_endpoint}\n\nIs kong running?\n\n- Try `make start` then `make update-readme`\n- Or execute again with arguments '{plugin_name}' 'http://<my-kong>:<admin-endpoint>/schemas/plugins' 'http://<my-kong>:<custom-plugin-metadata-endpoint>'")
    sys.exit(1)


def get_plugin_priority_and_version(kong_plugins_metadata_endpoint, plugin_name):
    try:
        r = requests.get(kong_plugins_metadata_endpoint)
    except:
        _print_and_fail(kong_plugins_metadata_endpoint, plugin_name)

    if r.status_code != 200:
        _print_and_fail(kong_plugins_metadata_endpoint, plugin_name)

    try:
      plugin = r.json()['plugins']['available_on_server'][plugin_name]
    except:
      plugin = {}

    try:
      [ priority, version ] = [ plugin['priority'], plugin['version'] ]
    except:
      _print_and_fail(kong_plugins_metadata_endpoint, plugin_name)
    return [ priority, version ]
