/*
 * A set of simple functions to support the demo application.
 */


var enableAV = function (elementId) {
    var avtag = document.getElementById(elementId);
    // Using hls.js for display, see: https://video-dev.github.io/hls.js/
    if (Hls.isSupported()) {
        var config = {
            xhrSetup: function (xhr, url) {
                xhr.withCredentials = true; // do send cookies
            }
        }

        var hls = new Hls(config);
        hls.loadSource(avtag.src);
        hls.attachMedia(avtag);
    }
};
