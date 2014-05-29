/*
$(document).ready(function() {
	$( "#accordion" ).accordion();
});
*/
jQuery(document).ready(function($) {

	$( "#accordeon" ).accordion({
		header: "dt",
		heightStyle: "content",
		animate: 500,
		collapsible: true,
		active: false,
		});
	
/*
$(document).ready(function() {
	$("a.contenttype-abctune").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });

});
*/
});
