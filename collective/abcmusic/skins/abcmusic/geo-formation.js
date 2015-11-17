$(document).ready(function() {
	var coords = [43.601092044498785, 1.4432430267333984]
	var coords = [3.601092044498785, 1.4432430267333984]
	var map = L.map('myMap', {
	    center: coords ,
	    zoom: 13
	});
	var currentMapName = 'Stamen';
	
	map.on('moveend', function(e){
		// console.log(e.name);
		// console.log("Center : " + map.getCenter());
		console.log('zoom : ' + map.getZoom());
	});
	map.on('baselayerchange', function(e){
		currentMapName = e.name ;
		console.log(currentMapName);
	})
	var osmTiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: 'OpenStreetMap'
	});
	// osmTiles.addTo(map);
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
			currentMapName: stamenTiles,
			"OpenStreetMap": osmTiles,
			"MapQuestOpen Aerial": MapQuestOpen_Aerial
	}
	// console.log(map.getPanes());
	var geojsonMarkerOptions = {
		    radius: 8,
		    fillColor: "#ff7800",
		    color: "#000",
		    weight: 1,
		    opacity: 1,
		    fillOpacity: 0.8
		};
	terrasses = L.geoJson(null, {
	    onEachFeature: function (feature, layer) {
	        layer.bindPopup(feature.properties.etablisseme + '<br />' + feature.properties.nature_acti);
	    },
        pointToLayer: function (feature, latlng) {
        	nature = feature.properties.nature_acti;
        	// console.log(nature);
        	switch(nature){
	        	case "Terrasse ouverte-Extension terrasse":
	        		geojsonMarkerOptions.fillColor = "Red";
	        		break;
	        	case "Terrasse sur stationnement":
	        		geojsonMarkerOptions.fillColor = "Green";
	        		break;
	        	case "Terrasse ouverte":
	        		geojsonMarkerOptions.fillColor = "Grey";
	        		break;
	        	case "Terrasse fermée":
	        		geojsonMarkerOptions.fillColor = "Yellow";
	        		break;
	        	case "Terrasse marquise":
	        		geojsonMarkerOptions.fillColor = "Blue";
	        		break;
	        	case "Extension terrasse":
	        		geojsonMarkerOptions.fillColor = "Black";
	        		break;
	        	default:
	        		geojsonMarkerOptions.fillColor = "White";	        	
        	}
        	return L.circleMarker(latlng, geojsonMarkerOptions);
        }
        });
	terrasses.addData(terrassesGEOJSON) ;
	var overlays = {
			"Terrasses": terrasses
	}
	L.control.layers(baseLayers, overlays).addTo(map);

	terrasses.addTo(map);
	// on prend la BoundingBox de l'objet terrasses
	terrassesBounds = terrasses.getBounds();
	// et on cale la map sur cette bounding box
	map.fitBounds(terrassesBounds);
	
	// Popup avec texte "fixe", le meme pour tous les points
	// terrasses.bindPopup("une terrasse...");

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