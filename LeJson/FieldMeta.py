import types

from LeUtils import LeUtils, \
    s_objc_keyword_replace, s_objc_dialect_list, \
    u2C, u2c, leType, str_with_suf, cap, str_with_indent, \
    s_list_types, s_dict_types, s_number_types, s_string_types, s_java_simple_type_object_map, \
    s_objc_number_type_str_map, s_objc_simple_type_object_map, s_java_number_type_str_map, s_java_jo_simple_type_put_map


class FieldMeta:
    def __init__(self, name, field_type, orig):
        self.name = name
        self.field_type = field_type
        self.orig = orig
        self.dict_meta = None
        self.list_meta = None
        self.parent_dict_meta = None

    def get_objc_type_str(self):
        type_str = ""
        if self.field_type in s_number_types:
            type_str = s_objc_number_type_str_map[self.field_type]
        elif self.field_type in s_string_types:
            type_str = "NSString*"
        elif self.field_type in s_list_types:
            if self.list_meta.list_type in s_list_types:
                type_str = "NSMutableArray<NSMutableArray*>* "
            elif self.list_meta.list_type in s_dict_types:
                type_str = "NSMutableArray<%s*>* " % self.list_meta.dict_meta.get_objc_class_name()
            else:
                type_str = "NSMutableArray<%s*>* " % s_objc_simple_type_object_map[self.list_meta.list_type]

        elif self.field_type in s_dict_types:
            type_str = "%s* " % self.dict_meta.get_objc_class_name()
        else:
            raise Exception("unknown type %s" % self.field_type)
        return type_str

    def gen_objc_property(self):
        retain_str = "retain"
        if self.field_type in s_number_types:
            retain_str = "assign"

        type_str = self.get_objc_type_str()
        str = "@property (nonatomic, {retain}) {type} {name};".format(retain=retain_str, type=type_str, name=self.name)
        return str

    def gen_objc_init(self):
        str = ""
        if self.field_type in s_list_types:
            str = "self.%s = [[NSMutableArray alloc] init];" % self.name
        elif self.field_type in s_dict_types:
            str = "self.%s= [[%s alloc] init];" % (self.name, self.dict_meta.get_objc_class_name())
        return str

    def gen_objc_mj_class_in_array(self):
        str = ""
        if self.field_type in s_list_types:
            str = '@"%s" : @"%s",' % (self.name, self.list_meta.get_objc_final_type_str())
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
        str = ''
        if self.field_type in s_list_types:
            str = '''
+ (NSValueTransformer *)%sJSONTransformer {
    return [MTLJSONAdapter dictionaryTransformerWithModelClass:%s.class];
}
''' % (self.name, self.list_meta.get_objc_final_type_str())
        return str

    def gen_objc_mt_array_generic(self):
        str = '''
+ (NSValueTransformer *)%sJSONTransformer {
    return [MTLJSONAdapter arrayTransformerWithModelClass:%s.class];
}
''' % (self.name, self.list_meta.get_objc_final_type_str())
        return str

    def get_java_type_str(self):
        if self.field_type in s_number_types:
            type_str = s_java_number_type_str_map[self.field_type]
        elif self.field_type in s_string_types:
            type_str = "String"
        elif self.field_type in s_list_types:
            type_str = self.list_meta.get_java_type_str()
        elif self.field_type in s_dict_types:
            type_str = self.dict_meta.get_java_class_name()
        else:
            raise Exception("unknown type %s" % self.field_type)
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

    def gen_java_jo_declare(self):
        type_str = self.get_java_type_str()
        str = ''
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

    def gen_java_jo_j2o(self):
        str = ''
        if self.field_type in s_java_jo_simple_type_put_map:
            str = '''
object.%s = jsonObject.%s("%s");''' % (
                self.name, s_java_jo_simple_type_put_map[self.field_type], self.orig)
        elif self.field_type in s_dict_types:
            str = '''
if (jsonObject.optJSONObject("%s") != null) {
    JSONObject jsonObj = jsonObject.optJSONObject("%s");
    object.%s = %s.objectFromJSON(jsonObj);
}
''' % (self.name, self.orig, self.name, self.dict_meta.get_java_class_name())
        elif self.field_type in s_list_types:
            type_str = self.get_java_type_str()

            str = '''
if (jsonObject.optJSONArray("%s") != null) {
    JSONArray jsonArray = jsonObject.optJSONArray("%s");
    %s list = new ArrayList<>();
    for (int i = 0; i < jsonArray.length(); i++) {%s    }
    object.%s = list;
}
''' % (self.orig, self.orig, type_str, str_with_indent(self.list_meta.gen_java_jo_j2o(0), 2), self.name)

        return str

    def gen_java_jo_o2j(self):
        str = ''
        if self.field_type in s_java_jo_simple_type_put_map:
            str = '''
jsonObject.put("{orig}", object.{name});'''.format(orig=self.orig, name=self.name)
        elif self.field_type in s_dict_types:
            str = '''
if(object.{name} != null){{
    JSONObject jsonObj = {class_name}.JSONFromObject(object.{name});
    jsonObject.put("{orig}",jsonObj);
}} '''.format(name=self.name, orig=self.orig, class_name=self.dict_meta.get_java_class_name())
        elif self.field_type in s_list_types:
            type_str = self.get_java_type_str()
            statement = str_with_indent(self.list_meta.gen_java_jo_o2j(0), 1)
            str = '''
if(object.{name}!=null){{
    {type} list = object.{name};
    JSONArray jsonArray = new JSONArray();{statement}
    jsonObject.put("{orig}",jsonArray);
}} '''.format(orig=self.orig, type=type_str, statement=statement, name=self.name)

        return str
