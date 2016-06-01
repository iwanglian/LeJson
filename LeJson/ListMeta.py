from LeUtils import LeUtils, \
    s_objc_keyword_replace, s_objc_dialect_list, \
    u2C, u2c, leType, str_with_suf, str_with_indent, \
    s_list_types, s_dict_types, s_number_types, s_java_simple_type_object_map, \
    s_objc_number_type_str_map, s_objc_simple_type_object_map, \
    s_java_number_type_str_map, s_java_jo_simple_type_put_map


class ListMeta:
    def __init__(self, list_type):
        self.list_type = list_type
        self.list_meta = None
        self.dict_meta = None
        self.parent_field_meta = None
        self.parent_list_meta = None

    def get_near_field_meta(self):
        if self.parent_field_meta:
            return self.parent_field_meta
        elif self.parent_list_meta:
            return self.parent_list_meta.get_near_field_meta()
        else:
            return None

    def get_objc_type_str(self):
        type_str = ''
        if self.list_type in s_list_types:
            type_str = "NSMutableArray"
        elif self.list_type in s_dict_types:
            type_str = self.dict_meta.get_objc_class_name()
        else:
            type_str = s_objc_simple_type_object_map[self.list_type]
        return type_str

    def get_objc_final_type_str(self):
        type_str = ''
        if self.list_type in s_list_types:
            type_str = self.list_meta.get_objc_final_type_str()
        else:
            type_str = self.get_objc_type_str()
        return type_str

    def get_java_type_str(self):
        if self.list_type in s_java_simple_type_object_map:
            return 'List<%s>' % s_java_simple_type_object_map[self.list_type]
        elif self.list_type in s_dict_types:
            return 'List<%s>' % self.dict_meta.get_java_class_name()
        elif self.list_type in s_list_types:
            return 'List<%s>' % self.list_meta.get_java_type_str()
        else:
            raise Exception('list type error: %s' % self.list_type)

    def gen_java_list_meta(self):
        str = ""
        if self.list_type in s_list_types:
            str = self.list_meta.gen_java_list_meta()
        elif self.list_type in s_dict_types:
            str = self.dict_meta.gen_java_class_meta()
        return str

    def gen_java_jo_j2o(self, inner):
        str = ''
        if self.list_type in s_java_simple_type_object_map:
            str += '''
{type} item = {jsonArray}.{jo_type}({i});
{list}.add(item);
'''.format(type=s_java_simple_type_object_map[self.list_type],
           jo_type=s_java_jo_simple_type_put_map[self.list_type],
           jsonArray=str_with_suf('jsonArray', inner),
           i=str_with_suf('i', inner), list=str_with_suf('list', inner))
        elif self.list_type in s_dict_types:
            str += '''
JSONObject jsonObj = {jsonArray}.optJSONObject(i);
if(jsonObj!=null) {{
    {class_name} item = {class_name}.objectFromJSON(jsonObj);
    {list}.add(item);
}}
'''.format(class_name=self.dict_meta.get_java_class_name(), jsonArray=str_with_suf('jsonArray', inner),
           list=str_with_suf('list', inner), )
        elif self.list_type in s_list_types:
            type_str = self.list_meta.get_java_type_str()
            statement = self.list_meta.gen_java_jo_j2o(inner + 1)
            statement = str_with_indent(statement, 1)
            str += '''
JSONArray {jsonArray1} = {jsonArray}.optJSONArray({i});
{type} {list1} = new ArrayList<>();
for (int {i1} = 0; {i1} < {jsonArray1}.length(); {i1}++) {{{statement}}}
{list}.add({list1});
'''.format(jsonArray1=str_with_suf('jsonArray', inner + 1), i=str_with_suf('i', inner),
           type=type_str, jsonArray=str_with_suf('jsonArray', inner),
           list1=str_with_suf('list', inner + 1), i1=str_with_suf('i', inner + 1),
           statement=statement,
           list=str_with_suf('list', inner))

        return str

    def gen_java_jo_o2j(self, inner):
        str = ''
        if self.list_type in s_java_simple_type_object_map:
            str += '''
for ({type} item : {list}) {{
    {jsonArray}.put(item);
}} '''.format(type=s_java_simple_type_object_map[self.list_type],
              list=str_with_suf('list', inner), jsonArray=str_with_suf('jsonArray', inner)
              )
        elif self.list_type in s_dict_types:
            str += '''
for ({type} item : {list}) {{
    JSONObject jsonObj = {class_name}.JSONFromObject(item);
    {jsonArray}.put(jsonObj);
}} '''.format(class_name=self.dict_meta.get_java_class_name(), type=self.dict_meta.get_java_class_name(),
              list=str_with_suf('list', inner), jsonArray=str_with_suf('jsonArray', inner)
              )
        elif self.list_type in s_list_types:
            type_str = self.list_meta.get_java_type_str()
            statement = self.list_meta.gen_java_jo_o2j(inner + 1)
            statement = str_with_indent(statement, 1)
            str += '''
for ({type} {list1} : {list}) {{
    JSONArray {jsonArray1} = new JSONArray();{statement}
    {jsonArray}.put({jsonArray1});
}} '''.format(jsonArray1=str_with_suf('jsonArray', inner + 1), i=str_with_suf('i', inner),
              type=type_str, jsonArray=str_with_suf('jsonArray', inner),
              list1=str_with_suf('list', inner + 1), i1=str_with_suf('i', inner + 1),
              statement=statement, list2=str_with_suf('list', inner + 2),
              list=str_with_suf('list', inner))

        return str
