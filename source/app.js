var http = require('http');
var fs = require('fs');
var rpc = require('./node-msgpack-rpc/lib/msgpack-rpc');
var st = require('node-static');
var file = new st.Server('./');

var server = http.createServer(function (request, response) {
    request.addListener('end', function () {
        file.serve(request, response);
    }).resume();
});

var io = require('socket.io').listen(server);

io.sockets.on('connection', function(socket) {

	socket.on('predict', function(data){
		console.log("listen");
		var c = rpc.createClient(6000, '127.0.0.1', function() {
		  c.invoke('predict', [30,1,46.3288,0,-22.411464,-0.028708,-4.91025,20.8182,52.89575,17.55085,73.233,41.6452,66.726], function(err, response) {
		  	console.log(response);
		    c.close();
		  });
		});

    });
});

server.listen(8000);