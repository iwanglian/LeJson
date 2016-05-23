# -*- coding: utf-8 -*-
__author__ = 'alickwang'

import types

from LeUtils import u2C, leType,cap


class FieldMeta:
    s_number_types = [types.IntType, types.FloatType, types.BooleanType, types.LongType]
    s_string_types = [types.StringType, types.UnicodeType]
    s_list_types = [types.ListType]
    s_dict_types = [types.DictType]
    s_objc_number_type_str_map = {types.IntType: 'int',
                                  types.FloatType: 'float',
                                  types.BooleanType: 'BOOL',
                                  types.LongType: 'long',
                                  }
    s_java_number_type_str_map = {types.IntType: 'int',
                                  types.FloatType: 'float',
                                  types.BooleanType: 'boolean',
                                  types.LongType: 'long',
                                  }

    s_java_number_type_object_map = {types.IntType: 'Integer',
                                     types.FloatType: 'Double',
                                     types.BooleanType: 'Boolean',
                                     types.LongType: 'Long',
                                     }

    def __init__(self, name, type, generic_type, orig, class_meta=None):
        self.name = name;
        self.type = type;
        self.generic_type = generic_type;
        self.orig = orig;
        self.class_meta = class_meta;

    def get_objc_generic(self):
        if self.generic_type in self.s_number_types:
            return 'NSNumber'
        elif self.generic_type in self.s_string_types:
            return 'NSString'
        elif self.generic_type in self.s_list_types:
            return 'NSMutableArray'
        elif self.generic_type in self.s_dict_types:
            return self.class_meta.name
        else:
            return ''

    def get_objc_final_generic(self):
        if self.generic_type in self.s_number_types:
            return 'NSNumber'
        elif self.generic_type in self.s_string_types:
            return 'NSString'
        elif self.generic_type in self.s_list_types:
            return self.class_meta.field_meta_list[0].get_objc_final_generic()
        elif self.generic_type in self.s_dict_types:
            return self.class_meta.name
        else:
            return ''

    def gen_objc_property(self):
        retain_str = "retain"
        if self.type in self.s_number_types:
            retain_str = "assign"

        type_str = ""
        if self.type in self.s_number_types:
            type_str = self.s_objc_number_type_str_map[self.type]
        elif self.type in self.s_string_types:
            type_str = "NSString*"
        elif self.type in self.s_list_types:
            type_str = "NSMutableArray<%s*>* " % self.get_objc_generic()
        elif self.type in self.s_dict_types:
            type_str = "%s* " % self.get_objc_generic()
        else:
            print "unknown type %s" % self.type
            exit(-1)

        str = "@property (nonatomic, %s) %s %s;" % (retain_str, type_str, self.name)
        return str

    def gen_objc_init(self):
        str = ""
        if self.type in self.s_list_types:
            str = "self.%s = [[NSMutableArray alloc] init];" % self.name
        elif self.type in self.s_dict_types:
            str = "self.%s= [[%s alloc] init];" % (self.name, self.get_objc_generic())
        return str

    def gen_objc_mj_class_in_array(self):
        str = ""
        if self.type in self.s_list_types:
            str = '@"%s" : @"%s",' % (self.name, self.get_objc_final_generic())
        return str

    def gen_objc_mj_relpace_key(self):
        str = ""
        if self.name != self.orig:
            str = '@"%s" : @"%s",' % (self.name, self.orig)
        return str

    def gen_objc_mt_relpace_key(self):
        str = '@"%s" : @"%s",' % (self.name, self.orig)
        return str

    def gen_objc_mt_value_generic(self):
        str =''
        if self.type in self.s_list_types:
            str = '''
+ (NSValueTransformer *)%sJSONTransformer {
    return [MTLJSONAdapter dictionaryTransformerWithModelClass:%s.class];
}
''' % (self.name, self.get_objc_generic())
        return str

    def gen_objc_mt_array_generic(self):
        str = '''
+ (NSValueTransformer *)%sJSONTransformer {
    return [MTLJSONAdapter arrayTransformerWithModelClass:%s.class];
}
''' % (self.name, self.get_objc_final_generic())
        return str

    def get_java_generic(self):
        if self.generic_type in self.s_number_types:
            return self.s_java_number_type_object_map[self.generic_type]
        elif self.generic_type in self.s_string_types:
            return 'String'
        elif self.generic_type in self.s_list_types:
            return 'List<%s>' % self.class_meta.field_meta_list[0].get_java_generic()
        elif self.generic_type in self.s_dict_types:
            return self.class_meta.name
        else:
            return ''

    def get_java_type_str(self):
        if self.type in self.s_number_types:
            type_str = self.s_java_number_type_str_map[self.type]
        elif self.type in self.s_string_types:
            type_str = "String"
        elif self.type in self.s_list_types:
            type_str = "List<%s> " % self.get_java_generic()
        elif self.type in self.s_dict_types:
            type_str = "%s " % self.get_objc_generic()
        else:
            raise Exception("unknown type %s" % self.type)
        return type_str

    def gen_java_gs_declare(self):
        type_str = self.get_java_type_str()
        str = ''
        str += '\t@SerializedName("%s")\n' % self.orig
        str += '\tprivate %s %s; ' % (type_str, self.name)
        return str

    def gen_java_fj_declare(self):
        type_str = self.get_java_type_str()
        str = ''
        str += '\t@JSONField(name = "%s")\n' % self.orig
        str += '\tprivate %s %s; ' % (type_str, self.name)
        return str

    def gen_java_ja_declare(self):
        type_str = self.get_java_type_str()
        str = ''
        str += '\t@JsonProperty("%s")\n' % self.orig
        str += '\tprivate %s %s; ' % (type_str, self.name)
        return str

    def gen_java_ls_declare(self):
        type_str = self.get_java_type_str()
        str = ''
        str += '\t@JsonField(name = "%s")\n' % self.orig
        str += '\tprivate %s %s; ' % (type_str, self.name)
        return str

    def gen_java_gs_getter_setter(self):
        cname = cap(self.name)
        type_str = self.get_java_type_str()
        str = '''
    public %s get%s() {
        return %s;
    }

    public void set%s(%s %s) {
        this.%s = %s;
    } ''' % (type_str, cname, self.name, cname, type_str, self.name, self.name, self.name)
        return str
