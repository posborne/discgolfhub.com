/* Requires FB connect to be loaded into namespace */

/**
 * Initialize the page connection to facebook.
 */
function connectFacebook() {
    FB_RequireFeatures(["XFBML"], function() {
        FB.Facebook.init("05ef2c8b16b7e5d99da222965006275a", "connect/xd_receiver.htm");
    });
}


function update_login_box() {
    $('#login').html(
        "<span style='float:left; margin-right: 15px'>" +
	"You are logged in<br /> as <fb:name uid='loggedinuser' useyou='false'></fb:name><br />" +
	"</span>" +
	"<fb:profile-pic uid='loggedinuser' facebook-logo='true' size='square'></fb:profile-pic>" +
	"</span>");
    FB.XFBML.Host.parseDomTree();
}
