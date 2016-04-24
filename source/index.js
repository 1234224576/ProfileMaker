var socket = io.connect();

function sendbutton(){
	console.log("ccc");
	var socket = io.connect("http://127.0.0.1:8000");
	socket.emit('predict');
};

$(function() {
	var video = document.getElementById('camera');
	var localMediaStream = null;
	var hasGetUserMedia = function() {
		return (navigator.getUserMedia || navigator.webkitGetUserMedia ||
			navigator.mozGetUserMedia || navigator.msGetUserMedia);
	};
	var onFailSoHard = function(e) {
		console.log('エラー!', e);
	};
	if(!hasGetUserMedia()) {
		alert("未対応ブラウザです。");
	} else {
		window.URL = window.URL || window.webkitURL;
		navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
		navigator.getUserMedia({video: true}, function(stream) {
			video.src = window.URL.createObjectURL(stream);
			localMediaStream = stream;
		}, onFailSoHard);
		
		var c = document.getElementById('marker_view');
		var context = c.getContext('2d');
		context.strokeStyle = "rgb(255,0,0)";
		context.lineWidth = 0.2;
		context.beginPath();
		context.moveTo(50,70);
		context.lineTo(150,70);
		context.closePath();
		context.stroke();
		context.beginPath();
		context.moveTo(100,40);
		context.lineTo(100,100);
		context.closePath();
		context.stroke();
		
	}
	$("#start").click(function() {
		if (localMediaStream) {
			var canvas = document.getElementById('canvas');
			var ctx = canvas.getContext('2d');
			var img = document.getElementById('img');

			var w = video.offsetWidth;
			var h = video.offsetHeight;

			canvas.setAttribute("width", w);
			canvas.setAttribute("height", h);
			ctx.drawImage(video,180,0,300,400,0, 0, w, h);
			img.src = canvas.toDataURL('image/png');
			$('#captureModal').modal();
		}
	});
});

