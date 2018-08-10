/*
 * A set of simple functions to support the demo application.
 */


var enableAV = function(elementId) {
    var avtag = document.getElementById(elementId);
    // Using hls.js for display, see: https://video-dev.github.io/hls.js/
    if(Hls.isSupported()) {
        var hls = new Hls();
        hls.loadSource(avtag.src);
        hls.attachMedia(avtag);
    }
};