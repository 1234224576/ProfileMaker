var socket = io.connect();

socket.on("showPdfFile",function(data){
	console.log("GET");
	window.open(data["url"]+"?time=" + escape(new Date()));
});

function sendbutton(){
	$("#load_view").show();
	var canvas = document.getElementById('canvas');
	var can = canvas.toDataURL();
	var base64Data = can.split(',')[1];
	var data = window.atob(base64Data); 
	var buff = new ArrayBuffer(data.length);
	var arr = new Uint8Array(buff);
	for(var i = 0, dataLen = data.length; i < dataLen; i++){
		arr[i] = data.charCodeAt(i);
	}
	var blob = new Blob([arr], {type: 'image/png'});

	var api_key = '54fe659b6b6484074e0d161226e8e441';
	var api_secret = 'B-3Xcd1vEWras_OGkKnT5ROLfeZwKD3b';
	var url = 'http://api.us.faceplusplus.com/detection/detect' + '?api_key=' + api_key + '&api_secret=' + api_secret +'&attribute=glass,pose,gender,age,race,smiling';

	var formData = new FormData();
	formData.append('img', blob);

	$.ajax({
		url: url,
		type: 'POST',
		data: formData,
		contentType: false,
		processData: false,
		success: function(data, dataType) {
			$("#load_view").hide();
			if(data["face"].length == 0){
				$("#error_info").text("顔の検出に失敗しました。もう一度撮影して下さい。");
				return;
			}
			var faceData = createFaceData(data["face"][0]);
			console.log(faceData);
			var name = $("#name_text_box").val();
			var socket = io.connect("http://127.0.0.1:8000");
			socket.emit('predict',{faceData:faceData,name:name});
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			$("#load_view").hide();
			console.log('Error : ' + errorThrown);
		}
	});
};

$(function() {
	$("#load_view").hide();
	
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
		$("#error_info").text("");
		if($("#name_text_box").val().length <= 0){
			$("#submit_btn").prop("disabled", true);
		}

		if (localMediaStream) {
			var canvas = document.getElementById('canvas');
			var ctx = canvas.getContext('2d');
			var img = document.getElementById('img');

			var w = video.offsetWidth;
			var h = video.offsetHeight;

			canvas.setAttribute("width", w);
			canvas.setAttribute("height", h);

			ctx.drawImage(video,130,0,400,400,0,0,w,h);
			img.src = canvas.toDataURL('image/png');
			$.ajax({
			    url:"/upload",
			    method:"post",
			    data:{img:img.src,filename:"face.png"}
			});
			$('#captureModal').modal();
		}
	});

	$("#name_text_box").keypress(function(){
		if($(this).val().length > 0){
			$("#submit_btn").prop("disabled", false);
		}
	});
});

function createFaceData(data){
	var age = data["attribute"]["age"]["value"];
	var gender = 0;
	if(data["attribute"]["gender"]["value"] == "Female"){
		gender = 1;
	}
	var smiling = data["attribute"]["smiling"]["value"];

	var glass = 0;
	if(data["attribute"]["glass"]["value"] == "Normal"){
		glass = 1;
	}else if(data["attribute"]["glass"]["value"] == "Dark"){
		glass = 2;
	}
	var yaw = data["attribute"]["pose"]["yaw_angle"]["value"];
	var pitch = data["attribute"]["pose"]["pitch_angle"]["value"];
	var roll = data["attribute"]["pose"]["roll_angle"]["value"];
	var eye_x = data["position"]["eye_right"]["x"] - data["position"]["eye_left"]["x"];
	var eye_y = (data["position"]["eye_left"]["y"]+data["position"]["eye_right"]["y"])/2.0;
	var mouth_x = data["position"]["mouth_right"]["x"] - data["position"]["mouth_left"]["x"];
	var mouth_y = (data["position"]["mouth_left"]["y"]+data["position"]["mouth_right"]["y"])/2.0;
	var nose_x = data["position"]["nose"]["x"];
	var nose_y = data["position"]["nose"]["y"];
	return age+","+gender+","+smiling+","+glass+","+yaw+","+pitch+","+roll+","+eye_x+","+eye_y+","+mouth_x+","+mouth_y+","+nose_x+","+nose_y;
}

