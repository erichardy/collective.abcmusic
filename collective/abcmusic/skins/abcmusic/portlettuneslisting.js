
$(document).ready(function() {
	$(".portletTunesListingItem").click(function(){
		url = $(this).attr("value");
		// if isModified is not defined, we are not working on a tune
		if (typeof isModified == 'undefined') {
			window.location.replace(url);
			return ;
		}
		if (isModified == false){
			window.location.replace(url);
		}
		else {
			if (confirm(tuneModified)){
				window.location.replace(url);
			};
		}
	});
	val = '[value="' + window.location.href + '"]';
	$('.portletTunesListing ' + val).prop('selected', true) ;
});
