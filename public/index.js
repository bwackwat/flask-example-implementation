window.onload = function(){

var localStorageLoginUsernameKey = "FLASK_MAP_EXAMPLE_USERNAME";
var localStorageLoginTokenKey = "FLASK_MAP_EXAMPLE_TOKEN";
var apiUrl = "https://" + window.location.hostname + ":1000/api";

var status = document.getElementById("status");

//API POSTING FUNCTION

function callAPI(route, data, callback){
	var sendData = JSON.stringify(data);

	var http = new XMLHttpRequest();
	http.open("POST", apiUrl + route, true);
	http.setRequestHeader("Content-type", "application/json");
	http.onreadystatechange = function(){
		if(http.responseText == ""){
			//Bloody OPTIONS pre-flight...
			return;
		}
		var resjson = JSON.parse(http.responseText);
		if(http.readyState == 4 && http.status == 200){
			callback(resjson);
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
	http.send(sendData);
}

//LOGIN MODAL SCRIPT

var login = document.getElementById("loginModal");
var loginResult = document.getElementById("loginResult");
var username = document.getElementById("username");
var password = document.getElementById("password");

document.getElementById("loginButton").onclick = function() {
	callAPI("/login", {"username": username.value, "password": password.value}, function(response){
		if(typeof(response.error) === 'undefined'){
			localStorage.setItem(localStorageLoginUsernameKey, username.value);
			localStorage.setItem(localStorageLoginTokenKey, response.token);
			status.innerHTML = "Welcome! You are logged in as " + localStorage.getItem(localStorageLoginUsernameKey);
			login.close();	
		}else{
			loginResult.innerHTML = response.error;
		}
	});
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

var signup = document.getElementById("signupModal");
var signupResult = document.getElementById("signupResult");
var signupUsername = document.getElementById("signupUsername");
var signupEmail = document.getElementById("signupEmail");
var signupPassword = document.getElementById("signupPassword");

document.getElementById("signupButton").onclick = function() {
	callAPI("/signup", {"username": signupUsername.value, "email": signupEmail.value, "password": signupPassword.value}, function(response){
		if(typeof(response.error) === 'undefined'){
			signup.close();
			signupResult.innerHTML = "You signed up successfully!";
			login.show();
		}else{
			signupResult.innerHTML = response.error;
		}
	});
};
document.getElementById("cancelSignupButton").onclick = function() {
	signup.close();
};

document.getElementById("goToSignup").onclick = function() {
	login.close();

	signupUsername.value = username.value;
	signupPassword.value = password.value;

	signup.show();
};

//START MAP SCRIPT

map = new OpenLayers.Map("demoMap",{
	theme: false
});

map.addLayer(new OpenLayers.Layer.OSM(
	"OpenStreetMap", 
	[
		//Chrome will use HTTPS
		'//a.tile.openstreetmap.org/${z}/${x}/${y}.png',
		'//b.tile.openstreetmap.org/${z}/${x}/${y}.png',
		'//c.tile.openstreetmap.org/${z}/${x}/${y}.png'
	], 
	null));

var markers = new OpenLayers.Layer.Markers("Markers");
var size = new OpenLayers.Size(21, 25);
var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
var icon = new OpenLayers.Icon("https://maps.google.com/intl/en_us/mapfiles/ms/micons/orange-dot.png", size, offset);
map.addLayer(markers);

var currentmarker = null;

map.events.register("click", map, function(e) {
	if(localStorage.getItem(localStorageLoginTokenKey) === null){
		login.show();	
	}else{
		var position = map.getLonLatFromPixel(e.xy);
		poiLocation.innerHTML = position.lon.toFixed(5) + ", " + position.lat.toFixed(5);

		if(currentmarker !== 'undefined'){
			markers.removeMarker(currentmarker);
		}
		currentmarker = new OpenLayers.Marker(position, icon.clone());
		markers.addMarker(currentmarker);

		poi.show();
	}
});

map.zoomToMaxExtent();

}