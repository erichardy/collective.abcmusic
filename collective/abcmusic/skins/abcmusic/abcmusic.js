/*
* generic JS for the entire site
*/
$(document).ready(function() {
	$("a.a-overlay").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });
	$("a#plone-contentmenu-actions-gettunes").prepOverlay({
        subtype: 'ajax',
        // part of Plone page going into pop-up dialog content area
        filter: '#content > *'
    });
	$("div#get-tunes p.get-tunes-parent").click(function(event){
		event.preventDefault();
		alert();
	})
});