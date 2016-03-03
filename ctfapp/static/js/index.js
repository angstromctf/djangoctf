/*Javascript for index page. Handles the countdown clock. */

var START = 1997593702; //Start date of the competition, in seconds since epoch

function renderTime() {
    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth / 1.5;
    canvas.height = canvas.width / 4;

    var seconds = Math.abs(Date.now()/1000 - START);

    var dividers = [60, 24, 60, 60];//Days, hours, minutes, seconds
    var units = ["DAY", "HOUR", "MINUTE", "SECOND"];//units
    var times = new Array(4);

    var l = 1;
    for (i = 3; i >= 0; i--) {
        times[i] = Math.floor(seconds/l)%dividers[i];
        l *= dividers[i];
    }

    ctx.lineWidth = canvas.height/20;
    ctx.strokeStyle = "#AE73AE";//colour of the wheels

    for (i = 0; i < 4; i++) {//circles
        ctx.beginPath();
        ctx.arc(canvas.width * (2*i+1)/8, canvas.height/2, canvas.height/2.75, -Math.PI*.5,Math.PI*2*times[i]/dividers[i]-Math.PI*.5);
        ctx.stroke();
    }

    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.font = "2em Lato";//font
    for (i = 0; i < 4; i++) {
        ctx.fillText(times[i], canvas.width * (2*i+1)/8, canvas.height/2);
    }

    ctx.textBaseline = "top";
    ctx.font = "1.25em Lato";
    for (i = 0; i < 4; i++) {
        var unit = units[i];

        if (times[i] != 1) unit += "S";//plural units

        ctx.fillText(unit, canvas.width * (2*i+1)/8, canvas.height/2);
    }
}

var canvas = document.getElementById("clock");
window.setInterval(renderTime, 1000);//rerenders at set intervals

renderTime();
