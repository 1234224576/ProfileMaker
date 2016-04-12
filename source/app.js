var http = require('http');
var fs = require('fs');

var st = require('node-static');
var file = new st.Server('./');


var server = http.createServer(function (request, response) {
    request.addListener('end', function () {
        file.serve(request, response);
    }).resume();
});
var io = require('socket.io').listen(server);
io.sockets.on('connection', function(socket) {
    console.log('result:');
});

server.listen(8000);