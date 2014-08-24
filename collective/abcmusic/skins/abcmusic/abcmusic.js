/*
* generic JS for the entire site
*/
$(document).ready(function() {
	$("a.a-overlay").prepOverlay({
        subtype: 'ajax',
        // formselector: '.a-overlay',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *',
    });

	$("a#plone-contentmenu-actions-gettunes").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '',
    });
    /*
	$("div#get-tunes a.get-tunes-overlay").click(function(event){
		event.preventDefault();
		// $("div#get-tunes").html(content) ;
		console.log(this.href) ;
		// $("div.pb-ajax").load(url "#content");
		// $("#get-tunes").not(this).hide();
		console.log('get-tunes');
	});
	*/
	$("a").hover(function(event){
		console.log('div.pb-ajax a');
	});
	
	$(".overlaycontent td.contenttype-folder").prev().hide();
	$(".overlaycontent td.contenttype-folder").css("background-color","Red");
	
});