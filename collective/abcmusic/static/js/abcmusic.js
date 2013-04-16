/*
jq(document).ready(function() {
	jq("#form-widgets-abc").autoGrow();
 
});
*/
jq(document).ready(function() {
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
		updateSlider() ;
		ABCJS.renderAbc('abc-edit', input, {}, {scale:0.8});
		ABCJS.renderMidi('midi-edit',input, {});
	};
	function updateSpeedFromSlider() {
		var speed = jq("#slider").slider("option", "value") ;
		jq("#slider-value").text(jq("#slider").slider("option", "value"));
		abcText = setSpeed(speed) ;
		jq("#abc-text").val(abcText);
		updateABC();
	}

	minSpeed = 20 ;
	maxSpeed = 400 ;
	stepSpeed = 5 ;
	jq("#slider").slider({
		step : stepSpeed , 
		min: minSpeed , 
		max: maxSpeed , 
		range: false, 
		animate: "fast" ,
		change: function(event,ui){if (event.originalEvent){updateSpeedFromSlider()} }
		});

	speed = getSpeed() ;
	jq("#slider").width("350px") ;
	jq("#slider").slider("option" , "value" , speed);
	jq("#slider-value").text(speed);
	ABCJS.renderAbc('abc-edit', jq("#abc-text").text() , {}, {scale:0.8});
	ABCJS.renderMidi('midi-edit',jq("#abc-text").text(), {}) ;
	jq('#abc-text').keyup(updateABC);
	
});