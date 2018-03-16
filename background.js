// Copyright (c) 2009 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

var SERVER_URL = "http://127.0.0.1:5000/";

var selectedId = -1;


chrome.tabs.onUpdated.addListener(function(tabId, props) {
  if (props.status == "complete" && tabId == selectedId){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      selectedId = tabs[0].id;
      //alert(tabs[0].url);
      postUrlToServer(SERVER_URL, tabs[0].url);
    });
  }

});

chrome.tabs.onSelectionChanged.addListener(function(tabId, props) {
  selectedId = tabId;
});

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
  selectedId = tabs[0].id;
});

var method = "POST";

var shouldBeAsync = true;

var request = new XMLHttpRequest();

// Before we send anything, we first have to say what we will do when the
// server responds. This seems backwards (say how we'll respond before we send
// the request? huh?), but that's how Javascript works.
// This function attached to the XMLHttpRequest "onload" property specifies how
// the HTTP response will be handled. 


postUrlToServer = function (server, url) {
  request.open("POST", server, shouldBeAsync)
  request.onload = function () {
    var status = request.status; // HTTP response status, e.g., 200 for "200 OK"
    alert(status);
    var data = request.responseText; // Returned data, e.g., an HTML document.
  };
  request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
  request.send(url);
  //alert("Sent to server: " + server + " URL: " + url);
}
