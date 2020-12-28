package com.example.bbarroo.myapplication;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class MenuActivity extends AppCompatActivity {


    //  TCP연결 관련
    private Socket clientSocket;
    private BufferedReader socketIn;
    private PrintWriter socketOut;
    private int port = 35356;
    private final String ip = "172.21.4.130";
    private MyHandler myHandler;
    private MyThread myThread;
    TextView tva;
    EditText minsik;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        try {
            clientSocket = new Socket(ip, port);
            socketIn = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            socketOut = new PrintWriter(clientSocket.getOutputStream(), true);
        } catch (Exception e) {
            e.printStackTrace();
        }

        myHandler = new MenuActivity.MyHandler();
        myThread = new MenuActivity.MyThread();
        myThread.start();



        tva = (TextView) findViewById(R.id.tva);
        minsik = (EditText) findViewById(R.id.minsik);
        minsik.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String strSend = minsik.getText().toString();
                socketOut.println(strSend);
            }
        });

    }

    class MyThread extends Thread {
        @Override
        public void run() {
            while (true) {
                try {
                    // InputStream의 값을 읽어와서 data에 저장
                    String datas = socketIn.readLine();
                    // Message 객체를 생성, 핸들러에 정보를 보낼 땐 이 메세지 객체를 이용
                    Message msg = myHandler.obtainMessage();
                    msg.obj = datas;
                    myHandler.sendMessage(msg);
                }
                catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    class MyHandler extends Handler {
        @Override
        public void handleMessage(Message msg) {
            tva.setText(msg.obj.toString());
        }
    }

    public void backButtonClicked(View v) {
        Toast.makeText(getApplicationContext(), "돌아가기 버튼을 누르셨군요", Toast.LENGTH_SHORT);
        finish();
    }
}

