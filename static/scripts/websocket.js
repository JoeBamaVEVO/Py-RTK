// var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket = io.connect("http://127.0.0.1:5000");

socket.on('connect', function() {
    console.log('Websocket connected!');
    // You can emit events here if needed, e.g., socket.emit('my_event', {data: 'I'm connected!'});
    socket.emit("gps_data", {data: "Gimmie Data!"});
});

socket.on('gps_data', function(data) {
    console.log(data);
    // Do something with the data received
});



