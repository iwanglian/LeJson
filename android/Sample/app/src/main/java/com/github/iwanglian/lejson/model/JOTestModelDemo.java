package com.github.iwanglian.lejson.model;


import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by alick on 5/31/16.
 */
public class JOTestModelDemo {
    private int keyInt;
    private long keyLong;
    private double keyFloat;
    private double keyDouble;
    private String keyString;
    private KeyObj keyObj;
    private List<Integer> keyIntList;
    private List<List<Integer>> keyIntListList;
    private List<String> keyStringList;
    private List<List<String>> keyStringListList;
    private List<KeyObjList> keyObjList;
    private List<List<KeyObjListList>> keyObjListList;

    public static String stringFromList(List<JOTestModelDemo> list) throws JSONException {
        JSONArray jsonArray = JSONFromList(list);
        return jsonArray.toString();
    }

    public static List<JOTestModelDemo> listFromString(String string) throws JSONException {
        JSONArray jsonArray = new JSONArray(string);
        return listFromJSON(jsonArray);
    }

    public static List<JOTestModelDemo> listFromJSON(JSONArray jsonArray) {
        List<JOTestModelDemo> list = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++) {
            JSONObject jsonObject = jsonArray.optJSONObject(i);
            if (jsonObject != null) {
                JOTestModelDemo object = objectFromJSON(jsonObject);
                list.add(object);
            }
        }
        return list;
    }

    public static JSONArray JSONFromList(List<JOTestModelDemo> list) throws JSONException {
        JSONArray jsonArray = new JSONArray();
        for (JOTestModelDemo object : list) {
            JSONObject jsonObject = JSONFromObject(object);
            jsonArray.put(jsonObject);
        }
        return jsonArray;
    }


    public static JOTestModelDemo objectFromString(String string) throws JSONException {
        JSONObject jsonObject = new JSONObject(string);
        return objectFromJSON(jsonObject);
    }

    public static String stringFromObject(JOTestModelDemo object) throws JSONException {
        JSONObject jsonObject = JSONFromObject(object);
        return jsonObject.toString();
    }

    public static JSONObject JSONFromObject(JOTestModelDemo object) {
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("keyInt", object.keyInt);
            jsonObject.put("keyLong", object.keyLong);
            jsonObject.put("keyDouble", object.keyDouble);
            jsonObject.put("keyString", object.keyString);

            if (object.keyIntList != null) {
                List<Integer> list = object.keyIntList;
                JSONArray jsonArray = new JSONArray();
                for (Integer item : list) {
                    jsonArray.put(item);
                }
                jsonObject.put("keyIntList", jsonArray);
            }

            if(object.keyObjList!=null){
                List<KeyObjList> list = object.keyObjList;
                JSONArray jsonArray = new JSONArray();
                for(KeyObjList item:list){
                    JSONObject jsonObj = KeyObjList.JSONFromObject(item);
                    jsonArray.put(jsonObj);
                }
                jsonObject.put("keyObjList",jsonArray);
            }

            if(object.keyObj != null){
                JSONObject jsonObj = KeyObj.JSONFromObject(object.keyObj);
                jsonObject.put("keyObj",jsonObj);
            }

            if (object.keyIntListList != null) {
                List<List<Integer>> list = object.keyIntListList;
                JSONArray jsonArray = new JSONArray();
                for (List<Integer> list1 : list) {
                    JSONArray jsonArray1 = new JSONArray();
                    for (Integer item : list1) {
                        jsonArray1.put(item);
                    }

                    jsonArray.put(jsonArray1);
                }

                jsonObject.put("keyIntListList", jsonArray);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return jsonObject;
    }

    public static JOTestModelDemo objectFromJSON(JSONObject jsonObject) {
        JOTestModelDemo object = new JOTestModelDemo();

        object.keyInt = jsonObject.optInt("keyInt");
        object.keyLong = jsonObject.optLong("keyLong");
        object.keyDouble = jsonObject.optDouble("keyDouble");
        object.keyString = jsonObject.optString("keyString");

        if (jsonObject.optJSONArray("keyIntList") != null) {
            JSONArray jsonArray = jsonObject.optJSONArray("keyIntList");
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                Integer item = jsonArray.optInt(i);
                list.add(item);
            }

            object.keyIntList = list;
        }

        if (jsonObject.optJSONArray("keyObjList") != null) {
            JSONArray jsonArray = jsonObject.optJSONArray("keyIntListList");
            List<KeyObjList> list = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObj = jsonArray.optJSONObject(i);
                KeyObjList item = KeyObjList.objectFromJSON(jsonObj);
                list.add(item);
            }
        }

        if (jsonObject.optJSONArray("keyIntListList") != null) {
            JSONArray jsonArray = jsonObject.optJSONArray("keyIntListList");
            List<List<Integer>> list = new ArrayList<>();
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONArray jsonArray1 = jsonArray.optJSONArray(i);
                List<Integer> list1 = new ArrayList<>();
                for (int i1 = 0; i1 < jsonArray1.length(); i1++) {
                    Integer list2 = jsonArray1.optInt(i1);
                    list1.add(list2);
                }
                list.add(list1);
            }

            object.keyIntListList = list;
        }


        if (jsonObject.optJSONObject("keyObj") != null) {
            JSONObject jsonObj = jsonObject.optJSONObject("keyObj");
            object.keyObj = KeyObj.objectFromJSON(jsonObj);
        }


        return object;
    }


    public int getKeyInt() {
        return keyInt;
    }

    public void setKeyInt(int keyInt) {
        this.keyInt = keyInt;
    }

    public long getKeyLong() {
        return keyLong;
    }

    public void setKeyLong(long keyLong) {
        this.keyLong = keyLong;
    }

    public double getKeyFloat() {
        return keyFloat;
    }

    public void setKeyFloat(double keyFloat) {
        this.keyFloat = keyFloat;
    }

    public double getKeyDouble() {
        return keyDouble;
    }

    public void setKeyDouble(double keyDouble) {
        this.keyDouble = keyDouble;
    }

    public String getKeyString() {
        return keyString;
    }

    public void setKeyString(String keyString) {
        this.keyString = keyString;
    }

    public KeyObj getKeyObj() {
        return keyObj;
    }

    public void setKeyObj(KeyObj keyObj) {
        this.keyObj = keyObj;
    }

    public List<Integer> getKeyIntList() {
        return keyIntList;
    }

    public void setKeyIntList(List<Integer> keyIntList) {
        this.keyIntList = keyIntList;
    }

    public List<List<Integer>> getKeyIntListList() {
        return keyIntListList;
    }

    public void setKeyIntListList(List<List<Integer>> keyIntListList) {
        this.keyIntListList = keyIntListList;
    }

    public List<String> getKeyStringList() {
        return keyStringList;
    }

    public void setKeyStringList(List<String> keyStringList) {
        this.keyStringList = keyStringList;
    }

    public List<List<String>> getKeyStringListList() {
        return keyStringListList;
    }

    public void setKeyStringListList(List<List<String>> keyStringListList) {
        this.keyStringListList = keyStringListList;
    }

    public List<KeyObjList> getKeyObjList() {
        return keyObjList;
    }

    public void setKeyObjList(List<KeyObjList> keyObjList) {
        this.keyObjList = keyObjList;
    }

    public List<List<KeyObjListList>> getKeyObjListList() {
        return keyObjListList;
    }

    public void setKeyObjListList(List<List<KeyObjListList>> keyObjListList) {
        this.keyObjListList = keyObjListList;
    }

    public static class KeyObj {
        private int valueInt;
        private List<String> valueList;


        public static KeyObj objectFromJSON(JSONObject jsonObject) {
            KeyObj object = new KeyObj();
            object.valueInt = jsonObject.optInt("valueInt");

            {
                JSONArray jsonArray = jsonObject.optJSONArray("valueList");
                if (jsonArray != null) {
                    List<String> list = new ArrayList<>();
                    for (int i = 0; i < jsonArray.length(); i++) {
                        String item = jsonArray.optString(i);
                        list.add(item);
                    }

                    object.valueList = list;
                }
            }

            return object;
        }

        public static JSONObject JSONFromObject(KeyObj object){
            return new JSONObject();
        }

//        public static List<KeyObj> arrayFromJSON(JSONArray jsonArray) {
//            List<KeyObj> list = new ArrayList<>();
//            for (int i = 0; i < jsonArray.length(); i++) {
//                KeyObj item = objectFromJSON(jsonArray.optJSONObject(i));
//                list.add(item);
//            }
//            return list;
//        }

        public int getValueInt() {
            return valueInt;
        }

        public void setValueInt(int valueInt) {
            this.valueInt = valueInt;
        }

        public List<String> getValueList() {
            return valueList;
        }

        public void setValueList(List<String> valueList) {
            this.valueList = valueList;
        }
    }

    public static class KeyObjList {
        private double valueFloat;
        private List<Integer> valueList;


        public static KeyObjList objectFromJSON(JSONObject jsonObject) {
            return new KeyObjList();
        }

        public static JSONObject JSONFromObject(KeyObjList object){
            return new JSONObject();
        }

        public double getValueFloat() {
            return valueFloat;
        }

        public void setValueFloat(double valueFloat) {
            this.valueFloat = valueFloat;
        }

        public List<Integer> getValueList() {
            return valueList;
        }

        public void setValueList(List<Integer> valueList) {
            this.valueList = valueList;
        }
    }

    public static class KeyObjListList {
        private List<Integer> valueList;

        public static KeyObjListList objectFromData(String str) {

            return new Gson().fromJson(str, KeyObjListList.class);
        }

        public static List<KeyObjListList> arrayKeyObjListListFromData(String str) {

            Type listType = new TypeToken<ArrayList<KeyObjListList>>() {
            }.getType();

            return new Gson().fromJson(str, listType);
        }

        public List<Integer> getValueList() {
            return valueList;
        }

        public void setValueList(List<Integer> valueList) {
            this.valueList = valueList;
        }
    }
}
