function submit_course_review() {
    FB.requireSession(function() {
        review_text = $('#reviewtext').value;
        rating = $('#rating_select').options[$('#rating_select').selectedIndex].value;
        $.post("../addcoursereview/", { courseRating: rating, review: review_text, courseId: activeCourse });
    });
}
