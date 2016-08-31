function color_factor() {
    return Math.round(Math.random() * 255);
}

for (var i = 0; i < data.length; i++) {
    data[i]['lineTension'] = 0;
    data[i]['fill'] = false;

    var color = 'rgba(' + color_factor() + ',' + color_factor() + ',' + color_factor() + ',';
    data[i]['borderColor'] = color + '.6)';
    data[i]['backgroundColor'] = color + '.8)';
}

var scatterChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: data
    },
    options: {
        scales: {
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    display: true,
                    labelString: 'Time (minutes)'
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Team Score'
                }
            }]
        },
        title: {
            display: true,
            text: 'Score Progression'
        },
        responsive: true
    }
});