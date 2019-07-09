var daysLabel = document.getElementById("days");
var hoursLabel = document.getElementById("hours");
var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");

var lastServiceLabel = document.getElementById("last-service");
var serviceCountLabel = document.getElementById("service-count");
var totalSeconds = 0;

function start(initSeconds, lastService, serviceCount) {
    totalSeconds = initSeconds
    lastServiceLabel.innerHTML = lastService;
    serviceCountLabel.innerHTML = serviceCount;
    var socket = new WebSocket("ws://127.0.0.1:7676/");
    socket.onmessage = function(event) {
        var incomingMessage = event.data;
        var state = JSON.parse(incomingMessage);
        totalSeconds = state.total_seconds;
        lastServiceLabel.innerHTML = state.last_service;
        serviceCountLabel.innerHTML = state.services_count;
    };
    setInterval(setTime, 1000);
}

function setTime() {
    ++totalSeconds;

    var parts = normalizeTime(totalSeconds);

    daysLabel.innerHTML = pad(parts[0]);
    hoursLabel.innerHTML = pad(parts[1]);
    minutesLabel.innerHTML = pad(parts[2]);
    secondsLabel.innerHTML = pad(parts[3]);
}

function normalizeTime(totalSeconds) {
    var days = Math.floor(totalSeconds / 86400);
    totalSeconds = totalSeconds % 86400;

    var hours = Math.floor(totalSeconds / 3600);
    totalSeconds = totalSeconds % 3600;

    var minutes = Math.floor(totalSeconds / 60);
    var seconds = totalSeconds % 60;

    return [days, hours, minutes, seconds];
}

function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
        return "0" + valString;
    } else {
        return valString;
    }
}