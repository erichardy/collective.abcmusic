/*
jq(document).ready(function() {
	jq("#form-widgets-abc").autoGrow();
 
});
*/

jq(document).ready(function() {
	jq("#record").click(function(){
		var pathname = window.location.pathname;
		abctext = jq("#abc-text").val()
		var aaa = jq.post("@@updateMidi" , {'abctext':abctext, 'abctuneURL':pathname} , function(data){alert(data)});
		var aaa = jq.post("@@updateScore" , {'abctext':abctext, 'abctuneURL':pathname} , function(data){alert(data)});
		return false;
	});

	function getSpeed() {
		abcInput = jq("#abc-text").val();
		lines = abcInput.split('\n');
		i = 0 ;
		for (i ; i < lines.length ; i++) {
			if (lines[i].split(':')[0] == 'Q') {
				return parseInt(lines[i].split(':')[1]) ;
			}
		}
		return 0
	}
	function setSpeed(q) {
		abcInput = jq("#abc-text").val();
		lines = abcInput.split('\n');
		i = 0 ;
		for (i ; i < lines.length ; i++) {
			if (lines[i].split(':')[0] == 'Q') {
				lines[i] = 'Q: ' + q
				break;
			}
		}
		var abcText = '';
		i = 0 ;
		for (i ; i < lines.length ; i++) {
			abcText = abcText + lines[i] + '\n';
		}
		return abcText
	}
	function updateSlider() {
		speed = getSpeed() ;
		jq('#slider').slider("option" , "value" , speed) ;
		jq("#slider-value").text(speed);

	}
	function updateABC() {
		var input = jq("#abc-text").val();
		var scoreSize = jq("#abc-edit-slider-size").slider("option", "value") ;
		updateSlider() ;
		ABCJS.renderAbc('abc-edit', input, {}, {scale:scoreSize});
		ABCJS.renderMidi('midi-edit',input, {});
	};
	function updateSpeedFromSlider() {
		var speed = jq("#slider").slider("option", "value") ;
		jq("#slider-value").text(jq("#slider").slider("option", "value"));
		abcText = setSpeed(speed) ;
		jq("#abc-text").val(abcText);
		updateABC();
	}
	function resizeABCscore(){
		var scoreSize = jq("#abc-edit-slider-size").slider("option", "value") ;
		var input = jq("#abc-text").val();
		ABCJS.renderAbc('abc-edit', input , {}, {scale: scoreSize});
	}
	minSpeed = 20 ;
	maxSpeed = 400 ;
	stepSpeed = 5 ;
	jq("#slider").slider({
		min: minSpeed , 
		max: maxSpeed , 
		from: minSpeed ,
		to: maxSpeed ,
		step : stepSpeed , 
		animate: "fast" ,
		round: 0 ,
		format: {format:"###"} ,
		skin: "round" ,
		dimension: '&nbsp;QQQ' ,
		change: function(event,ui){if (event.originalEvent){updateSpeedFromSlider()} }
		});
	speed = getSpeed() ;
	jq("#slider").width("350px") ;
	jq("#slider").slider("option" , "value" , speed);
	jq("#slider-value").text(speed);
	jq("#abc-edit-slider-size").slider ({
		min: 0.1 ,
		max: 1 ,
		step: 0.1 ,
		orientation: "vertical" ,
		change: function(event,ui){if (event.originalEvent){resizeABCscore()} }
	});
	scoreSize = 0.8 ;
	jq("#abc-edit-slider-size").slider("option" , "value" , scoreSize);
	ABCJS.renderAbc('abc-edit', jq("#abc-text").text() , {}, {scale:0.8});
	ABCJS.renderMidi('midi-edit',jq("#abc-text").text(), {}) ;
	jq('#abc-text').keyup(updateABC);
	
});