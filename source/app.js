var http = require('http');
var fs = require('fs');
var rpc = require('./node-msgpack-rpc/lib/msgpack-rpc');
var st = require('node-static');
var file = new st.Server('./');
var qs = require('querystring');

var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(__dirname + '/ML/profilemaker.db');

var PDFDocument = require('pdfkit');
var doc = new PDFDocument();

var server = http.createServer(function (request, response) {
	if(request.url=='/upload'){
		var body='';
		request.on('data', function (data) {
		   body +=data;
		});
		request.on('end',function(){
			var POST =  qs.parse(body);
			var base64Data = POST["img"].replace(/^data:image\/png;base64,/, "");
			fs.writeFile(POST["filename"],base64Data,'base64',function(err){
			  // console.log(err);
			});
		});
	}
    request.addListener('end', function () {
        file.serve(request, response);
    }).resume();
});

var io = require('socket.io').listen(server);
io.sockets.on('connection', function(socket) {
	socket.on('predict', function(data){
		console.log("listen");
		var c = rpc.createClient(6000, '127.0.0.1', function() {
		  c.invoke('predict',data["faceData"], function(err, response) {
		  	console.log("wroks_label:"+response);
		  	createPdf(response[0],response[1],data["name"],data["age"],data["gender"]);
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
	};

	function createPdf(job_id,copy_id,name,age,gender){
		var job = "";
	  	getJobStr(job_id).then(function success(j){
	  		job = j;
	  	});
	  	getSentence(job_id,copy_id).then(function outputPdf(sentence){
	  		console.log(sentence);
	  		console.log(job);
	  		doc.font('kochi-mincho-subst.ttf');
	  		doc.image("back.png", 30, 30, {fit:[521,383]});
	  		doc.fontSize(16).text(name,300,80);
				doc.fontSize(16).text(age+"歳",300,125);
				if(gender == "Male") gender = "男";
				else gender = "女";
				doc.fontSize(16).text(gender,470,125);
	  		doc.fontSize(16).text(job,310,165);

				var r=new RegExp(".{1,"+35+"}","g");
				var sentences = sentence.match(r);
				console.log(sentences);
				for(var i=0;i<sentences.length;i++){
					doc.fontSize(14).text(sentences[i],40,255 + (i*35));
				}

	  		doc.image("face.png", 30, 30, {fit:[170, 170]});
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
