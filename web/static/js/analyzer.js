var sessionId = getUuId();
var pointerX;
var pointerY;
var prevPointerX;
var prevPointerY;
var timestamp;
var moves = [];
var keys = [];

function pointerCheck() {
    if (prevPointerX != pointerX && prevPointerY != pointerY) {
        moves.push({"x": pointerX, "y": pointerY, "timestamp": timestamp, "session_id": sessionId, "event_type": "move"});
    }
}

function getUuId(){
    return String(Math.floor(Math.random() * 100) * Date.now());
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function poll(uri) {
    console.log("polling ", uri);
    $.ajax({
        type: 'GET',
        url: uri,
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(res) {
            if (!res['result']) {
                sleep(2000);
                poll(res['status_update']);
            } else {
                let image_id = res['result'];
                console.log("/images/" + image_id);
                window.open("/images/" + image_id);
            }
        },
        error: function () {
            alert('Failed polling request');
        }
    })
}

$(document).ready(function () {
    document.onmousemove = function(event) {
        prevPointerX = pointerX;
        prevPointerY = pointerY;
        pointerX = event.pageX;
        pointerY = event.pageY;
        timestamp = event.timeStamp;
    }

    document.onclick = function(event) {
        moves.push({"x": event.pageX, "y": event.pageY, "timestamp": event.timeStamp, "session_id": sessionId, "event_type": "click"});
    }

    document.onkeyup = function(event) {
        keys.push({"key": event.key, "keyCode": event.keyCode, "timestamp": event.timeStamp, "session_id": sessionId, "event_type": "press"});
    }

    document.onkeydown = function(event) {
        keys.push({"key": event.key, "keyCode": event.keyCode, "timestamp": event.timeStamp, "session_id": sessionId, "event_type": "release"});
    }

    setInterval(pointerCheck, 5);

    $('#bootstrapForm').submit(function (event) {
        event.preventDefault();
        document.getElementById('submitbutton').disabled = "disabled";
        var extraData = { "moves": moves, "keys": keys };
        $.ajax({
            data: JSON.stringify(extraData),
            type: 'POST',
            url: '/submit_form',
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(res) {
                if (res['result'] == 'success') {
                    alert('Form Submitted. Processing data...');
                    poll(res['redirect_url']);
                } else {
                    console.log(res);
                    alert('Failed sending form. Try again later');
                }
            },
            error: function (xhr, status, error) {
                // `xhr.responseText` usually contains the server's response, which might be an error message
                // `status` is a string describing the type of failure that occurred
                // `error` is an exception object in case of an exception or the HTTP status text
                alert('Failed sending form. Error: ' + xhr.responseText || error);
                console.error('Ajax error:', status, error);
            }
        })
    })
});