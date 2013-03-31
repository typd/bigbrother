var mins_to_str = function(){
    mins = this.value;
    if (mins < 60)
        return mins + " mins";
    hours = parseInt(mins / 60);
    mins = mins % 60;
    return hours.toString() + " h, " + mins.toString() + " m";
}

function stacked(yaxis) {
    var cln = jQuery.extend(true, {}, yaxis);
    cln['stackLabels'] = { enabled: true }
    return cln
}

var HC_TYPE_LINE = 'line';
var HC_TYPE_AREA = 'area';
var HC_TYPE_COLUMN = 'column';
var HC_XAXIS_WEEKDAY = { categories: [ 'Mon', 'Tus', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun' ] }
var HC_XAXIS_HOUR = { min: 0, max: 23 }
var HC_XAXIS_MINUTE = { min: 0, max: 24 * 60 }
var HC_XAXIS_INT = { }
var HC_YAXIS_TIME = { title: {text: 'time' }, labels: {formatter: mins_to_str} }
var HC_PLOT_STACKED = { column: {stacking: 'normal'}, dataLabels: { enabled: true}}

function drawChart(containerId, data, charttype, title, yAxis, xAxis, plotOptions) {
    $(function () {
        if (!plotOptions)
            plotOptions = {};
        plotOptions['fillOpacity'] = 0.5;
        var chart;
        $(document).ready(function() {
            chart = new Highcharts.Chart({
                    chart: {
                        renderTo: containerId,
                        type: charttype,
                        spacingBottom: 30
                    },
                    title: {
                        text: title
                    },
                    xAxis: xAxis, 
                    yAxis: yAxis,
                    tooltip: {
                        formatter: function() {
                            return '<b>'+ this.series.name +'</b><br/>'+
                                this.x +': '+ this.y;
                        }
                    },
                    plotOptions: plotOptions,
                    credits: {
                        enabled: false
                    },
                    series: data
            });
        });
    });
}
