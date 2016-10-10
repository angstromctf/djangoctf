Chart.defaults.global.legend.position = 'right';

function draw_progression(ctx, display_legend) {
    var start = Math.round(Math.random() * 360);

    for (var i = 0; i < data.length; i++) {
        data[i]['lineTension'] = 0;
        data[i]['fill'] = false;

        var color = 'hsla(' + (start + 45 * i) % 360 + ',85%,50%,';
        console.log(color);
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
            responsive: true,
            legend: {
                display: display_legend
            }
        }
    });
}