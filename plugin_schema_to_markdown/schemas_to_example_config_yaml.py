DEFAULT_PRIMITIVE_VALUES_MAP = {
    'string': '',
    'number': 0.0,
    'integer': 0,
    'boolean': False
}


def _default_primitive_values(schema_configs):
    if 'default' in schema_configs and schema_configs['default']:
        return schema_configs['default']
    return DEFAULT_PRIMITIVE_VALUES_MAP[schema_configs['type']]


def _default_map_value(schema_configs):
    if 'default' in schema_configs and schema_configs['default']:
        return schema_configs['default']
    if not schema_configs['values']['type'] == 'record':
        return {}
    key = 'some_key' if schema_configs['keys']['type'] == 'string' else '?'
    return {key: schemas_to_example_config_yaml(schema_configs['values']['fields'])}


def _default_lists_value(schema_configs):
    if 'default' in schema_configs and schema_configs['default']:
        return schema_configs['default']
    if not schema_configs['elements']['type'] == 'record':
        return []
    return schemas_to_example_config_yaml(schema_configs['elements']['fields'])


def _default_record_value(schema_configs):
    if 'default' in schema_configs and schema_configs['default']:
        return schema_configs['default']
    return schemas_to_example_config_yaml(schema_configs['fields'])


DEFAULT_VALUES_MAP = {
    'string': _default_primitive_values,
    'number': _default_primitive_values,
    'integer': _default_primitive_values,
    'boolean': _default_primitive_values,
    'map': _default_map_value,
    'set': _default_lists_value,
    'array': _default_lists_value,
    'record': _default_record_value
}


def schemas_to_example_config_yaml(schemas) -> dict:
    config = {}
    for schema_object in schemas:
        for field_name, schema_configs in schema_object.items():
            try:
                config[field_name] = DEFAULT_VALUES_MAP[schema_configs['type']](schema_configs)
            except:
                config[field_name] = "# sorry, example for this field is not implemented yet by the parser"
    return config
