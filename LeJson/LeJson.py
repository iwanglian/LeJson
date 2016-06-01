# -*- coding: utf-8 -*-
from JsonParser import gen_dict_meta

__author__ = 'alickwang'

from JsonParser import gen_dict_meta
from LeUtils import LeUtils, cap, s_objc_dialect_list, s_java_dialect_list
from ObjcWriter import write_objc_all_class_meta, is_objc_output_expired
from JavaWriter import write_java_all_class_meta, is_java_output_expired

import argparse
import json, re
import os


def get_json_list(dir):
    json_list = []
    list = os.listdir(dir)
    for line in list:
        filepath = os.path.join(dir, line)
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == '.json':
            json_list.append(filepath)
    return json_list


def write_class(input_file_path, base_class_name, out_path, package):
    str = ""
    input_file = open(input_file_path)
    for line in input_file.readlines():
        string = re.sub('([^:]//.*"?$)|(/\*(.*?)\*/)', '', line)
        str = str + string
    input_file.close()

    base_object = json.loads(str)
    base_dict_meta = gen_dict_meta(base_object)

    if LeUtils.s_dialect in s_objc_dialect_list:
        write_objc_all_class_meta(base_dict_meta, output_path)
    elif LeUtils.s_dialect in s_java_dialect_list:
        write_java_all_class_meta(base_dict_meta, output_path, package)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='自动生成JSON模型类')
    parser.add_argument('input', metavar='input', nargs='*',
                        help='json文件路径,如果是目录名,则处理目录下所有一级.json文件;默认为当前路径')
    parser.add_argument('-d', dest='dialect', choices=['mj', 'mt', 'yy', 'jo', 'gs', 'jc', 'fj', 'ls', 'le'],
                        required=True,
                        help='采用的解析方法,必填.')
    parser.add_argument('-o', dest='output_path', help='输出路径,默认为当前路径')
    parser.add_argument('-f', dest='force_update', action='store_true',
                        help='强制更新,即使json未变化 ,也生成新的目标模型')
    # parser.add_argument('--name', dest='class_name', default="",
    #                     help='输出的结果类名,针对单文件时有效')
    parser.add_argument('--fp', dest='field_prefix', default='', help='生成字段的前缀')
    parser.add_argument('--cp', dest='class_prefix', default='',
                        help='输出结果类名的前缀')
    # parser.add_argument('--cs', dest='class_suffix', default='',
    #                     help='输出结果类名的后缀')
    parser.add_argument('--pkg', dest='package', help='如果是Java类,需要指定其package;默认会根据 OUTPUT_PATH 计算')
    # parser.add_argument('-r', action='store_true',
    #                     help='reuse model ,if key and value type matched ,reuse it instead create one')
    args = parser.parse_args()

    input_file_list = []
    if len(args.input) == 0:
        input_file_list = get_json_list('.')
    else:
        for arginput in args.input:
            if os.path.isdir(arginput):
                input_file_list += get_json_list(arginput)
            else:
                input_file_list.append(arginput)

    if len(input_file_list) == 0:
        raise Exception('no input file')

    output_path = args.output_path
    if not args.output_path:
        output_path = '.'

    package = args.package

    if args.dialect in s_java_dialect_list:
        if not args.package:
            output_abs_path = os.path.abspath(output_path)
            sep = '/src/main/java/'
            if os.name == 'nt':
                sep = '\\src\\main\\java\\'
            output_abs_path_parts = output_abs_path.split(sep)
            if len(output_abs_path_parts) < 2:
                raise Exception("Not assign a Package for Java")
            else:
                package = output_abs_path_parts[-1].replace('/', '.').replace('\\', '.')

    for input_file_path in input_file_list:
        json_name = os.path.splitext(os.path.basename(input_file_path))[0]
        base_class_name = cap(json_name)
        if args.class_prefix:
            base_class_name = args.class_prefix + base_class_name

        if not args.force_update:
            is_expired = False
            if args.dialect in s_java_dialect_list:
                is_expired = is_java_output_expired(input_file_path, output_path, base_class_name)
            else:
                is_expired = is_objc_output_expired(input_file_path, output_path, base_class_name)

            if not is_expired:
                print '%s/%s is latest model, continue!' % (output_path, base_class_name)
                continue

        LeUtils.s_field_prefix = args.field_prefix
        LeUtils.s_dialect = args.dialect
        LeUtils.s_base_class_name = base_class_name

        write_class(input_file_path, base_class_name, output_path, package)
