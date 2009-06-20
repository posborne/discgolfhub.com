var TESTING = true;
if (TESTING) {
    FB_API_KEY = 'ca48b6923a4819cd461499d22e9f1f83';
} else {
    FB_API_KEY = '05ef2c8b16b7e5d99da222965006275a';
}

/** Unobtrusive onload */
$(document).ready(function() {
    facebook_connect();
    $('#query').val("Search Courses");
    $('#query').css({'color': '#999'});
    
    // onfocus, if default, empty and make text dark
    $('#query').focus(function() {
        if ($(this).val() == 'Search Courses') {
            $(this).val('');
            $(this).css({'color': '#000'});
        }
    });
    
    // onblur, if empty, fill with text and gray text
    $('#query').blur(function() {
        if ($(this).val() == '') {
            $(this).val("Search Courses");
            $(this).css({'color': '#999'});
        }
    });
    
});

/**
 * Setup the initial connection to facebook and start loading of
 * necessary libraries.  If the user is logged in update the box so
 * that it shows the logged in user's information
 */
function facebook_connect() {
    FB.init(FB_API_KEY, "../connect/xd_receiver.htm");
    // ensure init since libraries are loaded asynchronously
    FB.ensureInit(function() {
        FB.Connect.ifUserConnected(update_login_box, null);
    });
}

/**
 * Logout of facebook and reload the page to have the full, lame
 * logged out experience
 */
function facebook_logout() {
    FB.Connect.logout(function() {
        window.parent.location.href = "../home/";
    });
}

/**
 * Change the login box so that it displays the user's name, profile
 * picture, and links for changing settings and logging out of their
 * facebook profile
 */
function update_login_box() {
    $("#login").hide("normal", function() {
        $("#loggedin").show("normal");
    });
}
