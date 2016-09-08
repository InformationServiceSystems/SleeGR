define (['jquery', 'common.functions', 'amcharts.functions', 'highcharts.functions','amcharts.serial', 'highcharts', 'highcharts.exporting', 'amcharts.themeLight'], function ($, utils, amFunctions, highchartFunctions,AmCharts) {

	"use strict";
	function Chart(mean, dev, maxhour, hours, blue, green, maxvalue){
		this.glb_mean 		= mean;
		this.glb_dev  		= dev;
		this.glb_maxhour	= maxhour;
		this.glb_hours 		= hours;
		this.glb_blue 		= blue;
		this.glb_green 		= green;
		this.glb_maxvalue	= maxvalue;

	};

	Chart.prototype = {
		charts_createRanking: function (root, team_id, begin_date, end_date, html_id){
			var url_data		= root;//format_url(root, team_id, begin_date, end_date);
			var categories		= new Object();
			var serieses 		= [];
			var average_data	= [];
			var current_cat_val	= 0;


			function find_cat (value) {
				for(var cat in categories)
					if(categories[cat].id == value){
						return cat;
					}
					return value;
			}

			$.ajax({url:  url_data, success: function(result){
				var points = eval(result);
				console.log('data from  %s len: %d',  url_data, points.length);
				for(var i=0; i<points.length; i++){
								var series_id 	= points[i]['athlete_id'];
								var series 	= new Object();
								series.name	= points[i]['last_name'] + ',' + points[i]['name'];
								series.data	= [];

								for (var property in points[i]) {
									if(property.startsWith('score')){
										if(!categories.hasOwnProperty(property)){
											categories[property]	 	= new Object();
											categories[property].id  	= current_cat_val++;
											categories[property].sum 	= 0;
											categories[property].count 	= 0;

										}
										series.data.push([categories[property].id , points[i][property]]);
										categories[property].sum 	+= points[i][property];
										categories[property].count 	+= 1;
									}
								}
								series.type = 'column';
								serieses.push(series);
				}
				for(var cat in categories){
					average_data.push([categories[cat].id , categories[cat].sum/categories[cat].count]);
				}
				console.log('update');
							var series 	= new Object();
							series.name	= 'average';
							series.data 	= average_data;
							series.type 	= 'line';
							series.color	= '#FF0000';
							series.lineWidth = 5;
							serieses.push(series);

							$(html_id).highcharts({
									//chart: { type: 'column'	},
									title: { text: 'Compare Scores'},
									yAxis: { min: 0, title: { text: 'score'} },
									xAxis: {
									   labels: {
											formatter:function () {
												return find_cat (this.value)
											}
										}

									},
									tooltip: {
										headerFormat: '',
										/*formatter: function () {
											var s = '<b>' + find_cat(this.x) + '</b>';
											$.each(this.points, function () {
												s += '<br/>' + this.series.name + ': ' + this.y;
											});
											return s;
											},*/
										shared: false
									},
									plotOptions: {column: { pointPadding: 0, borderWidth: 0, stacking: false }},
										series: serieses});
			}});

		},
		create_heatmap: function  (points, html_id, begin_date, end_date){

			var sourceData = amFunctions.getHeatmapDataPoints(points, this.glb_maxhour, this.glb_maxvalue, this.glb_hours, this.glb_green, this.glb_blue);

			var graphs = amFunctions.getHeatmapGraphObjects(begin_date, end_date);
			//
			// create the heatmap chart!
			var chart = AmCharts.makeChart(html_id,{
					"type": "serial",
					"dataProvider": sourceData,
					"valueAxes": [ {
						"title": "Deep Sleep (in %)",
						"baseValue": 0,
						"stackType": "regular",
						"axisAlpha": 0.3,
						"gridAlpha": 1,
						"gridColor": "rgb(105,105,105)",
						"maximum": 20,
						"labelFunction":function( value, valueText, valueAxis) {
									return value * 5 + '%';
								}
					} ],
					"graphs": graphs,
					"columnWidth": 1,
					"categoryField": "hour",
					"categoryAxis": {
						"title": "Sleeping hours",
						"gridPosition": "start",
						"axisAlpha": 0,
						"gridAlpha": 1,
						"gridColor": "rgb(105,105,105)",
						"position": "left"
						},
				} );
		},
		draw_multiChart: function (points, show_data, grp_type, show_type1, data_select_id, point_symbol,html_id, only_5mins){
			var serieses = highchartFunctions.getMultichartSeries(points, show_data, grp_type, show_type1, data_select_id, 'circle', only_5mins, html_id);

			 $(html_id).highcharts({
				title: {
					text: 'Heartrate Cooldown after Workout'
				},
				xAxis: {
					title: {
						text: 'time'
					},
					labels: {
						formatter: function(){
							if(only_5mins)
								return this.value;

							var hours = this.value/(60*60);
							return hours.toFixed(2) + 'h';
						}
					}
					//tickInterval: 1.5
				},
				 yAxis: {
					 title:{
						 text: 'heartrate (in bpm)'
					 }
				 },
				 tooltip: {
					 formatter: function () {
						 var s='';
						 if (!only_5mins){
							 s = '<small> Heartrate after ' + utils.secondsToMinutes(this.x) + '</small>' +
								 '<table>';
						 }
						 else{
							 s = '<small> Heartrate after ' +this.x+ ' seconds</small>' +
								 '<table>';
						 }

						 if(this.points != null){
							 $.each(this.points, function () {
								 s += '<tr>' +
									 '<td style="color: '+this.series.color+'">' + this.series.name + ': </td>' +
									 '<td style="text-align: right"><b>' + Math.round(this.y*100)/100 + 'bpm </b></td>' +
									 '</tr>';
							 });
						 }
						 if (this.point != null){
							 s += '<tr>' +
								 '<td style="color: '+this.point.color+'">' + this.point.series.name + ': </td>' +
								 '<td style="text-align: right"><b>' + Math.round(this.y*100)/100 + 'bpm </b></td>' +
								 '</tr>';
						 }

						 s += '</table>';

						 return s;
					 },
					 shared: true,
					 useHTML: true,
					 valueDecimals: 2
				 },
				 plotOptions: {
					 line: {
						 marker: {
							 enabled: false
						 }
					 }
				 },
				 series: serieses
			 });
		},
		setTypeVisible: function (htmlId, type, visible, showdata){
			if ($(htmlId).highcharts()!=null){
				var chart = $(htmlId).highcharts();
				var series = chart.series;
				for(var i=0; i<series.length; i++){
					if(series[i].options.grp == type){
						if(series[i].options.type == 'scatter')
							series[i].setVisible(showdata && visible, false);
						else
							series[i].setVisible(visible, false);

					}// if group matches
				}// for
				chart.redraw();
			}

		},
		setScatterVisible: function (htmlId, visible){
			if ($(htmlId).highcharts()!=null){
				var chart = $(htmlId).highcharts();
				var series = chart.series;
				for(var i=0; i<series.length; i++){
					if(series[i].options.type == 'scatter'){
						var linkedto = chart.get(series[i].options.linkedTo);
						series[i].setVisible((visible && linkedto.visible), false);
					}// if group matches
				}// for
				chart.redraw();
			}

		},
		draw_linearChart: function (data_points, title, xLabel, yLabel, html_id){

			var series = highchartFunctions.getCorellSeries(data_points.x0, data_points.y0, data_points.x1, data_points.y1, data_points.data, 'circle', title);

			var formatter = highchartFunctions.highcharts_getFormatter(xLabel);

			$(html_id).highcharts({
				title: {
					text: title
				},
				xAxis: {
					title: {
						text: xLabel
					},
					labels: {
						formatter: formatter
					}
				},
				yAxis: {
					title: {
						text: yLabel
					}
				},
				tooltip: {
					useHTML: true,
					formatter: function () {
						var s=s = '<p>'+ xLabel + ': ' + Math.round(this.x*100)/100 + '</p>' +
							'<table>'
						if(this.points != null){
							$.each(this.points, function () {
								s += '<tr>' +
									'<td style="color: '+this.series.color+'">' + yLabel+ ': </td>' +
									'<td style="text-align: right"><b>' + this.y + '</b></td>' +
									'</tr>';
							});
						}
						if (this.point != null){
							s += '<tr>' +
								'<td style="color: '+this.point.color+'">' + yLabel + ': </td>' +
								'<td style="text-align: right"><b>' + Math.round(this.y*100)/100 + '</b></td>' +
								'</tr>';
						}

						s += '</table>';

						return s;
					}
				},
				plotOptions: {
					line: {
						marker: {
							enabled: false
						}
					}
				},
				series: series
			});
		},
		create_gaussian: function (settings, points, html_id){
			var chartData = amFunctions.getGaussianDataPoints(settings, points, this.glb_mean, this.glb_dev);
			//
			// create the Gaussian chart!
			var chart = AmCharts.makeChart(html_id,{
				"type": "serial",
				"theme": "light",
				"dataProvider": chartData,
				"precision": 2,
				"valueAxes": [ {
					"title": "Deep Sleep (in %)",
					"gridAlpha": 0.2,
					"dashLength": 0
				} ],
				"startDuration": 1,
				"graphs": [ {
					"balloonText": "[[date]]",
						"lineThickness": 3,
						"valueField": "value"
				  }, {
					"balloonText": "",
					"fillAlphas": 1,
					"type": "column",
					 "valueField": "vertical",
					"fixedColumnWidth": 2,
					"labelText": "[[value]]",
					"labelOffset": 20
				  } ],
				  "chartCursor": {
					"categoryBalloonEnabled": false,
					 "cursorAlpha": 0,
					"zoomable": false
				  },
				"categoryField": "category",
				"categoryAxis": {
					"title": "Sleeping Hours",
					"gridAlpha": 0.05,
					"startOnAxis": true,
					"tickLength": 5,
					"labelFunction": function( label, item ) {
							return '' + Math.round( item.dataContext.category * 10 ) / 10;
						}
				 }

			} );
		},
		clearHighchart: function (html_id, error_text) {
			highchartFunctions.clearHighchart(html_id, error_text);
		},
		clearAmChart: function (html_id, error_text) {
			amFunctions.clearAmChart(html_id, error_text);
		}
	};

	return Chart;

});

