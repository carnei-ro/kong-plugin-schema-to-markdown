import yaml
import sys

from schemas_to_md_tables import schemas_to_md_tables
from schemas_to_example_config_yaml import schemas_to_example_config_yaml
from request_schema import get_schemas_dict
from request_priority_and_version import get_plugin_priority_and_version
from custom_yaml_dumper import CUSTOMYAMLDUMPER

try:
    plugin_name = sys.argv[1]
except:
    plugin_name = 'kong-plugin'

try:
    kong_schema_endpoint = sys.argv[2]
except:
    kong_schema_endpoint = "http://172.17.0.1:8001/schemas/plugins/"

try:
    kong_plugins_metadata_endpoint = sys.argv[3]
except:
    kong_plugins_metadata_endpoint = "http://172.17.0.1:8001/"

[ plugin_priority, plugin_version ] = get_plugin_priority_and_version(kong_plugins_metadata_endpoint, plugin_name)

print(f"## Plugin Priority\n\nPriority: **{plugin_priority}**\n\n## Plugin Version\n\nVersion: **{plugin_version}**\n")

schemas = get_schemas_dict(kong_schema_endpoint, plugin_name)

print(schemas_to_md_tables(schemas))

example = {"plugins": [{"name": plugin_name, "enabled": True,
                        "configs": schemas_to_example_config_yaml(schemas)}]}
yaml_example = yaml.dump(example, default_flow_style=False,
                         Dumper=CUSTOMYAMLDUMPER, sort_keys=False)
print("## Usage\n\n```yaml")
print(yaml_example)
print("```")
