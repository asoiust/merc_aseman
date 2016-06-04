$(function () {
    $('#overall').highcharts({
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            }
        },
        title: {
            text: 'Overall'
        },
        subtitle: {
            text: 'subtitle'
        },
        plotOptions: {
            pie: {
                innerSize: 100,
                depth: 45
            }
        },
        series: [{
            name: 'Delivered amount',
            data: [
                ['positive', 100],
                ['Vary positive', 356],
                ['Mostly Positive', 1120],
                ['Overwhelmingly Positive', 600]

            ]
        }]
    });

    var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };

    // The speed gauge
    $('#price-average').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 500,
            title: {
                text: 'Price Average'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'dollar',
            data: [21],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">$/game</span></div>'
            },
            tooltip: {
                valueSuffix: ' km/h'
            }
        }]

    }));

    // The RPM gauge
    $('#discount-average').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 500,
            title: {
                text: 'Discount Average'
            }
        },

        series: [{
            name: 'dollar',
            data: [12],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                       '<span style="font-size:12px;color:silver">$ / game</span></div>'
            },
            tooltip: {
                valueSuffix: ' revolutions/min'
            }
        }]

    }));

    // Bring life to the dials
    setTimeout(function () {
        // Speed
        var chart = $('#price-average').highcharts(),
            point,
            newVal,
            inc;

        if (chart) {
        //     point = chart.series[0].points[0];
            // inc = Math.round((Math.random() - 0.5) * 100);
            // newVal = point.y + inc;

            // if (newVal < 0 || newVal > 200) {
            //     newVal = point.y - inc;
            // }

            // point.update(newVal);
        }

        // RPM
        chart = $('#discount-average').highcharts();
        if (chart) {
            // point = chart.series[0].points[0];
            // inc = Math.random() - 0.5;
            // newVal = point.y + inc;
            //
            // if (newVal < 0 || newVal > 5) {
            //     newVal = point.y - inc;
            // }
            //
            // point.update(newVal);
        }
    }, 2000);



});



function getOverall() {
    var xmlObject = new XMLHttpRequest();
    xmlObject.onreadystatechange = function () {
        if(xmlObject.readyState == 4 && xmlObject.status == 200){
            console.log("kir");
            console.log(xmlObject.responseText);
            var jsonObject = JSON.parse(xmlObject.responseText);
                $(function () {
        $('#overall').highcharts({
            chart: {
                type: 'pie',
                options3d: {
                    enabled: true,
                    alpha: 45
                }
            },
            title: {
                text: 'Overall'
            },
            subtitle: {
                text: 'subtitle'
            },
            plotOptions: {
                pie: {
                    innerSize: 100,
                    depth: 45
                }
            },
            series: [{
                name: 'Delivered amount',
                data: [
                    ['positive', jsonObject[1]],
                    ['Vary positive', jsonObject[0]],
                    ['Mostly Positive', jsonObject[3]],
                    ['Overwhelmingly Positive', jsonObject[2]]

                ]
            }]
        });
});
        }
    };
    xmlObject.open("POST", "/statistics", true);
    xmlObject.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    xmlObject.send("requestType=overall");
}


function getPriceAverages(){
    var xmlObject = new XMLHttpRequest();
    xmlObject.onreadystatechange = function () {
        if(xmlObject.readyState == 4 && xmlObject.status == 200){
             var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };var jResult = JSON.parse(xmlObject.responseText);
            $('#price-average').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 500,
            title: {
                text: 'Price Average'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'dollar',
            data: [Number(jResult[0])],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                       '<span style="font-size:12px;color:silver">$/game</span></div>'
            },
            tooltip: {
                valueSuffix: ' km/h'
            }
        }]

    }));

        }
    };
    xmlObject.open("POST", "/statistics", true);
    xmlObject.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    xmlObject.send("requestType=aveofall");

}

function getDiscountAverages(){
    var xmlObject = new XMLHttpRequest();
    xmlObject.onreadystatechange = function () {
        if(xmlObject.readyState == 4 && xmlObject.status == 200){
             var gaugeOptions = {

        chart: {
            type: 'solidgauge'
        },

        title: null,

        pane: {
            center: ['50%', '85%'],
            size: '140%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },

        tooltip: {
            enabled: false
        },

        // the value axis
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -70
            },
            labels: {
                y: 16
            }
        },

        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    };var jResult = JSON.parse(xmlObject.responseText);
 $('#discount-average').highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: 500,
            title: {
                text: 'Discount Average'
            }
        },

        series: [{
            name: 'dollar',
            data: [Number(JSON.parse(xmlObject.responseText)[0])],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                    ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                       '<span style="font-size:12px;color:silver">$ / game</span></div>'
            },
            tooltip: {
                valueSuffix: ' revolutions/min'
            }
        }]

    }));

        }
    };
    xmlObject.open("POST", "/statistics", true);
    xmlObject.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    xmlObject.send("requestType=averageDiscount");

}

getOverall();
getPriceAverages();
getDiscountAverages();