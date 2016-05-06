var http = require('http');
var fs = require('fs');
var rpc = require('./node-msgpack-rpc/lib/msgpack-rpc');
var st = require('node-static');
var file = new st.Server('./');

var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(__dirname + '/ML/profilemaker.db');

var PDFDocument = require('pdfkit');
var doc = new PDFDocument();

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
		  c.invoke('predict',data, function(err, response) {
		  	console.log("wroks_label:"+response);
		  	createPdf(response[0],response[1]);
		    c.close();
		  });
		});
    });

	var getJobStr = function(job_id){
		return new Promise(function(success){
			var sql = 'SELECT * FROM job WHERE id = '+job_id+';';
			db.each(sql, function(err, row) {
			    success(row.job);
		  	});
		});
	};

	var getSentence = function(job_id,copy_id){
		return new Promise(function(success){
			var rand = Math.floor( Math.random() * 3);
			var count = 0;
			var sql = 'SELECT * FROM firstSentence WHERE catchcopy_id = '+copy_id+';';
			db.each(sql, function(err, row) {
				if(count == rand) success(row.text);
				count++;
		  	});
		});
	}

	function createPdf(job_id,copy_id){
		var job = "";
	  	getJobStr(job_id).then(function success(j){
	  		job = j;
	  	});
	  	getSentence(job_id,copy_id).then(function outputPdf(sentence){
	  		console.log(sentence);
	  		console.log(job);
	  		doc.font('kochi-mincho-subst.ttf');
	  		doc.image("template.png", 0, 0, {fit:[500, 500]});
	  		doc.fontSize(30).text(job,100,200);
	  		doc.fontSize(20).text(sentence,100,300);
	  		doc.pipe(fs.createWriteStream('output.pdf'),{end:true}).on('finish', function () {
	  			console.log("complete");
	  			socket.broadcast.emit('showPdfFile',{url:"http://127.0.0.1:8000/output.pdf"});
	  			doc = new PDFDocument();
	  		});
	  		doc.end();

	  	});
	}

});



server.listen(8000);