import types

from ClassMeta import ClassMeta
from FieldMeta import FieldMeta
from LeUtils import s_objc_keyword_replace, s_objc_dialect_list,u2C, u2c, leType


def gen_class_meta(base_class_name, dialect, base_value, prefix=""):
    base_value_type = leType(base_value)
    base_class_meta = None
    if base_value_type == types.DictType:
        base_class_meta = ClassMeta(base_class_name, dialect)

        for prop, value in base_value.items():
            value_type = leType(value)
            field_name = prop
            if dialect in s_objc_dialect_list:
                field_name = prefix + prop
            else:
                if prefix:
                    if prefix[-1]=='_':
                        field_name = prefix + u2c(prop)
                    else:
                        field_name = prefix + u2C(prop)
                else:
                    field_name = u2c(prop)

            if field_name in s_objc_keyword_replace.keys():
                field_name = s_objc_keyword_replace[field_name]

            if value_type in FieldMeta.s_string_types:
                field_meta = FieldMeta(field_name, value_type, None, prop)
                base_class_meta.add_field(field_meta)

            if value_type in FieldMeta.s_number_types:
                value_type = leType(value)
                field_meta = FieldMeta(field_name, value_type, None, prop)
                base_class_meta.add_field(field_meta)
            elif value_type in FieldMeta.s_list_types:
                if len(value) > 0:
                    field_meta = gen_field_meta(base_class_name, dialect, field_name, prefix, prop, value[0],
                                                value_type)
                    base_class_meta.add_field(field_meta)
            elif value_type in FieldMeta.s_dict_types:
                field_meta = gen_field_meta(base_class_name, dialect, field_name, prefix, prop, value, value_type)
                base_class_meta.add_field(field_meta)
    elif base_value_type in FieldMeta.s_list_types:
        if len(base_value)>0:
            base_class_meta = ClassMeta(base_class_name, dialect)
            field_meta = gen_field_meta(base_class_name, dialect, "", prefix, "", base_value[0], base_value_type)
            base_class_meta.add_field(field_meta)
    else:
        print "could not generate class from type:%s" % base_value_type
        exit(-1)
    return base_class_meta


def gen_field_meta(base_class_name, dialect, field_name, prefix, prop, sub_value, value_type):
    sub_value_type = leType(sub_value)
    field_generic_type = None
    field_class_meta = None
    if sub_value_type in FieldMeta.s_number_types:
        field_generic_type = sub_value_type
    elif sub_value_type in FieldMeta.s_string_types:
        field_generic_type = sub_value_type
    elif sub_value_type in FieldMeta.s_list_types:
        if dialect in ['yy','mt']:
            print '======WARNING==== YYModel and Mantle does not support Array in Array, please remove in Json File'
        field_generic_type = sub_value_type
        sub_class_name = base_class_name + u2C(prop)
        sub_class_meta = gen_class_meta(sub_class_name,dialect,sub_value,prefix)
        field_class_meta = sub_class_meta
    elif sub_value_type in FieldMeta.s_dict_types:
        field_generic_type = sub_value_type
        if dialect in s_objc_dialect_list:
            sub_class_name = base_class_name + u2C(prop)
        else:
            sub_class_name = u2C(prop)
        sub_class_meta = gen_class_meta(sub_class_name, dialect, sub_value, prefix)
        field_class_meta = sub_class_meta
    else:
        print "unknown sub_value_type %s , prop=%s" % sub_value_type, prop
        exit(-1)
    field_meta = FieldMeta(field_name, value_type, field_generic_type, prop,field_class_meta)

    return field_meta