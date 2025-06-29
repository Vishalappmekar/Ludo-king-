package com.example.ludoking;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        WebView webView = new WebView(this);
        webView.setWebViewClient(new WebViewClient());
        webView.getSettings().setJavaScriptEnabled(true);
        
        // अपना HTML कोड यहाँ लोड करें
        webView.loadDataWithBaseURL(null, 
            "आपका पूरा HTML कोड यहाँ", 
            "text/html", "UTF-8", null);
            
        setContentView(webView);
    }
}
