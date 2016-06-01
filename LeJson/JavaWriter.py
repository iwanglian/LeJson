import os

from LeUtils import LeUtils, gen_desc


def is_java_output_expired(input_file_path, out_path, base_class_name):
    body_path = os.path.join(out_path, base_class_name + '.java')
    if not os.path.exists(body_path):
        return True
    body_time = os.path.getctime(body_path)

    input_time = os.path.getctime(input_file_path)

    if input_time > body_time:
        return True
    else:
        return False


def write_java_all_class_meta(base_class_meta, path, package):
    java_fp = open(os.path.join(path, LeUtils.s_base_class_name + ".java"), 'w')
    java_fp.write(gen_desc())
    str = "package %s;\n\n" % package
    dialect = LeUtils.s_dialect
    str += 'import java.util.List;\n'
    if dialect == 'gs':
        str += 'import com.google.gson.annotations.SerializedName;'
    elif dialect == 'le':
        str += 'import com.github.iwanglian.lemodel.SerializedName;'
    elif dialect == 'fj':
        str += 'import com.alibaba.fastjson.annotation.JSONField;'
    elif dialect == 'jc':
        str += 'import com.fasterxml.jackson.annotation.JsonProperty;'
    elif dialect == 'ls':
        str += 'import com.bluelinelabs.logansquare.annotation.JsonField;\nimport com.bluelinelabs.logansquare.annotation.JsonObject;'
    elif dialect == 'jo':
        str += '''import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

'''

    str += '\n'
    java_fp.write(str);

    write_java_class_meta(base_class_meta, java_fp)
    java_fp.close()

    print '%s OK!' % java_fp.name

def write_java_class_meta(class_meta, java_fp):
    java_fp.write(class_meta.gen_java_class_meta())
