
/**
 *    Common functions to use with AMcharts
 *
 **/


// Daily date-value pairs - simple
function loadJSONData(url)
{
    var request = new XMLHttpRequest();
    

    request.open('GET', url, false);
    request.send();
    data = eval(request.responseText);
    /*if (Array.isArray(data) === true)    {
     data = toObject(data)
    }*/
    return data;

};


// Test js function for filling html from example data source end
function fillSingleDateDataExample(id,data) {
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
function fillDoubleOverlay(id, dataset,title, units, xValueField, yValueField1, yValueField2,yTitle1, yTitle2,  yText1, yText2 )
{
 
    var chart = AmCharts.makeChart(id, {
        "theme": "light",
        "type": "serial",
        "dataProvider": dataset ,
        "valueAxes": [{
            "unit": units,
            "position": "left",
            "title": title,
        }],
        "startDuration": 1,
        "graphs": [{
            "balloonText":  yText1         /* "GDP grow in [[category]] (2004): <b>[[value]]</b>"*/,
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
    chart.validateData()

}


function fillDoubleLineChart(id, dataset, categoryField, yValueField1, yValueField2, title, graphOneTitle, graphTwoTitle, axisTitle, dataDateFormat, minPeriod)
{

   
    var chart = AmCharts.makeChart(id,
                    {
                        "type": "serial",
                        "categoryField": categoryField,
                        "dataDateFormat":dataDateFormat ,
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
                chart.validateData()
}

function fillGaugeChart(id)
{
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
            "bottomText": "0 Metabolic Rate",
            "bottomTextYOffset": -20,
            "endValue": 100
        }],
        "arrows": [{}],
        "export": {
            "enabled": true
        }
    });
    gaugeChart.validateData()

   

}
function toObject(arr) {
  var rv = {};
  for (var i = 0; i < arr.length; ++i)
    rv[i] = arr[i];
  return rv;
}

