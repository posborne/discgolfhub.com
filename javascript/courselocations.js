/**************************************************************
 * ALL CODE COPYRIGHT 2009, Paul Osborne
 * 
 * @author Paul Osborne
 * @version January 17, 2009
 *************************************************************/
var map;
var markerManager;

function createMarkersForJSON(json) {
    // The JSON for the markers is in the form
    // { "coordinates": [
    //    { ...},
    //    { ...},
    //    ...
    // ] }
    var coordinates = json.coordinates;
    var markers = [];
    var detailsUrlBase = 'http://www.pdga.com/course-details?id=';
    $.each(coordinates, function(i, coordinate) {
            var mapPoint = new GLatLng(parseFloat(coordinate.lat), 
                                       parseFloat(coordinate.lon));
            var icon = new GIcon(G_DEFAULT_ICON);
            //icon.iconSize = new GSize(10, 15);
            icon.shadow = '';
            icon.shadowSize = new GSize(0,0);
            var marker = new GMarker(mapPoint, {title: coordinate.name + " (" + coordinate.numholes + ")", icon: icon});
            GEvent.addListener(marker, "click", function() {
                    var myHtml = "<strong>" + coordinate.name + "</strong>";
                    myHtml += "<br />Holes: " + coordinate.numholes;
                    myHtml += "<br /><a href=\"" + detailsUrlBase + coordinate.id + "\">Visit at PDGA</a>";
                    map.openInfoWindowHtml(mapPoint, myHtml);
			});
            map.addOverlay(marker);
	});
    markerManager.addMarkers(markers, 1);
}

/**
 * Initialize the page connection to facebook.
 * @return
 */
function connectFacebook() {
    FB_RequireFeatures(["XFBML"], function() {
            FB.Facebook.init("05ef2c8b16b7e5d99da222965006275a", "connect/xd_receiver.htm");
        });
}

/**
 * Load the google map centered somewhere in the midwest.  Set up the
 * appropriate display parameters
 */
function loadGoogleMap() {
    if (GBrowserIsCompatible()) {
	  var mapDiv = document.getElementById("map");
          map = new GMap2(mapDiv);
          map.setCenter(new GLatLng(38.27268853598097, -92.724609375), 4);
          map.addControl(new GSmallZoomControl());
          var mgrOptions = { borderPadding: 100, maxZoom: 15, trackMarkers: true };
          markerManager = new MarkerManager(map, mgrOptions);
    }
}

function zoomAndCenter(zipCode) {
    var geocoder = new GClientGeocoder();
    geocoder.getLatLng(
                       zipCode,
			function(point) {
                           if (!point) {
                               alert("Couldn't find: " + zipCode);
                           } else {
                               $.getJSON("/getpoints/?lat=" + point.lat() + "&lon=" + point.lng(), createMarkersForJSON);
                               map.setCenter(point, 10);
                           }
                       });
}

