/************************************************************ *
 * ALL CODE COPYRIGHT 2009, Paul Osborne
 * 
 * @author Paul Osborne
 * @version January 17, 2009
 *************************************************************/
var map;
var markerManager;
var activeCourse = new Object();
activeCourse.courseId = -1;
var coursesChangedListeners = [];
var courses;

/**
 * Add a function on as a listener for an event where the active
 * courses on the map changes
 */
function addCoursesChangedListener(func) {
    coursesChangedListeners.push(func);
}

/**
 * Notify listeners that the course data has changed
 */
function notifyCoursesChanged() {
    $.each(coursesChangedListeners, function(i, func) {
        func(courses);
    });
}

/**
 * Create markers from the json response and notify registered listeners
 * of the change (passing on the courses)
 */
function createMarkersForJSON(json) {
    var coordinates = json.coordinates;
    var markers = [];
    var detailsUrlBase = 'http://www.pdga.com/course-details?id=';
    courses = [];
    $.each(coordinates, function(i, coordinate) {
            var mapPoint = new GLatLng(parseFloat(coordinate.lat), 
                                       parseFloat(coordinate.lon));
            courses.push({'courseName': coordinate.name,
			'courseId': coordinate.id,
			'lat': coordinate.lat,
			'lon': coordinate.lon,
			'city': coordinate.city,
			'state': coordinate.state,
			'numHoles': coordinate.numholes});
            var icon = new GIcon(G_DEFAULT_ICON);
            if (coordinate.id == activeCourse.courseId) {
                icon.image = '/images/markeryellow.png';
                icon.iconSize = new GSize(20, 34);
                icon.iconAnchor = new GPoint(9, 34);
                activeCourse = courses[courses.length - 1]; // most recent
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
    notifyCoursesChanged();
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
    activeCourse.courseId = id;
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

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */
/*  Vincenty Inverse Solution of Geodesics on the Ellipsoid (c) Chris Veness 2002-2008            */
/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  */

/*
 * Calculate geodesic distance (in m) between two points specified by latitude/longitude 
 * (in numeric degrees) using Vincenty inverse formula for ellipsoids
 */
function distVincenty(lat1, lon1, lat2, lon2) {
    var a = 6378137, b = 6356752.3142,  f = 1/298.257223563;  // WGS-84 ellipsiod
    var L = (lon2-lon1).toRad();
    var U1 = Math.atan((1-f) * Math.tan(lat1.toRad()));
    var U2 = Math.atan((1-f) * Math.tan(lat2.toRad()));
    var sinU1 = Math.sin(U1), cosU1 = Math.cos(U1);
    var sinU2 = Math.sin(U2), cosU2 = Math.cos(U2);
  
    var lambda = L, lambdaP, iterLimit = 100;
    do {
        var sinLambda = Math.sin(lambda), cosLambda = Math.cos(lambda);
        var sinSigma = Math.sqrt((cosU2*sinLambda) * (cosU2*sinLambda) + 
          (cosU1*sinU2-sinU1*cosU2*cosLambda) * (cosU1*sinU2-sinU1*cosU2*cosLambda));
        if (sinSigma==0) return 0;  // co-incident points
        var cosSigma = sinU1*sinU2 + cosU1*cosU2*cosLambda;
        var sigma = Math.atan2(sinSigma, cosSigma);
        var sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma;
        var cosSqAlpha = 1 - sinAlpha*sinAlpha;
        var cos2SigmaM = cosSigma - 2*sinU1*sinU2/cosSqAlpha;
        if (isNaN(cos2SigmaM)) cos2SigmaM = 0;  // equatorial line: cosSqAlpha=0 (§6)
        var C = f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha));
        lambdaP = lambda;
        lambda = L + (1-C) * f * sinAlpha *
          (sigma + C*sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)));
    } while (Math.abs(lambda-lambdaP) > 1e-12 && --iterLimit>0);

    if (iterLimit==0) return NaN  // formula failed to converge

    var uSq = cosSqAlpha * (a*a - b*b) / (b*b);
    var A = 1 + uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq)));
    var B = uSq/1024 * (256+uSq*(-128+uSq*(74-47*uSq)));
    var deltaSigma = B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-
    B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)));
    var s = b*A*(sigma-deltaSigma);

    s = s.toFixed(3); // round to 1mm precision
    return s;
}

Number.prototype.toRad = function() {  // convert degrees to radians
  return this * Math.PI / 180;
}

