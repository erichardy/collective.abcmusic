$(document).ready(function() {
	var coords = [43.601092044498785, 1.4432430267333984]
	var coords = [3.601092044498785, 1.4432430267333984]
	var map = L.map('myMap', {
	    center: coords ,
	    zoom: 13
	});
	
	var osmTiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: 'OpenStreetMap'
	});
	osmTiles.addTo(map);
	stamenTiles = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {
	    attribution: 'Stamen'
	});
	stamenTiles.addTo(map);
	opacity = 0.5
	stamenTiles.setOpacity(opacity);
	var MapQuestOpen_Aerial = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/{type}/{z}/{x}/{y}.{ext}', {
		type: 'sat',
		ext: 'jpg',
		attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency',
		subdomains: '1234'
	});

	var baseLayers = {
			"Stamen": stamenTiles,
			"OpenStreetMap": osmTiles,
			"MapQuestOpen_Aerial": MapQuestOpen_Aerial
	}
	
	terrasses = L.geoJson(null);
	terrasses.addData(terrassesGEOJSON) ;
	var overlays = {
			"Terrasses": terrasses
	}
	L.control.layers(baseLayers, overlays).addTo(map);

	terrasses.addTo(map);
	// on prend la BoundingBox de l'objet terrasses
	terrassesBounds = terrasses.getBounds()
	// et on cale la map sur cette bounding box
	map.fitBounds(terrassesBounds)
	
	// Popup avec texte "fixe", le mme pour tous les points
	terrasses.bindPopup("une terrasse...")

	$("#plus").click(function(){
		opacity = opacity + 0.1
		if (opacity > 1) {opacity = 1};
		stamenTiles.setOpacity(opacity);
		console.log(opacity)
	});
	$("#moins").click(function(){
		opacity = opacity - 0.1
		if (opacity < 0) {opacity = 0};
		stamenTiles.setOpacity(opacity);
		console.log(opacity)
	});

});