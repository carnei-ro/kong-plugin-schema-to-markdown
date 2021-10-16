import yaml
import re
from tomark import Tomark

PRIMITIVES = ['string', 'number', 'boolean', 'integer']
VALIDATIONS_KEYWORDS = ['between', 'eq', 'ne', 'gt', 'len_eq', 'len_min', 'len_max', 'match',
                        'not_match', 'match_all', 'match_none', 'match_any', 'starts_with', 'one_of', 'contains', 'is_regex']


def _dump_yaml_to_md_table(obj) -> str:
    s = yaml.dump(obj, default_flow_style=False)
    s = re.sub(r'\.\.\.\n$', '', s)  # Converting "None" to yaml
    s = re.sub(r'\n$', '', s)
    s = re.sub(r'\n', '<br/>', s)
    if s in ['null', '[]', '{}']:
        return ''
    return f"<pre>{s}</pre>"


def _parse_primitives_types(schema_configs, _, additional_dict_tables):
    return [schema_configs['type'], additional_dict_tables]


def _parse_map_type(schema_configs, field_name, additional_dict_tables):
    suffix = ' '.strip() if schema_configs['values']['type'] in PRIMITIVES else '**'
    field_type = f"map[{schema_configs['keys']['type']}][{schema_configs['values']['type']}{suffix}]"
    new_table_object = {}
    try:
        if schema_configs['values']['type'] == 'record':
            new_table_object = {field_name: _schemas_to_table(
                schema_configs['values']['fields'], additional_dict_tables)}
            additional_dict_tables.append(new_table_object)
    except:
        raise
    return [field_type, additional_dict_tables]


def parse_lists_type(schema_configs, field_name, additional_dict_tables):
    suffix = ' '.strip() if schema_configs['elements']['type'] in PRIMITIVES else '**'
    field_type = f"{schema_configs['type']} of {schema_configs['elements']['type']}s{suffix}"
    try:
        if schema_configs['elements']['type'] == 'record':
            new_table_object = {field_name: _schemas_to_table(
                schema_configs['elements']['fields'], additional_dict_tables)}
            additional_dict_tables.append(new_table_object)
    except:
        raise
    return [field_type, additional_dict_tables]


def parse_record_type(schema_configs, field_name, additional_dict_tables):
    try:
        new_table_object = {field_name: _schemas_to_table(
            schema_configs['fields'], additional_dict_tables)}
        additional_dict_tables.append(new_table_object)
    except:
        raise
    return [f"{schema_configs['type']}**", additional_dict_tables]


_parser_types = {
    "map": _parse_map_type,
    "set": parse_lists_type,
    "array": parse_lists_type,
    "record": parse_record_type,
}
for primitive_type in PRIMITIVES:
    _parser_types[primitive_type] = _parse_primitives_types


def _validations_primitives(schema_configs):
    validations = []
    for validation_keyword in VALIDATIONS_KEYWORDS:
        try:
            validation = {validation_keyword: schema_configs[validation_keyword]}
            validations.append(validation)
        except:
            pass
    return validations


def _validations_lists(schema_configs):
    validations = []
    for validation_keyword in VALIDATIONS_KEYWORDS:
        try:
            validation = {validation_keyword: schema_configs['elements'][validation_keyword]}
            validations.append(validation)
        except:
            pass
    return validations


_validations_types = {
    "map": _parse_map_type,
    "set": _validations_lists,
    "array": _validations_lists,
    "record": parse_record_type,
}
for primitive_type in PRIMITIVES:
    _validations_types[primitive_type] = _validations_primitives


def _schemas_to_table(schemas, additional_dict_tables) -> dict:
    output = []
    for schema_object in schemas:
        for field_name, schema_configs in schema_object.items():
            table_row = {}
            table_row['name'] = field_name
            try:
                [table_row['type'], additional_dict_tables] = _parser_types[schema_configs['type']](
                    schema_configs, field_name, additional_dict_tables)
            except:
                table_row['type'] = "not supported yet"
            try:
                table_row['required'] = schema_configs['required'] if schema_configs['type'] != "record" else False
            except:
                table_row['required'] = False
            table_row['validations'] = []
            table_row['default'] = None
            try:
                table_row['default'] = schema_configs['default']
            except:
                pass
            try:
                table_row['validations'] = _validations_types[schema_configs['type']](
                    schema_configs)
            except:
                pass
            table_row['required'] = _dump_yaml_to_md_table(table_row['required'])
            table_row['validations'] = _dump_yaml_to_md_table(table_row['validations'])
            table_row['default'] = _dump_yaml_to_md_table(table_row['default'])
            output.append(table_row)
    return output


def schemas_to_md_tables(schemas) -> str:
    output = ["## config\n"]
    additional_dict_tables = []
    config_table = _schemas_to_table(schemas, additional_dict_tables)
    output.append(Tomark.table(config_table))
    for additional_dict_table in additional_dict_tables:
        for record_name, record_config_table in additional_dict_table.items():
            output.append(f"### record** of {record_name}\n")
            output.append(Tomark.table(record_config_table))
    return "\n".join(output)
