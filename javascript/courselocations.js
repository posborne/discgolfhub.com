/************************************************************ *
 * ALL CODE COPYRIGHT 2009, Paul Osborne
 * 
 * @author Paul Osborne
 * @version January 17, 2009
 *************************************************************/
var map;
var markerManager;
var activeCourse = -1; 

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
            if (coordinate.id == activeCourse) {
                icon.image = '/images/markeryellow.png';
                icon.iconSize = new GSize(20, 34);
                icon.iconAnchor = new GPoint(9, 34);
            }
            icon.shadow = '';
            icon.shadowSize = new GSize(0,0);
            var marker = new GMarker(mapPoint, {title: coordinate.name + " (" + coordinate.numholes + ")", icon: icon});
            GEvent.addListener(marker, "click", function() {
                    var myHtml = "<div style='font-size: 70%'>" +
                        "<strong><a href='/coursepage/?id=" + coordinate.id + "'>" + coordinate.name + "</a></strong>" +
                        "<br/>" + coordinate.city + ", " + coordinate.state +
                        "<br />Holes: " + coordinate.numholes +
                        "<br /><a href=\"" + detailsUrlBase + coordinate.id + "\">Visit at PDGA</a>" +
                        "</div>";
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
 * For a course page we need some state variable which tells us which course
 * is the course we are currently focused on so we can show it in a different
 * color.  This function lets us mutate that variable
 */
function setActiveCourse(id) {
    activeCourse = id;
}

/**
 * Load the google map centered somewhere in the midwest.  Set up the
 * appropriate display parameters
 */
function loadGoogleMap() {
    if (GBrowserIsCompatible()) {
	  var mapDiv = document.getElementById("map");
          map = new GMap2(mapDiv);
          // 38.27268853598097, -92.724609375 is 
          // somewhere around kansas with zoomlevel 4
          map.setCenter(new GLatLng(38.27268853598097, -92.724609375), 4);
          map.addControl(new GLargeMapControl3D());
          map.addControl(new GMapTypeControl());
          var mgrOptions = { borderPadding: 100, maxZoom: 15, trackMarkers: true };
          markerManager = new MarkerManager(map, mgrOptions);
    }
}

/**
 * When we really know where we want to go we load that point at a higher zoom
 * level with the marker colored differenetly.
 */
function zoomAndCenterCoordinate(latitude, longitude) {
    map.setCenter(new GLatLng(latitude, longitude), 13);
    $.getJSON("/getpoints/?lat=" + latitude + "&lon=" + longitude, createMarkersForJSON);
}

function zoomAndCenter(zipCode) {
    var geocoder = new GClientGeocoder();
    geocoder.getLatLng(zipCode,
                       function(point) {
                           if (!point) {
                               alert("Couldn't find: " + zipCode);
                           } else {
                               $.getJSON("/getpoints/?lat=" + point.lat() + "&lon=" + point.lng(), createMarkersForJSON);
                               map.setCenter(point, 10);
                           }
                       });
}

