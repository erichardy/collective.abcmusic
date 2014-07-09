/*
$(document).ready(function() {
	$( "#accordion" ).accordion();
});
*/
jQuery(document).ready(function($) {

$(document).ready(function() {
	$("a.a-overlay").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });
	if (auth == false) {
		$("h3").removeClass("tuneCollapsedHeading");
	}
	$("h3.tuneCollapsedHeading").click(function() {
		  $(this).nextUntil("h1 , h2 ,h3").slideToggle("fast");
		  $(this).toggleClass("tuneCollapsed");
	});
	$("h3.tuneCollapsed").nextUntil("h1 , h2 ,h3").hide();
	
	$("#saveModifications").click(function(){
		// var pathname = window.location.pathname;
		var pathname = $(location).attr('href');
		// console.log(uuid);
		abctext = $("#abc-text").val();
		makeMP3 = 0;
		if ($("#checkboxMakeMP3").is(':checked')) makeMP3 = 1;
		var updatedTune  = $.post("@@updateTune" , {'abctext':abctext, 'uuid':uuid, 'makeMP3':makeMP3} , function(data){
			// console.log(makeMP3);
			$.post("@@currentScore", {'uuid':uuid}, function(data){
				width = $("#scoreView").attr('width');
				height = $("#scoreView").attr('height');
				$("#scoreView").html(data);
				});
			// I don't understand why: without doing anything, the midi div is automaticaly updated...???
			// but I force it anyway !
			$.post("@@currentMidi", {'uuid':uuid}, function(data){
				$("#midiView").html(data);
				});
			$.post("@@currentPDFScore", {'uuid':uuid}, function(data){
				$("#pdfScore").html(data);
				});
			
			if (makeMP3 == 1) {
				$.post("@@currentMP3", {'uuid':uuid}, function(data){
					$("#mp3View").html(data);
					});
			}
			});
		isModified = false ;
		// $("#avertissementTuneModified").html(tuneNotModified);
		$("#tuneModified").hide() ;
		return false;
	});
	$("#createMP3").click(function(){
		var pathname = window.location.pathname;
		abctext = $("#abc-text").val();
		$.post("@@createMP3", {'abctext':abctext, 'uuid':uuid}, function(data){
			$("#mp3").html(data);
			});
	});
	$('#view-nav').click(function(){
		$("#viewlet-above-content").show();
	});
	function getSpeed() {
		abcInput = $("#abc-text").val();
		if (abcInput == undefined) return ;
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
		abcInput = $("#abc-text").val();
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
		$('#slider').slider("option" , "value" , speed) ;
		$("#slider-value").text(speed);

	};
	function updateABC() {
		var input = $("#abc-text").val();
		var scoreSize = $("#abc-edit-slider-size").slider("option", "value") ;
		updateSlider() ;
		ABCJS.renderAbc('abc-edit', input, {print: true}, {scale:scoreSize , editable: true},{});
		ABCJS.renderMidi('midi-edit',input, {});
		if ( ! isModified ) {
			// $("#avertissementTuneModified").html(tuneModified);
			$("#tuneModified").show() ;
			isModified = true ;
		}
	};
	function updateSpeedFromSlider() {
		var speed = $("#slider").slider("option", "value") ;
		$("#slider-value").text($("#slider").slider("option", "value"));
		abcText = setSpeed(speed) ;
		$("#abc-text").val(abcText);
		updateABC();
	};
	function resizeABCscore(){
		var scoreSize = $("#abc-edit-slider-size").slider("option", "value") ;
		var input = $("#abc-text").val();
		$("#abcscale").text(scoreSize) ;
		localStorage.setItem(window.location.href + '-scoreSize' , scoreSize);
		ABCJS.renderAbc('abc-edit', input , {}, {scale: scoreSize},{});
	};

	var currentPage = window.location.href ;
	
	// Delay for updateABC: 2000ms (2 seconds)
	//
	// implementation of the answer of Anderson Aug 19 '13 at 2:48
	// in http://stackoverflow.com/questions/1909441/jquery-keyup-delay
	var delay = (function(){
	    var timer = 0;
	    return function(callback, ms){
	      clearTimeout (timer);
	      timer = setTimeout(callback, ms);
	    };
	})(); 

	var duplicateFilter=(function(){
	  var lastContent;
	  return function(content,callback){
	    content=$.trim(content);
	    if(content!=lastContent){
	      callback(content);
	    }
	    lastContent=content;
	  };
	})();
	// OLD $('#abc-text').keyup(updateABC);
	$("#abc-text").on("keyup",function(ev){
		  var self=this;
		  delay(function(){
		    duplicateFilter($(self).val(),function(c){
		    	updateABC();
		        // console.log(c);
		    });
		  }, 2000 );
		})
	//
	
	minSpeed = 20 ;
	maxSpeed = 400 ;
	stepSpeed = 5 ;
	$("#slider").slider({
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
	$("#slider").width("350px") ;
	$("#slider").slider("option" , "value" , speed);
	$("#slider-value").text(speed);
	$("#abc-edit-slider-size").slider ({
		min: 0.1 ,
		max: 1.3 ,
		step: 0.1 ,
		orientation: "vertical" ,
		change: function(event,ui){if (event.originalEvent){resizeABCscore()} }
	});
	if (localStorage.getItem(window.location.href + '-scoreSize') != null) {
		scoreSize = localStorage.getItem(window.location.href + '-scoreSize') ; }
	else { scoreSize = .8 ; }
	$("#abc-edit-slider-size").slider("option" , "value" , scoreSize);
	$("#abcscale").text(scoreSize) ;
	ABCJS.renderAbc('abc-edit', $("#abc-text").text() , {}, {scale: scoreSize},{});
	ABCJS.renderMidi('midi-edit',$("#abc-text").text(), {}) ;
	// tuneNotModified = $("#tuneNotModified").html() ;
	// $("#tuneNotModified").hide() ;
	// tuneModified = $("#tuneModified").html() ;
	$("#tuneModified").hide() ;
	isModified = false ;
	// $("#avertissementTuneModified").html(tuneNotModified);
	$("#view-nav").hide() ;
	if (localStorage.getItem(window.location.href + '-portalTopHidden') == 'true') {
		$("#portal-top").hide();
		$("#viewlet-above-content").hide();
		$("#edit-bar").hide();
		$("#view-nav").show() ;
	}
	if (localStorage.getItem(window.location.href + '-abcTextHidden') == 'true') {
		$('#abc-text').hide();
	}
});

});
