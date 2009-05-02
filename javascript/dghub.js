/** Unobtrusive onload */
$(document).ready(function() {
    facebook_connect();
});

/**
 * Setup the initial connection to facebook and start loading of
 * necessary libraries.  If the user is logged in update the box so
 * that it shows the logged in user's information
 */
function facebook_connect() {
    FB.init("05ef2c8b16b7e5d99da222965006275a", "../connect/xd_receiver.htm");
    
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
    $('#login').css({'font-size': '80%', "line-height": "1"});
    $('#login').html(
        "<span style='float:left; margin-right: 15px'>" +
        "You are logged in<br /> as <fb:name uid='loggedinuser' useyou='false'></fb:name><br />" +
        "</span>" +
        "<fb:profile-pic uid='loggedinuser' facebook-logo='true' size='square'></fb:profile-pic> <br />" +
        "<a href='#' onclick='facebook_logout()'>Logout of Facebook</a>");
    
    // reparse XFBML on the page
    FB.XFBML.Host.parseDomTree();
}
