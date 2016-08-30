define (['jquery', 'exporting'], function ($) {
	var chart = {};
	/**************************************************************************************************

					Public Functions

	**************************************************************************************************/
	var glb_mean 		= 0; 
	var glb_dev  		= 0;
	var glb_usedate 	= true;
	var enable_logging 	= false;
	var weekday = new Array(7);
	weekday[0]=  "Sunday";
	weekday[1] = "Monday";
	weekday[2] = "Tuesday";
	weekday[3] = "Wednesday";
	weekday[4] = "Thursday";
	weekday[5] = "Friday";
	weekday[6] = "Saturday";
	var points;
	
	/*
			function name: charts_createRanking
	*/
	
	chart.charts_createRanking = function (root, team_id, begin_date, end_date, html_id){
		var url_data		= root;//format_url(root, team_id, begin_date, end_date);
		var categories		= new Object();
		var serieses 		= [];
		var average_data	= [];
		var current_cat_val	= 0;
	
	
		function find_cat (value) {
			for(cat in categories)
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
			for(cat in categories){
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
	
	}//charts_createRanking
	
	
	/*
			function name: charts_createGaussian
	*/
	function create_gaussian(settings, points, html_id){
		var lowerbound 		= 0; //-5;
		var upperbound 		= 12; //5.1;
		var verticals		= [];
		var y_values 		= [];
		var dates 		= [];
		var chartData		= [];
		var index		= 0;
	
		glb_mean 		= settings[0].avg;
		glb_dev  		= settings[0].std;
	
		// extract data points
		for(i=0; i < points.length; i++){
			verticals.push(points[i].x);
			y_values.push(points[i].y);
			dates.push(points[i].date);
		}
		// Calculate data
		for (var i = lowerbound; i < upperbound; i += 0.1 ) {
			var dp = {
					category: i,
					value: NormalDensityZx(i, glb_mean, glb_dev)
				};
			if (verticals.indexOf( Math.round( i * 10 ) / 10 ) !== -1 ) {
				dp.vertical	= y_values[index]/100;
				dp.date		= dates[index];
				index		+= 1;
			}
			chartData.push( dp );
		}// for
	
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
	}// create_gaussian
	chart.charts_createGaussian = function (rooturl, user_id, begin_date, end_date, html_id){
		try{
			var data = {
						userId: user_id,
						beginDate: begin_date,
						endDate: end_date,
						gaussianSettings: true
						};
	
			$.ajax({type: "POST", url:  rooturl, data: data, success: function(setting_result){
				var settings = eval(setting_result);
				data.gaussianSettings = false;
				$.ajax({type: "POST", url:  rooturl, data: data, success: function(points_result){
					var points = eval(points_result);
					if (points.length != 0){
						console.log('data from  %s len: %d', rooturl , points.length);
						create_gaussian(settings, points, html_id);
					}
					else{
						var chart = getChart(html_id);
						if (chart != null){
							chart.clear();
							chart=null;
						}
						html_id = '#'+html_id;
						no_data_handler(html_id, 'There is no sleep data measured in the given time period. Please choose another period to analyse your personal sleep data.');
					}
	
					}});
			}});
		}
		catch(e){
			logerr('charts_createGaussian', e);
		}
	
	
	}// charts_createGaussian
	
	/*
			function name: charts_createHeatmap
	*/
	var glb_maxhour		= 12;
	var glb_hours 		= [];
	var glb_blue 		= 0;
	var glb_green 		= 0;
	var glb_maxvalue	= 0;
	
	
	function  create_heatmap(points, html_id, begin_date, end_date){
		var step		= 0.25;
	
		// for each hour find the relevant percents
		for(var h=0; h<=glb_maxhour; h+=step){
			var percents = []; // for each hour there is a colomn percent
			for(var j=0; j<=95; j+=5){
				percents[j/5] = {end: j + '%', value: 0};
			}
			for(var i=0; i<points.length; i++){
				var x = points[i].x;
				var y = points[i].y;
				if(x > h && x <= (h+step)){
					for(var j=0; j<=95; j+=5){
						if(y > j && y <= (j+5)){
							percents[j/5].end   = j + '%';
							percents[j/5].value +=1;
							if(percents[j/5].value > glb_maxvalue){
								glb_maxvalue = percents[j/5].value;
							}
	
						}//if
					}//for
	
				}
			}
			glb_hours[h] = percents;
		}
	
	
		var sourceData = [];
		for(var h = 0; h <= glb_maxhour; h+=step ) {
			var dataPoint = {hour: h}
			// generate value for each percent
			for (var p = 0; p < 20; p++ ) {
				dataPoint[ 'value' + p] = glb_hours[h][p].value;
			}
			sourceData.push(dataPoint);
		}
	
	
		// now let's populate the source data with the colors based on the value
		// as well as replace the original value with 1
		for ( i in sourceData ) {
			for (var p = 0; p < 20; p++) {
				if(sourceData[ i ][ 'value' + p ]==0){
					sourceData[ i ][ 'color' + p ] = 'rgb(255,255,255)';
				}
				else{
					sourceData[ i ][ 'color' + p ] = 'rgb(' + getColor(sourceData[ i ][ 'value' + p ]) + ',' +  glb_green + ',' +  glb_blue  + ')';
				}
				sourceData[ i ][ 'percent' + p ] = 1;
			}
		}
	
		// define graph objects for each percent
		var graphs = [];
		for (var p = 0; p < 20; p++) {
			graphs.push( {
				"balloonText": "<small>Sleep Data </small>" +
				"<table class=\"table\">" +
				"<tbody>" +
				"<tr><td style='text-align: left'>From </td><td style='text-align: right'><b>"+ begin_date +"</b></td></tr>" +
				"<tr><td style='text-align: left'>to </td><td style='text-align: right'><b>"+ end_date +"</b></td></tr>" +
				"<tr><td style='text-align: left'>you slept </td><td style='text-align: right'><b>[[value" + p + "]]</b> time(s)</td></tr>" +
				"<tr><td style='text-align: left'>with a percentage of </td><td style='text-align: right'><b>" + p*5 + "%-" + (p*5+5) + "%</b> of deep sleep</td></tr>" +
				"<tr><td style='text-align: left'>by </td><td style='text-align: right'><b>[[category]] h</b> of total sleeping hours</td></tr>" +
				"</tbody>" +
				"</table>",
				"fillAlphas": 1,
				"lineAlpha": 0.2,
				"lineColor": "rgb(105,105,105)",
				"type": "column",
				"colorField": "color" + p,
				"valueField": "percent" + p
			} );
		}
	
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
	}
	
	chart.charts_createHeatmap = function (rooturl, user_id, begin_date, end_date, html_id){
		var data = {
					userId: user_id,
					beginDate: begin_date,
					endDate: end_date,
					gaussianSettings: false
					};
	
		$.ajax({type: "POST", url: rooturl, data: data, success: function(result){
			var points = eval(result);
			if (points.length != 0){
				console.log('data from  %s len: %d', rooturl , points.length);
				create_heatmap(points, html_id, begin_date, end_date);
			}
			else{

				var chart = getChart(html_id);
				if (chart != null){
					chart.clear();
					chart=null;
				}
				html_id = '#'+html_id;
				no_data_handler(html_id, 'There is no sleep data measured in the given time period. Please choose another period to analyse your personal sleep data.');
			}
		 }});
	
	}//charts_createHeatmap
	
	
	/**************************************************************************************************
	
						Internal Functions
	
	**************************************************************************************************/
	
	/**************************************************************
				COMMON FUNCTIONS
	**************************************************************/
	/*
		function name: log
	*/
	function log(fun_name, msg){
		if(enable_logging)
			console.log('[%s]:%s', fun_name, msg);
	}
	
	function no_data_handler(html_id, text){
		var error_page = '<div class="error-content" align="center"> ' +
			'<h3><i class="fa fa-warning text-yellow"></i> No data available.</h3> ' +
			'<p>' +
			'Sorry! ' + text +
			'</p> ' +
			'</div><!-- /.error-content --> ';

		$(html_id).html(error_page);
	
	}
	
	function get_current_color(html_id, name){
		if ($(html_id).highcharts()!=null){
			var chart = $(html_id).highcharts();
			var serieses = chart.series;
			for (var i = 0; i<serieses.length; i++){
				if (serieses[i].options.type=='line'&& serieses[i].options.name==name){
					return serieses[i].options.color
				}
			}
		}
		return newRandomColor();
	
	}
	/*
		function name: logerr
	*/
	function logerr(fun_name, msg){
		console.error('ERROR [%s]:%s', fun_name, msg);
	}
	
	function getChart(id) {
		var allCharts = AmCharts.charts;
		for (var i = 0; i < allCharts.length; i++) {
			if (id == allCharts[i].div.id) {
				return allCharts[i];
			}
		}
	}
	/*
		function name: toDate
		function Desc: converts a string of format mm.dd.yyyy to a date object
	*/
	function toDate(str){
		var chunks = str.split('.');
		return new Date(chunks[2], chunks[1]-1, chunks[0]);
	}// toDate
	
	
	function secondsToMinutes(seconds){
		var totalMins = Math.round(seconds/60);
		var mins = totalMins%60;
		var hours = (totalMins-mins)/60;
		if (hours===0){
			return mins + ' minutes';
		}
		return hours + ' hours ' + mins + ' minutes';
	}//secondsToMinutes
	
	/*
		function name: format_url
	*/
	function format_url(root, user_id, begin_date, end_date){
		var url =  encodeURI(root);
		if(glb_usedate){
			var url = encodeURI(root  +   '/' + user_id + '/' + begin_date + '/' + end_date);
			log('format_url', url);
		}
		return url;
	}
	
	/*
		function name: request_data
	*/
	function request_data(url){
		var response 	= '';
		var request 	= new XMLHttpRequest();
		request.open('GET', url, false);
		request.send();
		response	= eval(request.responseText);
		log('request_data', url);
		log('request_data', JSON.stringify(response));
		return response;
	}
	/*
		function name: getColor
	*/
	function getColor(value){
		var normalized_val = Math.round(value * 255 / glb_maxvalue);
		log('getColor', value +' -> '+ normalized_val);
		return normalized_val;
	}
	
	/********************************************************************************************************
				Gaussian CHART
	
	********************************************************************************************************/
	/*
		function name: NormalDensityZx
	*/
	function NormalDensityZx( x, Mean, StdDev ) {
		var a = x - Mean;
		return Math.exp( -( a * a ) / ( 2 * StdDev * StdDev ) ) / ( Math.sqrt( 2 * Math.PI ) * StdDev );
	}
	/*
		function name:	NormalDensityZx
		Description:	Calculates Q(x), the right tail area under the Standard Normal Curve.
	*/
	function StandardNormalQx( x ) {
		if ( x === 0 ) // no approximation necessary for 0
		  return 0.50;
	
		var t1, t2, t3, t4, t5, qx;
		var negative = false;
		if ( x < 0 ) {
		  x = -x;
		  negative = true;
		}
		t1 = 1 / ( 1 + ( 0.2316419 * x ) );
		t2 = t1 * t1;
		t3 = t2 * t1;
		t4 = t3 * t1;
		t5 = t4 * t1;
		qx = NormalDensityZx( x, glb_mean, glb_dev) * ( ( 0.319381530 * t1 ) + ( -0.356563782 * t2 ) +
		  ( 1.781477937 * t3 ) + ( -1.821255978 * t4 ) + ( 1.330274429 * t5 ) );
		if ( negative == true )
		  qx = 1 - qx;
		return qx;
	}
	/*
		function name:	StandardNormalPx
		Description:	Calculates P(x), the left tail area under the Standard Normal Curve, which is 1 - Q(x).
	*/
	function StandardNormalPx( x ) {
		return 1 - StandardNormalQx( x );
	}
	/*
		function name:	StandardNormalAx
		Description:	Calculates A(x), the area under the Standard Normal Curve between +x and -x.
	*/
	function StandardNormalAx( x ) {
		return 1 - ( 2 * StandardNormalQx( Math.abs( x ) ) );
	}
	
	
	
	/********************************************************************************************************
				MULTI CHART
	
	********************************************************************************************************/
	
	function generateColor() {
		var letters = '0123456789ABCDEF'.split('');
		var color = '#';
		for (var i = 0; i < 6; i++ ) {
			color += letters[Math.floor(Math.random() * 16)];
		}
		return color;
	}
	
	function checkBoxSetVisible(chxId, dataId, containerId){
		var checked 	= $(chxId).is(':checked');
		var showData 	= $(dataId).is(':checked');
		var value 	= $(chxId).val();
		setTypeVisible(containerId, value, checked, showData);
	}
	
	
	function newRandomColor() {
			var color = [];
			color.push((Math.random() * 255).toFixed());
			color.push((Math.random() * 255).toFixed());
			color.push((Math.random() * 255).toFixed());
			//color.push((Math.random()).toFixed(2));
			color.push(1);
		var color = 'rgba(' + color.join(',') + ')';
			return color;
	}
	
	
	chart.charts_createMultiChart = function (rooturl, show_type1, show_data, user_id, begin_date, end_date, html_id, table_id, data_select_id, only_5mins){
		var data = {
					userId: user_id,
					type: "Cooldown",
					beginDate: begin_date,
					endDate: end_date
					};
		var serieses = [];
		$.ajax({type: "POST", url: rooturl, data: data, success: function(result){
				points = eval(result);
				if (points.length!=0){
					addSerieses(points, show_data, 'Type1', show_type1, data_select_id, serieses, 'circle', only_5mins);
					console.log('data from  %s len: %d', rooturl, points.length);
					// the following commented lines are for getting type2 uncomment to get the results
					//$.ajax({url: type2_url, success: function(result_type2){
					//    	var points2 = eval(result_type2);
					//	console.log('data from  %s len: %d', type2_url, points2.length);
					//	addSerieses(points2, show_data, 'Type2', true, data_select_id, serieses,  'triangle');
					draw_chart(serieses, html_id, only_5mins);
					fadeInHtmlTable(points, table_id);
					//}});
				}
				else{
					if ($(html_id).highcharts()!=null){
						$(html_id).highcharts().destroy();
					}
					no_data_handler(html_id, 'There is no heartrate data measured in the given time period. Please choose another period to analyse your personal heartrate data.');
					no_data_handler(table_id, 'There is no heartrate data measured in the given time period. Please choose another period to analyse your personal heartrate data.');
				}
	
			}});
	
	}//charts_createMultiChart
	
	chart.charts_switchMultiChart = function (show_type1, show_data, html_id, data_select_id, only_5mins){
		if (points.length != 0){
			var serieses = [];
			addSerieses(points, show_data, 'Type1', show_type1, data_select_id, serieses, 'circle', only_5mins, html_id);
			draw_chart(serieses, html_id, only_5mins);
		}
	
	
	}//charts_switchMultiChart
	
	
	function draw_chart(serieses, html_id, only_5mins){
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
						 s = '<small> Heartrate after ' + secondsToMinutes(this.x) + '</small>' +
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
	}
	
	
	function addSerieses(points, show_data,  type, visible, data_select_id, serieses,  point_symbol, only_5mins, html_id){
		var max_x 	= only_5mins? 300: 12000; // 12K
		var step	= only_5mins? 1: 10;
	
		for(var i=0; i<points.length; i++){
			try{
	
				var a 		= points[i].a;
				var t 		= points[i].t;
				var c 		= points[i].c;
				if(!(a==null)&&!(t==null)&&!(c==null)){
					var dataPoints	= points[i].data_points;
					var date	= points[i].date;
					var tempDate = date.split(".");
					var dateObj = new Date (tempDate[2],tempDate[1]-1,tempDate[0],0,0,0);
	
					var line_data 		= getLineData(a, t, c, max_x, step);
					var scatter_data 	= getScatterData(dataPoints,  only_5mins);
	
					var scatter_name	= weekday[dateObj.getDay()] + ' ' + date;
					var line_name		= weekday[dateObj.getDay()] + ' ' + date;
					var legend		= 'maximum: ' + line_data[0][1] + ', minimum: ' + line_data[line_data.length-1][1] + ', current: ';
					if (html_id){
						var color = get_current_color(html_id, line_name);
					}
					else{
						var color		=  newRandomColor();
					}
	
					var id 			= type + '_' + i;
	
					var lineSeries 		= createLineSeries	(color, type, visible, data_select_id, id, line_name, line_data, legend);
					var scatterSeries 	= createScatterSeries	(scatter_name, color, type, visible, id, scatter_data, point_symbol, show_data);
	
					serieses.push(lineSeries);
					serieses.push(scatterSeries);
				}
	
	
			}catch(e){
				console.error(e);
			}// catch
	
		}//for
	}
	function getLineData(a, t, c, max_x, step){
		var series_data	= [];
		var start_HR = 180;
		for (var x = 0; x <= max_x; x+= step) {
			var y = (start_HR-c)*Math.exp(-(x-t)/a) + c;
			series_data.push([x, y]);
		}
		return series_data;
	}
	function getScatterData(points, only_5mins){
		var series_data = [];
		for(var i=0; i< points.length; i++){
			if(only_5mins){
				if(points[i].x <= 300){
					series_data.push([points[i].x, points[i].y]);
				}
			}else{
				if (points[i].x <= 12000){
					series_data.push([points[i].x, points[i].y]);
				}
			}
	
		}
		return series_data;
	}
	function createScatterSeries(name, color, type, visible, linkedId, data, point_symbol, show_data){
		var series = new Object();
		series.type 		= 'scatter';
		series.grp		= String(type);
		if (visible&&show_data){
			series.selected		= true;
			series.visible		= true;
		}
		else {
			series.selected		= false;
			series.visible		= false;
		}
	
		series.linkedTo 	= linkedId;
		series.name		= name;
		series.data 		= data;
		series.showInLegend 	= false;
		series.color		= color;
		series.marker		= {radius: 2,  symbol: point_symbol};
	
		return series;
	
	}
	function createLineSeries(color, type, visible, data_select_id, id, name, data, legend){
	
		//tooltip.valuePrefix = legend;
		var series 			= new Object();
		series.id			= id;
		series.type			= 'line';
		series.grp			= String(type);
		series.selected 		= visible;
		series.visible	 		= visible;
		series.name			= name;
		series.data			= data;
		series.color			= color;
		series.events 			= new Object();
		series.events.legendItemClick 	= function (event) {
							this.options.selected = !this.visible;
	
							this.linkedSeries[0].options.selected = !this.visible;
	
	
							this.setVisible(!this.visible, false);
	
							this.linkedSeries[0].setVisible($(data_select_id).is(':checked') && this.visible, false);
	
	
							this.chart.redraw();
							return false;
		};
	
		return series;
	}
	
	
	chart.setTypeVisible = function (htmlId, type, visible, showdata){
	
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
	
	}
	
	chart.setScatterVisible = function (htmlId, visible){
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
	
	}
	
	function fadeInHtmlTable (points, table_div){
		if(table_div!=null){
			var content = "";
			content+= "<thead class='tablethead'>" +
				"<tr class='tabletr'>" +
				"<th class='tableth'>Date</th>" +
				"<th class='tableth'>a</th>" +
				"<th class='tableth'>T</th>" +
				"<th class='tableth'>c</th>" +
				"</tr>" +
				"</thead>" +
				"<tbody class='tabletbody'>";
			if(points.length != 0){
				try{
					for (var i = 0; i<points.length; i++){
						if(!(points[i].a==null)&&!(points[i].t==null)&&!(points[i].c==null)){
							content+="<tr class='tabletr'>";
							content+="<td class=\"tabletd filterable-cell\">"+points[i].date+"</td>";
							content+="<td  class=\"tabletd filterable-cell\">"+Math.round(points[i].a*100)/100+"</td>";
							content+="<td  class=\"tabletd filterable-cell\">"+Math.round(points[i].t*100)/100+"</td>";
							content+="<td  class=\"tabletd filterable-cell\">"+Math.round(points[i].c*100)/100+"</td>";
							content+="</tr>";
						}
					}
				}
				catch(e){
					console.error(e);
				}// catch
	
			}
			content+="</tbody>";
			$(table_div).html(content);
			//document.getElementById(table_div).innerHTML = content;
		}
	
	}
	
	/********************************************************************************************************
	
	 Correlations
	
	 ********************************************************************************************************/
	/*
	 /*
	 function name: charts_createLinearCurve
	 */
	
	chart.charts_getCorrelations = function (rooturl, show_data, user_id, html_id, title, xLabel, yLabel, nextDay){
		var data = {
					userId: user_id,
					xAxis: xLabel,
					yAxis: yLabel,
					nextDay: nextDay
					};
		var series = [];
		var formatter = null;
		$.ajax({type: "POST", url: rooturl, data: data, success: function(result){
			var points1 = JSON.parse(result);
			if (points1!=null){
				console.log('data from  %s', rooturl);
				series = get_linear_series(points1, true, 'circle', title);
	
				if (points1.xlabel=="Sleep start"){
					formatter = function(){
						var format = this.value/(60*60);
						var hours = Math.round(format);
						var mins = format-hours;
						if (mins<0){
							--hours;
							mins = format-hours;
						}
						mins = Math.round(mins*60);
						return hours + ':' + mins + 'h';
					}
				}
				if (points1.xlabel=="Day of week"){
					formatter = function(){
						if (this.value-Math.round(this.value)==0){
							return weekday[Math.round(this.value)];
						}
					}
				}
				draw_linearChart(title, points1.xlabel, points1.ylabel, html_id, series, formatter);
			}
			else{
				if($(html_id).highcharts()!=null){
					$(html_id).highcharts().destroy();
				}
				no_data_handler(html_id, 'There is no correlation data available from ' + xLabel + ' to ' + yLabel + '. Please choose other labels.');
			}
	
	
			return;
	
		}});
	
	}
	
	function get_linear_series(data, visible, point_symbol, title){
		var point1 = [];
		point1.push(data.x0);
		point1.push(data.y0);
		var point2 = [];
		point2.push(data.x1);
		point2.push(data.y1);
		var color		=  'rgba(0, 0, 0, 1)';
		var id 			= title;
		var data_points = data.data;
	
	
		var series = linearSeriesFactory(point1, point2, color, data_points, point_symbol, id, data.xlabel, data.ylabel);
	
		return series;
		//TODO create line and scatter data an push it to series variable
	}
	
	function linearSeriesFactory(point1, point2, color, data_points, point_symbol, id, xAxis, yAxis){
		var step = (point2[0]-point1[0])/200;
		var lineData = getTwoDotLinePoints(point1, point2, step);
		var lineColor = 'rgba(0, 85, 213, 1)';
		var scatterColor = 'rgba(228, 6, 6, 1)';
		var scatter = createScatterSeries("scatter " + id, scatterColor, "scatter", true, id, data_points, point_symbol, true);
		var line = createlinearLineSeries(lineColor, "line", id, "line " + id, lineData, xAxis, yAxis);
		var serieses = [];
		serieses.push(line);
		serieses.push(scatter);
		return serieses;
	
	}
	
	function getTwoDotLinePoints(point1, point2, step){
		var m = (point2[1]-point1[1])/(point2[0]-point1[0]);
		var n = point1[1] - m*point1[0];
		var points = [];
		for (var x = point1[0]; x <= point2[0]; x+= step) {
			var y =m*x+n;
			points.push([x, y]);
		}
		points.push(point2);
		return points;
	}
	
	function createlinearLineSeries(color, type, id, name, data, xAxis, yAxis){
		var series 			= new Object();
		series.id			= id;
		series.type			= type;
		series.grp			= String(type);
		series.visible		= true;
		series.showInLegend = false;
		series.name			= name;
		series.data			= data;
		series.color		= color;
	
	
		return series;
	}
	
	function draw_linearChart(title, xAxis, yAxis, html_id, serieses, formatter){
		$(html_id).highcharts({
			title: {
				text: title
			},
			xAxis: {
				title: {
					text: xAxis
				},
				labels: {
					formatter: formatter
				}
			},
			yAxis: {
				title: {
					text: yAxis
				}
			},
			tooltip: {
				useHTML: true,
				formatter: function () {
					var s=s = '<p>'+ xAxis + ': ' + Math.round(this.x*100)/100 + '</p>' +
						'<table>'
					if(this.points != null){
						$.each(this.points, function () {
							s += '<tr>' +
								'<td style="color: '+this.series.color+'">' + yAxis+ ': </td>' +
								'<td style="text-align: right"><b>' + this.y + '</b></td>' +
								'</tr>';
						});
					}
					if (this.point != null){
						s += '<tr>' +
							'<td style="color: '+this.point.color+'">' + yAxis + ': </td>' +
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
			series: serieses
		});
	}
	
	return chart;

});

