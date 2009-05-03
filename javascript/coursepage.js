function submit_course_review() {
    FB.requireSession(function() {
        review_text = $('#reviewtext').value;
        rating = $('#rating_select').options[$('#rating_select').selectedIndex].value;
        $.post("../addcoursereview/", { courseRating: rating, review: review_text, courseId: activeCourse });
    });
}

function show_review_preview() {
    review_text = $('#reviewtext').val();
    $.post("../mdpreview/", { mdtext: review_text },
        function(data) {
            $('#previewbox').html(data);
            $('#previewbox').show();    
        });
}
