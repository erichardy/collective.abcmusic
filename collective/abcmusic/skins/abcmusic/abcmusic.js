/*
* generic JS for the entire site
*/
$(document).ready(function() {
	$("a.a-overlay").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });
});