var url = "http://archive.mozilla.org/pub/mobile/tinderbox-builds/mozilla-inbound-android-api-15/1460592646/mozilla-inbound_ubuntu64_vm_armv7_mobile_test-robocop-2-bm54-tests1-linux64-build54.txt.gz"
var oReq = new XMLHttpRequest();
oReq.onload = function(e) {
    var buffer = oReq.responseText;

    var i=1;
    buffer.split('\n').forEach(function(line) {
        $("#log-container").append('<p class="lv-log-line"><a class="lv-line-num">'+i+'</a><span class="lv-line-text">'+line+'</span></p>');
        i++;
    });
  /* ... */
}
oReq.open("GET", url);
oReq.send();
