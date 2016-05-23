package com.github.iwanglian.lejson;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Date;

import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import org.json.JSONObject;
import com.google.gson.Gson;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.alibaba.fastjson.JSON;
import com.bluelinelabs.logansquare.LoganSquare;

import com.github.iwanglian.lejson.model.JCTestModel;
import com.github.iwanglian.lejson.model.FJTestModel;
import com.github.iwanglian.lejson.model.GSTestModel;
import com.github.iwanglian.lejson.model.LSTestModel;


public class MainActivity extends AppCompatActivity {

    private String jsonStr;
    private TextView label;
    private ObjectMapper objectMapper;
    private Gson gson;
    private Handler mHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        label = (TextView) findViewById(R.id.label);

        jsonStr = getJson("TestModel.json");
        objectMapper = new ObjectMapper();
        gson = new Gson();

        mHandler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {
                if (msg.what == 1) {
                    label.setText(label.getText() + (String) msg.obj);
                    return true;
                }
                return false;
            }
        });

        mHandler.post(new Runnable() {
            @Override
            public void run() {
                int round = 1000;

                Date beforeAN = new Date();
                for (int i = 0; i < round; i++) {
                    testJA();
                }
                Date afterAN = new Date();
                long durationAN = afterAN.getTime() - beforeAN.getTime();
                String resultAN = String.format("\nJava run %d times, duration: %f\n", round, durationAN / 1000.0f);
                Message msg = new Message();
                msg.what = 1;
                msg.obj = resultAN;
                mHandler.sendMessage(msg);

                Date beforeJA = new Date();
                for (int i = 0; i < round; i++) {
                    testJC();
                }
                Date afterJA = new Date();
                long durationJA = afterJA.getTime() - beforeJA.getTime();
                String jaResult = String.format("\nJackson(jc) run %d times, duration: %f\n", round, durationJA / 1000.0f);
                msg = new Message();
                msg.what = 1;
                msg.obj = jaResult;
                mHandler.sendMessage(msg);


                Date beforeGS = new Date();
                for (int i = 0; i < round; i++) {
                    testGS();
                }
                Date afterGS = new Date();
                long durationGS = afterGS.getTime() - beforeGS.getTime();
                String gsResult = String.format("\nGson(gs) run %d times, duration: %f\n", round, durationGS / 1000.0f);
                msg = new Message();
                msg.what = 1;
                msg.obj = gsResult;
                mHandler.sendMessage(msg);


                Date beforeFJ = new Date();
                for (int i = 0; i < round; i++) {
                    testFJ();
                }
                Date afterFJ = new Date();
                long durationFJ = afterFJ.getTime() - beforeFJ.getTime();
                String resultFJ = String.format("\nFastjson(fj) run %d times, duration: %f\n", round, durationFJ / 1000.0f);
                msg = new Message();
                msg.what = 1;
                msg.obj = resultFJ;
                mHandler.sendMessage(msg);


                Date beforeLS = new Date();
                for (int i = 0; i < round; i++) {
                    testLS();
                }
                Date afterLS = new Date();
                long durationLS = afterLS.getTime() - beforeLS.getTime();
                String resultLS = String.format("\nLoganSquare(ls) run %d times, duration: %f\n", round, durationLS / 1000.0f);
                msg = new Message();
                msg.what = 1;
                msg.obj = resultLS;
                mHandler.sendMessage(msg);


            }
        });
    }

    private void testGS() {
        GSTestModel testModel = gson.fromJson(jsonStr, GSTestModel.class);
    }


    private void testJA() {
        try {
            JSONObject jsonObject = new JSONObject(jsonStr);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void testJC() {
        try {
            JCTestModel testModel = objectMapper.readValue(jsonStr, JCTestModel.class);
        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }

    private void testFJ() {
        FJTestModel testModel = JSON.parseObject(jsonStr, FJTestModel.class);
    }

    private void testLS() {
        try {
            LSTestModel testModel = LoganSquare.parse(jsonStr, LSTestModel.class);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private String getJson(String fileName) {
        StringBuilder stringBuilder = new StringBuilder();
        try {
            BufferedReader bf = new BufferedReader(new InputStreamReader(
                    getAssets().open(fileName)));
            String line;
            while ((line = bf.readLine()) != null) {
                stringBuilder.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return stringBuilder.toString();
    }
}
