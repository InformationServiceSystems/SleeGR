
/**
 *    Common functions to use with AMcharts
 *
 **/


// Realtime chart value holders
var gaugeChart1;
var gaugeChart2;
var gaugeChart3;

var areaChart1;
var areaChart2;

var lineChart2;


var gaugeChart1url;
var areaChart1url;
var areaChart2url;


var gIndex = 1;

var areaChart1Data = new Array();
var areaChart2Data = new Array();



var lineChart2Data = new Array();
// Daily date-value pairs - simple
function loadJSONData(url) {
    var request = new XMLHttpRequest();


    request.open('GET', url, false);
    request.send();
    data = eval(request.responseText);
    return data;

};





// Test js function for filling html from example data source end
function fillSingleDateDataExample(id, data) {
    var chart = new AmCharts.AmStockChart();
    chart.pathToImages = "./static/amcharts/images/";
    var dataSet = new AmCharts.DataSet();
    dataSet.dataProvider = data;
    dataSet.fieldMappings = [{ fromField: "value", toField: "value" }];
    dataSet.categoryField = "date";
    chart.dataDateFormat = "MM-DD-YYYY";
    chart.dataSets = [dataSet];

    var stockPanel = new AmCharts.StockPanel();
    chart.panels = [stockPanel];

    var panelsSettings = new AmCharts.PanelsSettings();
    panelsSettings.startDuration = 1;
    chart.panelsSettings = panelsSettings;

    var graph = new AmCharts.StockGraph();
    graph.valueField = "value";
    graph.type = "column";
    graph.fillAlphas = 1;
    graph.title = "MyGraph";
    stockPanel.addStockGraph(graph);

    chart.write(id);
    chart.validateData();
}


// Double Bar Date fill - constant for now 
/**
 @id: Which HTML element to be filled. 
 @dataset: Data
 @title: What is the title of the chart
 @xvaluefield: Horizontal axis values.
 */
function fillDoubleOverlay(id, dataset, title, units, xValueField, yValueField1, yValueField2, yTitle1, yTitle2, yText1, yText2) {
    var chart = AmCharts.makeChart(id, {
        "theme": "light",
        "type": "serial",
        "dataProvider": dataset,
        "valueAxes": [{
            "unit": units,
            "position": "left",
            "title": title,
        }],
        "startDuration": 1,
        "graphs": [{
            "balloonText": yText1         /* "GDP grow in [[category]] (2004): <b>[[value]]</b>"*/,
            "fillAlphas": 0.9,
            "lineAlpha": 0.2,
            "title": yTitle1,
            "type": "column",
            "valueField": yValueField1
        }, {
            "balloonText": yText2/*"GDP grow in [[category]] (2005): <b>[[value]]</b>"*/,
            "fillAlphas": 0.9,
            "lineAlpha": 0.2,
            "title": yTitle2,
            "type": "column",
            "clustered": false,
            "columnWidth": 0.5,
            "valueField": yValueField2
        }],
        "plotAreaFillAlphas": 0.1,
        "categoryField": xValueField,
        "categoryAxis": {
            "gridPosition": "start"
        },
        "export": {
            "enabled": true
        }

    });

}


function fillDoubleLineChart(id, dataset, categoryField, yValueField1, yValueField2, title, graphOneTitle, graphTwoTitle, axisTitle, dataDateFormat, minPeriod) {


    AmCharts.makeChart(id,
        {
            "type": "serial",
            "categoryField": categoryField,
            "dataDateFormat": dataDateFormat,
            "categoryAxis": {
                "minPeriod": minPeriod,
                "parseDates": true
            },
            "chartCursor": {
                "categoryBalloonDateFormat": "JJ:NN"
            },
            "chartScrollbar": {},
            "trendLines": [],
            "graphs": [
                {
                    "bullet": "round",
                    "id": "AmGraph-1",
                    "title": graphOneTitle,
                    "valueField": yValueField1
                },
                {
                    "bullet": "square",
                    "id": "AmGraph-2",
                    "title": graphTwoTitle,
                    "valueField": yValueField2
                }
            ],
            "guides": [],
            "valueAxes": [
                {
                    "id": "ValueAxis-1",
                    "title": axisTitle
                }
            ],
            "allLabels": [],
            "balloon": {},
            "legend": {
                "useGraphSettings": true
            },
            "titles": [
                {
                    "id": "Title-1",
                    "size": 15,
                    "text": title
                }
            ],
            "dataProvider":
               dataset
        }
    );
}

