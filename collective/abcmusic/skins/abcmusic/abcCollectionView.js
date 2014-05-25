/*
$(document).ready(function() {
	$( "#accordion" ).accordion();
});
*/
jQuery(document).ready(function($) {

$(document).ready(function() {
	$("a.contenttype-abctune").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });

});

});
