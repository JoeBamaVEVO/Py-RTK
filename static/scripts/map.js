var socket = io.connect('http://' + document.domain + ':' + location.port);
// var socket = io.connect("http://127.0.0.1:5000");

socket.on('connect', function() {
    console.log('Websocket connected!');
    // You can emit events here if needed, e.g., socket.emit('my_event', {data: 'I'm connected!'});
    socket.emit("gps_data", {data: "Gimmie Data!"});
});

socket.on('gps_data', function(data) {
    console.log(data);
    addMarker(data.lat, data.long);
    // Do something with the data received
});

var map = L.map('map').setView([60.68467800058445, 5.678324332522398], 30);
var newMarker = L.circle([60.68467800058445, 5.678324332522398], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 1,
    radius: 1,
    title: 'RTK-GPS'
}).addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function addMarker(lat, lon) {
    map.eachLayer(function (layer) {
        if (layer instanceof L.Marker) map.removeLayer(layer);
    });
    let myIcon = L.icon({
        iconUrl: '/static/images/icons/home.svg',
        iconSize: [38, 95],
        iconAnchor: [22, 94],
        popupAnchor: [-3, -76],
       
    });
    let options = {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 5,
        title: 'RTK-GPS',
        icon: myIcon
    }
 
    var marker = L.marker([lat, lon], options).addTo(map);
}