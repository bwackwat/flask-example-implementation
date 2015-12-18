window.onload = function(){

var localStorageLoginUsernameKey = "FLASK_MAP_EXAMPLE_USERNAME";
var localStorageLoginTokenKey = "FLASK_MAP_EXAMPLE_TOKEN";
var apiUrl = "http://" + window.location.hostname + ":5000/login";

var status = document.getElementById("status");

//LOGIN MODAL SCRIPT

var login = document.getElementById("loginModal");
var loginResult = document.getElementById("loginResult");
var username = document.getElementById("username");
var password = document.getElementById("password");

document.getElementById("loginButton").onclick = function() {
	var loginData = JSON.stringify({"username": username.value, "password": password.value});
	alert(loginData);

	var http = new XMLHttpRequest();
	http.open("POST", apiUrl, true);
	http.setRequestHeader("Content-type", "application/json");
	http.onreadystatechange = function(){
		var resjson = JSON.parse(http.responseText);
		alert(http.responseText);

		if(http.readyState == 4 && http.status == 200){
			if(typeof(resjson.error) === 'undefined'){
				localStorage.setItem(localStorageLoginUsernameKey, username.value);
				localStorage.setItem(localStorageLoginTokenKey, resjson.token);
				status.innerHTML = "Welcome! You are logged in as " + localStorage.getItem(localStorageLoginUsernameKey);
				login.close();	
			}else{
				loginResult.innerHTML = resjson.error;
			}
		}else if(http.readyState == 3){
			//Bogus OPTIONS response...
			
			//0: request not initialized
			//1: server connection established
			//2: request received
			//3: processing request
			//4: request finished and response is ready
		}else{
			//Invalid API usage...
			alert("HTTP ERROR!");
		}
	}
	http.send(loginData);
};

document.getElementById("cancelLoginButton").onclick = function() {
	login.close();
};

if(localStorage.getItem(localStorageLoginTokenKey) === null){
	status.innerHTML = "Welcome! You are not logged in; you cannot save points of interest.";
	login.show();
}else{
	status.innerHTML = "Welcome! You are logged in as " + localStorage.getItem(localStorageLoginUsernameKey);
}

//POI MODAL SCRIPT

var poi = document.getElementById("poiModal");
var poiLocation = document.getElementById("poiLocation");

document.getElementById("savePoi").onclick = function() {
	
};
document.getElementById("cancelPoi").onclick = function() {
	poi.close();
};
document.getElementById("logout").onclick = function() {
	localStorage.removeItem(localStorageLoginTokenKey);
	status.innerHTML = "Welcome! You are not logged in; you cannot save points of interest.";
	poi.close();
};

//SIGNUP MODAL SCRIPT

//START MAP SCRIPT

map = new OpenLayers.Map("demoMap");
map.addLayer(new OpenLayers.Layer.OSM());

map.events.register("click", map, function(e) {
	if(localStorage.getItem(localStorageLoginTokenKey) === null){
		login.show();	
	}else{
		var position = map.getLonLatFromPixel(e.xy);
		position.transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
		poiLocation.innerHTML = position.lon.toFixed(5) + ", " + position.lat.toFixed(5);
		poi.show();	
	}
});

map.zoomToMaxExtent();

}