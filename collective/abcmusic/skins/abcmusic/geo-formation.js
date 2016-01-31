$(document).ready(function() {
	var coords = [43.601092044498785, 1.4432430267333984]
	var coords = [3.601092044498785, 1.4432430267333984]
	var map = L.map('myMap', {
	    center: coords ,
	    zoom: 13,
	    maxZoom: 18
	});
	var currentMapName = 'Stamen';

	// EVENTS
	map.on('moveend', function(e){
		// console.log(e.name);
		// console.log("Center : " + map.getCenter());
		// console.log('zoom : ' + map.getZoom());
	});
	map.on('baselayerchange', function(e){
		currentMapName = e.name ;
		// console.log(currentMapName);
	})
	// END EVENTS
	
	// Déclaration des tuiles de fond de plan
	var osmTiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	    attribution: 'OpenStreetMap'
	});
	stamenTiles = L.tileLayer('http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png', {
	    attribution: 'Stamen'
	});
	var MapQuestOpen_Aerial = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/{type}/{z}/{x}/{y}.{ext}', {
		type: 'sat',
		ext: 'jpg',
		attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency',
		subdomains: '1234'
	});

	var localTiles = L.tileLayer("tiles/{z}/{x}/{y}.png")
	
	var baseLayers = {
//			currentMapName: stamenTiles,
			"OpenStreetMap": osmTiles,
			"MapQuestOpen Aerial": MapQuestOpen_Aerial,
			"localTiles": localTiles
	}
	baseLayers[currentMapName] = stamenTiles;
	baseLayers[currentMapName].addTo(map);
	opacity = 0.5
	baseLayers[currentMapName].setOpacity(opacity);
	// Fin Déclaration des tuiles de fond de plan

	var geojsonMarkerOptions = {
		    radius: 8,
		    fillColor: "#ff7800",
		    color: "#000",
		    weight: 1,
		    opacity: 1,
		    fillOpacity: 0.8
		};
	var cluster = L.markerClusterGroup();
	
	terrasses = L.geoJson(null, {
	    onEachFeature: function (feature, layer) {
	        layer.bindPopup(feature.properties.etablisseme + '<br />' + feature.properties.nature_acti);
	    },
        pointToLayer: function (feature, latlng) {
        	nature = feature.properties.nature_acti;
        	iconOptions = {size: 'm'};
        	// console.log(nature);
        	switch(nature){
	        	case "Terrasse ouverte-Extension terrasse":
	        		// geojsonMarkerOptions.fillColor = "Red";
	        		iconOptions.icon = "school" ;
	        		iconOptions.color = "#b00" ;
	        		break;
	        	case "Terrasse sur stationnement":
	        		// geojsonMarkerOptions.fillColor = "Green";
	        		iconOptions.icon = "park2" ;
	        		iconOptions.color = "#0b0" ;
	        		break;
	        	case "Terrasse ouverte":
	        		// geojsonMarkerOptions.fillColor = "Grey";
	        		iconOptions.icon = "cafe" ;
	        		iconOptions.color = "#b0b" ;
	        		break;
	        	case "Terrasse fermée":
	        		iconOptions.icon = "warehouse" ;
	        		iconOptions.color = '#bbb' ;
	        		// geojsonMarkerOptions.fillColor = "Yellow";
	        		break;
	        	case "Terrasse marquise":
	        		// geojsonMarkerOptions.fillColor = "Blue";
	        		iconOptions.icon = "school" ;
	        		iconOptions.color = "#aaa" ;
	        		break;
	        	case "Extension terrasse":
	        		// geojsonMarkerOptions.fillColor = "Black";
	        		iconOptions.icon = "school" ;
	        		iconOptions.color = "#444" ;
	        		break;
	        	default:
	        		iconOptions.icon = "cafe" ;
        			iconOptions.color = "#fff" ;	        	
        	}
        	// return L.circleMarker(latlng, geojsonMarkerOptions);
        	var terrasseIcon = L.MakiMarkers.icon(iconOptions) ;
        	return L.marker(latlng, {icon: terrasseIcon});
        }
        });
	terrasses.addData(terrassesGEOJSON) ;
	var overlays = {
			"Terrasses": cluster,
	}
	L.control.layers(baseLayers, overlays).addTo(map);

	cluster.addLayer(terrasses) ;
	cluster.addTo(map) ;
	// terrasses.addTo(map);
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