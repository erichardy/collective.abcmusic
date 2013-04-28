/*
jq(document).ready(function() {
	jq("#form-widgets-abc").autoGrow();
 
});
*/

jq(document).ready(function() {
	jq("#tuneModified").submit(function(){
		var pathname = window.location.pathname;
		abctext = jq("#abc-text").val()
		var newMidi  = jq.post("@@updateMidi" , {'abctext':abctext, 'abctuneURL':pathname} , function(data){
			jq('#abctuneMidi').attr('src', pathname+'/@@download/midi/' + data) ;
			alert(pathname+'/@@download/midi/' + data) ;
			});
		var newScore = jq.post("@@updateScore" , {'abctext':abctext, 'abctuneURL':pathname} , function(data){alert(data)});
		tuneModified = true ;
		jq("#tuneModified").hide() ;
		// alert(window.location.href) ;
		return false;
	});
	
	var tuneModified = false ;
	
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
		ABCJS.renderAbc('abc-edit', input, {}, {scale:scoreSize},{});
		ABCJS.renderMidi('midi-edit',input, {});
		jq("#avertissementTuneModified").html(tuneModified);
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
		jq("#abcscale").text(scoreSize) ;
		ABCJS.renderAbc('abc-edit', input , {}, {scale: scoreSize},{});
		// alert ('scoresize:::' + scoreSize) ;
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
		max: 3 ,
		step: 0.1 ,
		orientation: "vertical" ,
		change: function(event,ui){if (event.originalEvent){resizeABCscore()} }
	});
	scoreSize = .8 ;
	jq("#abc-edit-slider-size").slider("option" , "value" , scoreSize);
	jq("#abcscale").text(scoreSize) ;
	ABCJS.renderAbc('abc-edit', jq("#abc-text").text() , {}, {scale: scoreSize},{});
	ABCJS.renderMidi('midi-edit',jq("#abc-text").text(), {}) ;
	jq('#abc-text').keyup(updateABC);
	tuneNotModified = jq("#tuneNotModified").html() ;
	// alert(tuneNotModified) ;
	jq("#tuneNotModified").hide() ;
	tuneModified = jq("#tuneModified").html() ;
	jq("#tuneModified").hide() ;
	// alert(tuneModified)
	jq("#avertissementTuneModified").html(tuneNotModified);
	
});