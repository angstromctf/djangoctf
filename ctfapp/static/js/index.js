var START = 1456808400;

function renderTime() {
    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth / 1.5;
    canvas.height = canvas.width / 4;

    var seconds = Math.abs(Date.now()/1000 - START);

    var dividers = [5184000, 86400, 3600, 60];
    var units = ["DAY", "HOUR", "MINUTE", "SECOND"];

    ctx.lineWidth = 15;
    ctx.strokeStyle = "firebrick";

    for (i = 0; i < 4; i++) {
        ctx.beginPath();
        ctx.arc(canvas.width * (2*i+1)/8, canvas.height/2, canvas.height/2.75, -Math.PI*.5,Math.PI*2*(seconds%dividers[i])/dividers[i]-Math.PI*.5);
        ctx.stroke();
    }

    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.font = "25pt Lato";
    for (i = 0; i < 4; i++) {
        var res = 1;

        if (i < 3) res = dividers[i+1];

        ctx.fillText(Math.round((seconds%dividers[i])/res), canvas.width * (2*i+1)/8, canvas.height/2);
    }

    ctx.textBaseline = "top";
    ctx.font = "15pt Lato";
    for (i = 0; i < 4; i++) {
        var unit = units[i];
        var res = 1;

        if (i < 3) res = dividers[i+1];

        if (Math.round((seconds%dividers[i])/res) != 1) unit += "S";

        ctx.fillText(unit, canvas.width * (2*i+1)/8, canvas.height/2);
    }
}

var canvas = document.getElementById("clock");
window.setInterval(renderTime, 1000);