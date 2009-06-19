function submit_course_review() {
    FB.requireSession(function() {
        review_text = $('#reviewtext').value;
        rating = $('#rating_select').options[$('#rating_select').selectedIndex].value;
	template_data = {
	    'courseId': targetCourse.courseId,
	    'courseName': targetCourse.courseName,
	    'rating': rating };
	FB.Connect.showFeedDialog(83346882395, template_data, null, null, null, FB.RequireConnect.require, null, "Share your review?", null);
        $.post("../addcoursereview/", { courseRating: rating, review: review_text, courseId: activeCourse });
    });
}

function show_review_preview() {
    review_text = $('#reviewtext').val();
    $.post("http://markdown-service.appspot.com/markdown", { content: review_text },
        function(data) {
            $('#previewbox').html(data);
            $('#previewbox').show();
        });
}

function publish_review_feed() {
    rating = $('#rating').val();
    template_data = {
	    'courseId': activeCourse.courseId,
	    'courseName': activeCourse.courseName,
	    'courseRating': rating };
    FB.Connect.showFeedDialog(83346882395, template_data);
    return true;
}

// Note that courses is an external variable located in dghub.js
$(document).ready(function() {
    addCoursesChangedListener(function(courses) {
        // first, let's calculate distance for each from center point
        targetLat = activeCourse.lat;
        targetLon = activeCourse.lon;
        $.each(courses, function(i, course) {
            // there are 1 609.344 meters/mile
            course.displacement = distVincenty(targetLat, targetLon,
                                          course.lat, course.lon) / 1609.344;
            course.displacement = Math.round(course.displacement * 10) / 10.0;
        });
        
        courses.sort(function(a,b) {
            return (a.displacement - b.displacement);
        });

        $('#nearby_courses').html('');
        var toAppend = '<table>';
        for (i = 1; i < 11; i++) {
            course = courses[i];
            toAppend += "<tr><td style='padding-right: 15px'>" + course.displacement + " mi</td>";
            toAppend += "<td><a href='../coursepage/?id=" + 
                course.courseId + "'>" + course.courseName + "</a> (" +
		course.numHoles + " holes)</td></tr>";    
        }
        toAppend += "</table>";
        $('#nearby_courses').append(toAppend);
    });
});

// toggle directions
$(document).ready(function() {
        $("#destpar").hide();
        $("#dirbut").click(function() {
            $("#destpar").toggle("normal");
        });
    });
