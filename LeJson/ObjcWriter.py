import os

from LeUtils import LeUtils, gen_desc, s_objc_dialect_list, s_dict_types, s_list_types
from FieldMeta import FieldMeta


def is_objc_output_expired(input_file_path, out_path, base_class_name):
    head_path = os.path.join(out_path, base_class_name + '.h')
    body_path = os.path.join(out_path, base_class_name + '.m')
    if not os.path.exists(head_path) or not os.path.exists(body_path):
        return True
    head_time = os.path.getctime(head_path)
    body_time = os.path.getctime(body_path)

    input_time = os.path.getctime(input_file_path)

    if input_time > head_time or input_time > body_time:
        return True
    else:
        return False


def is_objc_output_exist(out_path, base_class_name):
    head_path = os.path.join(out_path, base_class_name + '.h')
    body_path = os.path.join(out_path, base_class_name + '.m')
    return os.path.exists(head_path) and os.path.exists(body_path)


def write_objc_all_class_meta(base_class_meta, path):
    head_fp = open(os.path.join(path, LeUtils.s_base_class_name + ".h"), 'w')
    body_fp = open(os.path.join(path, LeUtils.s_base_class_name + ".m"), 'w')

    desc = gen_desc()

    head_fp.write(desc)
    body_fp.write(desc)

    str = "#import <Foundation/Foundation.h>\n"
    if LeUtils.s_dialect == 'mt':
        str += "#import <Mantle/Mantle.h>\n"
    str += "\n"

    str = write_objc_class_declare(base_class_meta, str)
    str += "\n"

    head_fp.write(str)
    head_fp.flush()

    str = '#import "%s.h"\n\n' % LeUtils.s_base_class_name
    body_fp.write(str)
    body_fp.flush()

    write_objc_class_meta(base_class_meta, head_fp, body_fp)

    head_fp.close()
    body_fp.close()

    print '%s OK!' % head_fp.name
    print '%s OK!' % body_fp.name


def write_objc_class_declare(class_meta, out_str):
    for field_meta in class_meta.field_meta_array:
        if field_meta.field_type in s_dict_types:
            out_str += "@class %s;\n" % field_meta.dict_meta.get_objc_class_name()
            out_str = write_objc_class_declare(field_meta.dict_meta, out_str)
        elif field_meta.field_type in s_list_types:
            out_str = write_objc_list_declare(field_meta.list_meta, out_str)
    return out_str


def write_objc_list_declare(list_meta, out_str):
    if list_meta.list_type in s_list_types:
        out_str = write_objc_list_declare(list_meta.list_meta, out_str)
    elif list_meta.list_type in s_dict_types:
        out_str += "@class %s;\n" % list_meta.dict_meta.get_objc_class_name()
        out_str = write_objc_class_declare(list_meta.dict_meta, out_str)
    return out_str


def write_objc_class_meta(class_meta, head_fp, body_fp):
    head_str = class_meta.gen_objc_head()
    head_fp.write(head_str)
    head_fp.flush()

    body_str = class_meta.gen_objc_body()
    body_fp.write(body_str)
    body_fp.flush()

    for field_meta in class_meta.field_meta_array:
        if field_meta.field_type in s_list_types:
            write_objc_list_meta(field_meta.list_meta, head_fp, body_fp)
        elif field_meta.field_type in s_dict_types:
            write_objc_class_meta(field_meta.dict_meta, head_fp, body_fp)


def write_objc_list_meta(list_meta, head_fp, body_fp):
    if list_meta.list_type in s_list_types:
        write_objc_list_meta(list_meta.list_meta, head_fp, body_fp)
    elif list_meta.list_type in s_dict_types:
        write_objc_class_meta(list_meta.dict_meta, head_fp, body_fp)
