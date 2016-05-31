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

getOverall();