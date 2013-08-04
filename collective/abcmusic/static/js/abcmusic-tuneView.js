jq(document).ready(function() {
	jq( "#accordion" ).accordion();
});

jq(document).ready(function() {
	jq("#avertissementTuneModified").click(function(){
		var pathname = window.location.pathname;
		abctext = jq("#abc-text").val();
		var updatedTune  = jq.post("@@updateTune" , {'abctext':abctext, 'abctuneURL':pathname} , function(data){
			jq.post("@@currentScore", {'abctuneURL':pathname}, function(data){
				width = jq("#scoreView").attr('width');
				height = jq("#scoreView").attr('height');
				jq("#scoreView").html(data);
				});
			// I don't understand why: without doing anything, the midi div is automaticaly updated...???
			// but I force it anyway !
			jq.post("@@currentMidi", {'abctuneURL':pathname}, function(data){
				jq("#midiView").html(data);
				});
			});
		isModified = false ;
		jq("#avertissementTuneModified").html(tuneNotModified);
		return false;
	});
	// pour tester comment stocker l'etat de la fenetre en cours en vue de la remettre
	// dans le meme etat a l'appel suivant.
	// Pour cela, il faudra utiliser les fonctionnalites HTML5 : localStorage
	// cf : http://www.w3schools.com/html/html5_webstorage.asp
	jq("#slider-value").mouseenter(function(){
		alert(jq('#portal-top').is(':hidden'));
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
	};
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
			if (lines[i] != '') {
				abcText = abcText + lines[i] + '\n';
			}
		}
		return abcText
	};
	function updateSlider() {
		speed = getSpeed() ;
		jq('#slider').slider("option" , "value" , speed) ;
		jq("#slider-value").text(speed);

	};
	function updateABC() {
		var input = jq("#abc-text").val();
		var scoreSize = jq("#abc-edit-slider-size").slider("option", "value") ;
		updateSlider() ;
		ABCJS.renderAbc('abc-edit', input, {print: true}, {scale:scoreSize , editable: true},{});
		ABCJS.renderMidi('midi-edit',input, {});
		if ( ! isModified ) {
			jq("#avertissementTuneModified").html(tuneModified);
			isModified = true ;
		}
	};
	function updateSpeedFromSlider() {
		var speed = jq("#slider").slider("option", "value") ;
		jq("#slider-value").text(jq("#slider").slider("option", "value"));
		abcText = setSpeed(speed) ;
		jq("#abc-text").val(abcText);
		updateABC();
	};
	function resizeABCscore(){
		var scoreSize = jq("#abc-edit-slider-size").slider("option", "value") ;
		var input = jq("#abc-text").val();
		jq("#abcscale").text(scoreSize) ;
		ABCJS.renderAbc('abc-edit', input , {}, {scale: scoreSize},{});
	};
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
		max: 1.3 ,
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
	jq("#tuneNotModified").hide() ;
	tuneModified = jq("#tuneModified").html() ;
	jq("#tuneModified").hide() ;
	isModified = false ;
	jq("#avertissementTuneModified").html(tuneNotModified);
});