function fillRealTimeGaugeChart(id, url) {
    var gaugeChart = AmCharts.makeChart(id, {
        "type": "gauge",
        "theme": "light",
        "axes": [{
            "axisThickness": 1,
            "axisAlpha": 0.2,
            "tickAlpha": 0.2,
            "valueInterval": 20,
            "bands": [{
                "color": "#84b761",
                "endValue": 50,
                "startValue": 0
            }, {
                "color": "#fdd400",
                "endValue": 70,
                "startValue": 50
            }, {
                "color": "#cc4748",
                "endValue": 100,
                "innerRadius": "95%",
                "startValue": 70
            }],
            "bottomText": "0 % Metabolic Rate",
            "bottomTextYOffset": -20,
            "endValue": 100
        }],
        "arrows": [{}],
        "export": {
            "enabled": true
        }
    });
    if (gIndex === 1)
    {

        gaugeChart1 = gaugeChart;
        gaugeChart1url = url;
    }


}

function updateData()
{

   
    if (gaugeChart1) {
        json = loadJSONData(gaugeChart1url)
        //obj = JSON.parse(json);
        value = json[0].value;
        if (gaugeChart1.arrows) {
            if (gaugeChart1.arrows[0]) {
                if (gaugeChart1.arrows[0].setValue) {
                    gaugeChart1.arrows[0].setValue(value);
                    gaugeChart1.axes[0].setBottomText(value + " % Metabolic Rate");
                }
            }
        }
    }
    if (areaChart1) {
        json = loadJSONData(areaChart1url)
        
        date = new Date();
        value = json[0].value;
        var dataPoint = { "date": date, "value": value };
        areaChart1Data.push(dataPoint)
        areaChart1.validateData();

    }

    if (areaChart2) {
        json = loadJSONData(areaChart2url)
        
        
        date = new Date();
        value = json[0].value;
        var dataPoint = { "date": date, "value": value };
        areaChart2Data.push(dataPoint)
        areaChart2.validateData();

    }

}

function fillRealTimeAreaChart1(id,url)
{
    var chart = AmCharts.makeChart(id, {
        "type": "serial",
        "theme": "light",
        "dataProvider":areaChart1Data,
        "valueAxes": [{
            "axisAlpha": 0,
            "dashLength": 4,
            "position": "left"
        }],
        "graphs": [{
            "bulletSize": 14,
            "customBullet": "http://www.amcharts.com/lib/3/images/star.png?x",
            "customBulletField": "customBullet",
            "valueField": "value",
            "balloonText": "<div style='margin:10px; text-align:left;'><span style='font-size:13px'>[[category]]</span><br><span style='font-size:18px'>Value:[[value]]</span>",
        }],
        "marginTop": 20,
        "marginRight": 70,
        "marginLeft": 40,
        "marginBottom": 20,
        "chartCursor": {
            "graphBulletSize": 1.5
        },
        "autoMargins": false,
        "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
        "categoryField": "date",
        "categoryAxis": {
            "parseDates": true,
            "axisAlpha": 0,
            "gridAlpha": 0,
            "inside": true,
            "tickLength": 0
        },
        "export": {
            "enabled": true
        }
    });
    areaChart1 = chart;
    areaChart1url = url;
}



function fillRealTimeAreaChart2(id,url) {
    var chart = AmCharts.makeChart(id, {
        "type": "serial",
        "theme": "light",
        "dataProvider": areaChart2Data,
        "valueAxes": [{
            "axisAlpha": 0,
            "dashLength": 4,
            "position": "left"
        }],
        "graphs": [{
            "bulletSize": 14,
            "customBullet": "http://www.amcharts.com/lib/3/images/star.png?x",
            "customBulletField": "customBullet",
            "valueField": "value",
            "balloonText": "<div style='margin:10px; text-align:left;'><span style='font-size:13px'>[[category]]</span><br><span style='font-size:18px'>Value:[[value]]</span>",
        }],
        "marginTop": 20,
        "marginRight": 70,
        "marginLeft": 40,
        "marginBottom": 20,
        "chartCursor": {
            "graphBulletSize": 1.5
        },
        "autoMargins": false,
        "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
        "categoryField": "date",
        "categoryAxis": {
            "parseDates": true,
            "axisAlpha": 0,
            "gridAlpha": 0,
            "inside": true,
            "tickLength": 0
        },
        "export": {
            "enabled": true
        }
    });
    
    areaChart2 = chart;
    areaChart2url = url;
}

setInterval(updateData, 10000);


// set random value
/*
function randomValue() {
    var value = Math.round(Math.random() * 100);
    if (gaugeChart1) {
        if (gaugeChart1.arrows) {
            if (gaugeChart1.arrows[0]) {
                if (gaugeChart1.arrows[0].setValue) {
                    gaugeChart1.arrows[0].setValue(value);
                    gaugeChart1.axes[0].setBottomText(value + " Metabolic Rate");
                }
            }
        }
    }
}
*/
