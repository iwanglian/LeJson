from LeUtils import LeUtils, \
    s_objc_keyword_replace, s_objc_dialect_list, \
    u2C, u2c, leType, str_with_indent, \
    s_list_types, s_dict_types


class DictMeta:
    def __init__(self):
        self.field_meta_array = []
        self.parent_field_meta = None
        self.parent_list_meta = None

    def is_base(self):
        return not self.parent_field_meta and not self.parent_list_meta

    def get_near_field_meta(self):
        if self.parent_field_meta:
            return self.parent_field_meta
        elif self.parent_list_meta:
            return self.parent_list_meta.get_near_field_meta()
        else:
            return None

    def get_objc_class_name(self):
        near_field_meta = self.get_near_field_meta()
        if near_field_meta and near_field_meta.parent_dict_meta:
            return near_field_meta.parent_dict_meta.get_objc_class_name() + '_' + u2C(near_field_meta.orig)
        else:
            return LeUtils.s_base_class_name

    def get_java_class_name(self):
        near_field_meta = self.get_near_field_meta()
        if near_field_meta:
            return u2C(near_field_meta.orig)
        else:
            return LeUtils.s_base_class_name

    def gen_objc_head(self):
        str = ""
        super_class_name = "NSObject"
        if LeUtils.s_dialect == "mt":
            super_class_name = "MTLModel <MTLJSONSerializing>"
        str += "@interface %s : %s \n" % (self.get_objc_class_name(), super_class_name)

        for field_meta in self.field_meta_array:
            str += field_meta.gen_objc_property() + "\n"
        str += "@end\n\n\n"

        return str

    def gen_objc_body(self):
        str = ""
        str += '@implementation %s\n\n' % self.get_objc_class_name()
        str += self.gen_objc_body_init()
        if LeUtils.s_dialect == 'mj':
            str += self.gen_objc_body_mj_class_in_array()
            str += self.gen_objc_body_replace_key()
        elif LeUtils.s_dialect == 'yy':
            str += self.gen_objc_body_yy_class_in_array()
            str += self.gen_objc_body_replace_key()
        elif LeUtils.s_dialect == 'mt':
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
        for field_meta in self.field_meta_array:
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
        for field_meta in self.field_meta_array:
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
        for field_meta in self.field_meta_array:
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
''' % self.s_objc_method_replace_map[LeUtils.s_dialect]

        for field_meta in self.field_meta_array:
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
''' % self.s_objc_method_replace_map[LeUtils.s_dialect]

        for field_meta in self.field_meta_array:
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
        for field_meta in self.field_meta_array:
            if field_meta.field_type in s_list_types:
                if field_meta.dict_meta:
                    field_str = field_meta.gen_objc_mt_array_generic()
                    str += field_str + '\n'
            elif field_meta.field_type in s_dict_types:
                field_str = field_meta.gen_objc_mt_value_generic()
                str += field_str + '\n'

        return str

    def gen_java_class_meta(self):
        str_static = ''
        if not self.is_base():
            str_static = 'static '
        str = '\npublic %sclass %s {\n' % (str_static, self.get_java_class_name())
        if LeUtils.s_dialect in ['ls']:
            str = '@JsonObject\n' + str

        for field_meta in self.field_meta_array:
            field_str = ''
            if LeUtils.s_dialect in ['gs', 'le']:
                field_str = field_meta.gen_java_gs_declare()
            elif LeUtils.s_dialect in ['fj']:
                field_str = field_meta.gen_java_fj_declare()
            elif LeUtils.s_dialect in ['jc']:
                field_str = field_meta.gen_java_ja_declare()
            elif LeUtils.s_dialect in ['ls']:
                field_str = field_meta.gen_java_ls_declare()
            elif LeUtils.s_dialect in ['jo']:
                field_str = field_meta.gen_java_jo_declare()

            str += field_str + '\n'

        if LeUtils.s_dialect in ['jo']:
            if self.is_base():
                if not LeUtils.s_no_serialize:
                    str += self.gen_java_jo_o2s()
                if not LeUtils.s_no_deserialize:
                    str += self.gen_java_jo_s2o()
            method_str =''
            if not LeUtils.s_no_serialize:
                method_str += self.gen_java_jo_jsonfromobject()
            if not LeUtils.s_no_deserialize:
                method_str += self.gen_java_jo_objectfromjson()
            if method_str:
                str += str_with_indent(method_str, 1)

        if not LeUtils.s_java_public:
            for field_meta in self.field_meta_array:
                field_str = field_meta.gen_java_gs_getter_setter()
                str += field_str + '\n'

        for field_meta in self.field_meta_array:
            field_str = ""
            if field_meta.field_type in s_list_types:
                field_str += field_meta.list_meta.gen_java_list_meta()
            elif field_meta.field_type in s_dict_types:
                field_str += field_meta.dict_meta.gen_java_class_meta()
            str += '\t'.join(field_str.splitlines(True))
        str += '}\n\n'
        return str

    def gen_java_jo_objectfromjson(self):
        str = ''
        str += '''
public static {class_name} objectFromJSON(JSONObject jsonObject) {{
    {class_name} object = new {class_name}(); '''.format(class_name=self.get_java_class_name())
        field_str = ''
        for field_meta in self.field_meta_array:
            field_str += field_meta.gen_java_jo_j2o()
        field_str += '\nreturn object;'
        str += str_with_indent(field_str, 1)
        str += '\n}\n'
        return str

    def gen_java_jo_jsonfromobject(self):
        str = ''
        str += '''
public static JSONObject JSONFromObject({class_name} object) {{
    JSONObject jsonObject = new JSONObject();
    try {{ '''.format(class_name=self.get_java_class_name())
        field_str = ''
        for field_meta in self.field_meta_array:
            field_str += str_with_indent(field_meta.gen_java_jo_o2j(), 1)
        field_str += '''
} catch (JSONException e) {
    e.printStackTrace();
}

return jsonObject; '''
        str += str_with_indent(field_str, 1)
        str += '\n}\n'
        return str

    def gen_java_jo_s2o(self):
        str = '''
    public static {class_name} objectFromString(String string) throws JSONException {{
        JSONObject jsonObject = new JSONObject(string);
        return objectFromJSON(jsonObject);
    }}
'''.format(class_name=self.get_java_class_name())
        return str

    def gen_java_jo_o2s(self):
        str = '''
    public static String stringFromObject({class_name} object) throws JSONException {{
        JSONObject jsonObject = JSONFromObject(object);
        return jsonObject.toString();
    }}
'''.format(class_name=self.get_java_class_name())
        return str
