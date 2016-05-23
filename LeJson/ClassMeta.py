from FieldMeta import FieldMeta


class ClassMeta:
    def __init__(self, name, dialect):
        self.name = name
        self.field_meta_list = []
        self.dialect = dialect
        self.is_base = False

    def add_field(self, field_meta):
        self.field_meta_list.append(field_meta)

    def gen_objc_head(self):
        str = ""
        super_class_name = "NSObject"
        if self.dialect == "mt":
            super_class_name = "MTLModel <MTLJSONSerializing>"
        str += "@interface %s : %s \n" % (self.name, super_class_name)

        for field_meta in self.field_meta_list:
            str += field_meta.gen_objc_property() + "\n"
        str += "@end\n\n\n"

        return str

    def gen_objc_body(self):
        str = ""
        str += '@implementation %s\n\n' % self.name
        str += self.gen_objc_body_init()
        if self.dialect == 'mj':
            str += self.gen_objc_body_mj_class_in_array()
            str += self.gen_objc_body_replace_key()
        elif self.dialect == 'yy':
            str += self.gen_objc_body_yy_class_in_array()
            str += self.gen_objc_body_replace_key()
        elif self.dialect == 'mt':
            str += self.gen_objc_body_mt_replace_key()
            str += self.gen_objc_body_mt_generic()

        str += "@end\n\n\n"
        return str

    def gen_objc_body_init(self):
        str = ""
        str += '''
-(instancetype)init{
    self = [super init];
    if (self) {
'''
        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_objc_init()
            if field_str:
                str += '        ' + field_str + '\n'
        str += '''
    }
    return self;
}
    '''
        return str

    def gen_objc_body_mj_class_in_array(self):
        str = ""
        str += '''
+ (NSDictionary *)mj_objectClassInArray{
   return @{
'''
        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_objc_mj_class_in_array()
            if field_str:
                str += '        ' + field_str + '\n'
        str += '''
    };
}
'''
        return str

    def gen_objc_body_yy_class_in_array(self):
        str = ""
        str += '''
+ (NSDictionary *)modelContainerPropertyGenericClass{
   return @{
'''
        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_objc_mj_class_in_array()
            if field_str:
                str += '        ' + field_str + '\n'
        str += '''
    };
}
'''
        return str

    s_objc_method_replace_map = {'mj': 'mj_replacedKeyFromPropertyName',
                                 'mt': 'JSONKeyPathsByPropertyKey',
                                 'yy': 'modelCustomPropertyMapper'
                                 }

    def gen_objc_body_replace_key(self):
        str = ""
        str += '''

+ (NSDictionary *)%s{
   return @{
''' % self.s_objc_method_replace_map[self.dialect]

        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_objc_mj_relpace_key()
            if field_str:
                str += '        ' + field_str + '\n'
        str += '''
    };
}
'''
        return str

    def gen_objc_body_mt_replace_key(self):
        str = ""
        str += '''

+ (NSDictionary *)%s{
   return @{
''' % self.s_objc_method_replace_map[self.dialect]

        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_objc_mt_relpace_key()
            if field_str:
                str += '        ' + field_str + '\n'
        str += '''
    };
}
'''
        return str

    def gen_objc_body_mt_generic(self):
        str = ""
        for field_meta in self.field_meta_list:
            if field_meta.type in FieldMeta.s_list_types:
                if field_meta.class_meta:
                    field_str = field_meta.gen_objc_mt_array_generic()
                    str += field_str + '\n'
            elif field_meta.type in FieldMeta.s_dict_types:
                field_str = field_meta.gen_objc_mt_value_generic()
                str += field_str + '\n'

        return str

    def gen_java_class_meta(self):
        str_static = ''
        if not self.is_base:
            str_static = 'static '
        str = '\npublic %sclass %s {\n' % (str_static, self.name)
        if self.dialect in ['ls']:
            str ='@JsonObject\n' + str

        for field_meta in self.field_meta_list:
            field_str = ''
            if self.dialect in ['gs']:
                field_str = field_meta.gen_java_gs_declare()
            elif self.dialect in ['fj']:
                field_str = field_meta.gen_java_fj_declare()
            elif self.dialect in ['jc']:
                field_str = field_meta.gen_java_ja_declare()
            elif self.dialect in ['ls']:
                field_str = field_meta.gen_java_ls_declare()

            str += field_str + '\n'

        for field_meta in self.field_meta_list:
            field_str = field_meta.gen_java_gs_getter_setter()
            str += field_str + '\n'

        for field_meta in self.field_meta_list:
            field_str = ""
            if field_meta.generic_type in FieldMeta.s_list_types:
                field_str += field_meta.class_meta.gen_java_list_meta()
            elif field_meta.generic_type in FieldMeta.s_dict_types:
                field_str += field_meta.class_meta.gen_java_class_meta()
            str += '\t'.join(field_str.splitlines(True))
        str += '}\n\n'
        return str

    def gen_java_list_meta(self):
        field_meta = self.field_meta_list[0]
        str =""
        if field_meta.generic_type in FieldMeta.s_list_types:
            str = field_meta.class_meta.gen_java_list_meta()
        elif field_meta.generic_type in FieldMeta.s_dict_types:
            str = field_meta.class_meta.gen_java_class_meta()
        return str