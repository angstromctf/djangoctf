var START = 1460217600; //Start date of the competition, in seconds since epoch
var END = 1460865600; //End date of the competition, in seconds since epoch

var PAD = 10;
var DATA = "abcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()-_=+[]\\;',./<>?:\"{}|";

var back = [];
var back_width, back_height;

function setupTitle() {
    var canvas = document.getElementById("title-canvas");
    canvas.width = $("body").prop("clientWidth");
    canvas.height = canvas.width/3;
    var ctx = canvas.getContext("2d");

    ctx.font = "10pt monospace";
    var metrics = ctx.measureText("a");
    back_width = Math.floor((canvas.width-PAD)/(metrics.width+PAD));
    back_height = Math.floor((canvas.height-PAD)/(10+PAD));

    for (var j = 0; j < back_height; j++) {
        var arr = [];
        for (var i = 0; i < back_width; i++) {
            arr.push([Math.floor(10+Math.random()*200), DATA[Math.floor(Math.random()*DATA.length)]]);
        }

        back.push(arr);
    }

    renderTitle();
}

function renderTitle() {
    var canvas = document.getElementById("title-canvas");
    var ctx = canvas.getContext("2d");

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = "10pt monospace";
    var metrics = ctx.measureText("a");

    ctx.textBaseline = "top";

    for (var j = 0; j < back_height; j++) {
        for (var i = 0; i < back_width; i++) {
            ctx.fillStyle = "rgb(0,"+back[j][i][0]+",0)";
            ctx.fillText(back[j][i][1], PAD+i*(metrics.width+PAD), PAD+j*(10+PAD));
        }
    }

    ctx.font = canvas.height/5 + "pt monospace";
    ctx.fillStyle = "white";
    ctx.textBaseline = "middle";

    metrics = ctx.measureText("angstromCTF 2");
    ctx.fillText("angstromCTF 2", canvas.width/2-metrics.width/2, canvas.height/2);

    ctx.font = canvas.height/15 + "pt monospace";
    ctx.fillStyle = "#AAF";

    metrics = ctx.measureText("hacking competition coming this winter");
    ctx.fillText("hacking competition coming this winter", canvas.width/2-metrics.width/2, 3*canvas.height/4);

    for (var j = back_height-1; j > 0; j--) {
        back[j] = back[j-1];
    }

    var arr = [];
    for (var i = 0; i < back_width; i++) {
        arr.push([Math.floor(10+Math.random()*200), DATA[Math.floor(Math.random()*DATA.length)]]);
    }
    back[0] = arr;
}
/*
function renderTime() {
    var canvas = document.getElementById("clock");
    var ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth / 1.5;
    canvas.height = canvas.width / 4;

    var cur_time = Date.now()/1000;

    if (cur_time < START) {
        var seconds = START - cur_time;
    } else if (Date.now()/1000 < END) {
        var seconds = END - cur_time;
    } else {
        var seconds = 0;
    }

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
    ctx.font = Math.floor(canvas.height/10).toString() + "pt Lato";//font
    for (i = 0; i < 4; i++) {
        ctx.fillText(times[i], canvas.width * (2*i+1)/8, canvas.height/2);
    }

    ctx.textBaseline = "top";
    ctx.font = Math.floor(canvas.height/15).toString() + "pt Lato";
    for (i = 0; i < 4; i++) {
        var unit = units[i];

        if (times[i] != 1) unit += "S";//plural units

        ctx.fillText(unit, canvas.width * (2*i+1)/8, canvas.height/2);
    }

    var head = document.getElementById("time");
    if (cur_time < START) {
        head.innerHTML = "Competition has not yet started! Time until start:";
    } else if (cur_time < END) {
        head.innerHTML = "Competition has begun! Time remaining:";
    } else {
        head.innerHTML = "Competition is over!";
    }
}

var canvas = document.getElementById("clock");

canvas.width = window.innerWidth / 1.5;
canvas.height = canvas.width / 4;
*/

$(window).load( function startRendering() {
    setupTitle();
    window.setInterval(renderTitle, 200);
});