import types

from DictMeta import DictMeta
from FieldMeta import FieldMeta
from ListMeta import ListMeta
from LeUtils import LeUtils, \
    s_objc_keyword_replace, s_objc_dialect_list, \
    u2C, u2c, leType, \
    s_list_types, s_dict_types


def gen_list_meta(base_value):
    base_value_type = leType(base_value)
    base_list_meta = ListMeta(base_value_type)
    if base_value_type in s_dict_types:
        base_list_meta.dict_meta = gen_dict_meta(base_value)
        base_list_meta.dict_meta.parent_list_meta = base_list_meta

    elif base_value_type in s_list_types:
        if len(base_value) > 0:
            base_list_meta.list_meta = gen_list_meta(base_value[0])
            base_list_meta.list_meta.parent_list_meta = base_list_meta

    return base_list_meta


def gen_dict_meta(base_value):
    base_dict_meta = DictMeta()

    for prop, value in base_value.items():
        value_type = leType(value)
        field_name = prop
        if LeUtils.s_dialect in s_objc_dialect_list:
            field_name = LeUtils.s_field_prefix + prop
        else:
            if LeUtils.s_field_prefix:
                if LeUtils.s_field_prefix[-1] == '_':
                    field_name = LeUtils.s_field_prefix + u2c(prop)
                else:
                    field_name = LeUtils.s_field_prefix + u2C(prop)
            else:
                field_name = u2c(prop)

        if LeUtils.s_dialect in s_objc_dialect_list:
            if field_name in s_objc_keyword_replace.keys():
                field_name = s_objc_keyword_replace[field_name]

        field_meta = gen_field_meta(field_name, prop, value)
        field_meta.parent_dict_meta = base_dict_meta

        if value_type in s_list_types:
            if len(value) > 0:
                field_list_meta = gen_list_meta(value[0])
                field_list_meta.parent_field_meta = field_meta
                field_meta.list_meta = field_list_meta
            else:
                continue
        elif value_type in s_dict_types:
            field_dict_meta = gen_dict_meta(value)
            field_dict_meta.parent_field_meta = field_meta

        base_dict_meta.field_meta_array.append(field_meta)

    return base_dict_meta


def gen_field_meta(field_name, orig, value):
    value_type = leType(value)
    base_field_meta = FieldMeta(field_name, value_type, orig)
    if value_type in s_list_types:
        if len(value) > 0:
            base_field_meta.list_meta = gen_list_meta(value[0])
            base_field_meta.list_meta.parent_field_meta = base_field_meta

    elif value_type in s_dict_types:
        base_field_meta.dict_meta = gen_dict_meta(value)
        base_field_meta.dict_meta.parent_field_meta = base_field_meta

    return base_field_meta
