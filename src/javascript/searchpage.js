/*******************************************************************************
 * Copyright (c) 2009, Paul Osborne
 * 
 * This module contains funtionality specific to the search results page.
 * 
 * @author Paul Osborne
 * @version July 19, 2009
 ******************************************************************************/

var map = null;
var geocoder = new GClientGeocoder();

/**
 * Clear markers, create a marker, and center the map at the point.
 * 
 * @param gepoint
 *            The GLatLng at which the map should be centered and marker
 *            displayed
 */
function _createMarkerAtPoint(geopoint, courseName) {
    var courseMarker = new GMarker(geopoint, {title: courseName});
	map.clearOverlays();
	map.addOverlay(courseMarker);
    map.setCenter(geopoint, 11);
}

/**
 * Show the the provided course on the map... clear any existing overlays and
 * tie in the course name.
 * 
 * @param courseId
 *            The id of the course to show
 * @param courseName
 *            The name of the course to show
 * @param lat
 *            The latitude of the course to show
 * @param lon
 *            The longitude of the course to show
 */
function showonmap(courseId, courseName, lat, lon, city, state) {
	if (map == null) {
		map = new GMap2(document.getElementById("map"));
	}
	
	// display the course on the map, geocode if needed
	if (lat == 0.0 && lon == 0.0) {
		geocoder.getLatLng(city + ", " + state,
						   function(point) {_createMarkerAtPoint(point, courseName);});
	} else {
		_createMarkerAtPoint(new GLatLng(lat, lon), courseName);
	}
	
	// set the caption
    $('#mapcaption').html("<strong>Course: </strong>" 
    		+ "<a href='../coursepage/?id=" + courseId + "'>" + courseName + "</a>"
    		+ "<br />" + city + ", " + state);
    if (lat == 0.0 && lon == 0.0) {
    	$('#mapcaption').html($('#mapcaption').html() + "<br /><em>Note: No GPS data available, showing city</em>");
    }
}

function positionMapContainer() {
	mc = $('#mapcontainer');
	content = $('#content');
	offset = content.offset();
	mc.css('left', (offset.left + 630) + "px");
	top = offset.top 
	mc.css('top', offset.top + "px");
}

// add listeners
$(window).resize(positionMapContainer);
$(document).ready(positionMapContainer);
$(window).scroll(positionMapContainer);
