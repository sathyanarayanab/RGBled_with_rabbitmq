function connect(){
var ws = new WebSocket("ws://192.168.1.2:15674/ws");
var client = Stomp.over(ws);
client.connect('guest', 'guest', on_connect, on_error); //Change the default username and password in first and second param

client.debug = function() {}; // Sets the debug function to null to show no debug in console

callback = function(message) {
    if (message.body) {
        client.send("/exchange/logs", {
            'content-type': 'text/plain',
            'destination': '/exchange/logs'
        }, "Hello");
    }
};
return client;
}

var on_connect = function() {
    client.subscribe("/exchange/logs", onmessage, {
        "x-message-ttl": "60",
        "destination": "/exchange/logs"
    })
    console.log('connected');
    let apiCol = new XMLHttpRequest();
    apiCol.onreadystatechange = () => {};
    var apiColURL = "http://192.168.1.28:5000/fetch"
    apiCol.open('GET', apiColURL);
    apiCol.send();
    apiCol.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("color").value = "#" + apiCol.responseText;
            document.getElementById("hexvalue").innerHTML = "#" + apiCol.responseText;
            document.getElementById("hexvalue").style.color = document.getElementById("color").value;
        }
    };

};
var on_error = function() {
	console.log('error');
	client = connect();
	return client;
};

function onmessage(m) {
    document.getElementById("color").value = "#" + m.body;
    document.getElementById("hexvalue").innerHTML = document.getElementById("color").value;
    document.getElementById("hexvalue").style.color = document.getElementById("color").value;

}

function sendmessage(m) {
    var VALUE = document.getElementById("color").value.replace("#", '');
    var URL = "http://192.168.1.28:5000/color?set=" + VALUE;
    let apiRequest = new XMLHttpRequest();
    apiRequest.open('GET', URL);
    apiRequest.send();
    client.send("/exchange/logs", {
        'content-type': 'text/plain',
        'destination': '/exchange/logs'
    }, VALUE);
    document.getElementById("hexvalue").innerHTML = document.getElementById("color").value;
    document.getElementById("hexvalue").style.color = document.getElementById("color").value;
}
client = connect();