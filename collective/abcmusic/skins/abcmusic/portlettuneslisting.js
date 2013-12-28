
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
			if (confirm("tune changed... continue ?")){
				window.location.replace(url);
			};
		}
	});
});
