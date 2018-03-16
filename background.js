//****************************************************************************
// 1. Identifying New URLs Code
//****************************************************************************

var selectedId = -1;
var unvisitedTabs = new Set();

// Keep track of opened, but unvisited tabs. The "Open Link in New Tab" Case
chrome.tabs.onCreated.addListener(function(tab){
  unvisitedTabs.add(tab.id);
});


chrome.tabs.onUpdated.addListener(function(tabId, props) {
  if (props.status == "complete" && tabId == selectedId){
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      selectedId = tabs[0].id;
      startPostUrlToServer(SERVER_URL, tabs[0].url);
    });
  }

});

chrome.tabs.onActivated.addListener(function(activeInfo) {
  tabId = activeInfo.tabId;

  // Covers case when Link was opened from another tab
  // "Open Link in New Tab"
  if ( unvisitedTabs.has(tabId) ) {
    chrome.tabs.get(tabId, function(tab) {
      startPostUrlToServer(SERVER_URL, tab.url);
    });

  }
  unvisitedTabs.delete(tabId);
  selectedId = activeInfo.tabId;
});

//****************************************************************************
// Client REST API Logic
//****************************************************************************

var SERVER_URL = "http://127.0.0.1:5000/";

/* contentType is not JSON because an initial `OPTIONS` request is sent if 
 * it is not a "simple request". 
 * More info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Simple_requests
 */
var contentType = "application/x-www-form-urlencoded;charset=UTF-8";
var method = "POST";
var shouldBeAsync = true;

var request = new XMLHttpRequest();

startPostUrlToServer = function (server, url) {
  if (url != "chrome://newtab/"){
    postUrlToServer(server, url);
  }
}

postUrlToServer = function (server, url) {
  request.open("POST", server, shouldBeAsync)
  request.onload = function () {
    var status = request.status; // HTTP response status, e.g., 200 for "200 OK"
    //alert(status);
    var data = request.responseText; // Returned data, e.g., an HTML document.
  };

  request.setRequestHeader("Content-Type", contentType);
  request.send(url);
  //alert("Sent to server: " + server + " URL: " + url);
}
