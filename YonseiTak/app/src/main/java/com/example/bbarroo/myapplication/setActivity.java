package com.example.bbarroo.myapplication;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Toast;

public class setActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set);
    }
    public void backButtonClicked(View v) {
        Toast.makeText(getApplicationContext(), "돌아가기 버튼을 누르셨군요", Toast.LENGTH_SHORT);
        finish();
    }
}
