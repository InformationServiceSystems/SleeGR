/**
 * Created by Mirco on 07.09.2016.
 */

define(['jquery', 'common.functions', 'amcharts.serial', 'amcharts.themeLight'], function ($, utils, AmCharts) {
    
    var amFunctions = new Object();
    
    amFunctions.getChart = function (id) {
		var allCharts = AmCharts.charts;
		for (var i = 0; i < allCharts.length; i++) {
			if (id == allCharts[i].div.id) {
				return allCharts[i];
			}
		}
	}
	
	/*
		function name: getColor
	*/
	amFunctions.amCharts_getColor = function (value, glb_maxvalue){
		var normalized_val = Math.round(value * 255 / glb_maxvalue);
		return normalized_val;
	}

	amFunctions.getGaussianDataPoints = function (settings, points, glb_mean, glb_dev) {
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
					value: utils.NormalDensityZx(i, glb_mean, glb_dev)
				};
			if (verticals.indexOf( Math.round( i * 10 ) / 10 ) !== -1 ) {
				dp.vertical	= y_values[index]/100;
				dp.date		= dates[index];
				index		+= 1;
			}
			chartData.push( dp );
		}// for

		return chartData;
	}
	
	amFunctions.getHeatmapDataPoints = function (points, glb_maxhour, glb_maxvalue, glb_hours, glb_green, glb_blue) {
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
					sourceData[ i ][ 'color' + p ] = 'rgb(' + amFunctions.amCharts_getColor(sourceData[ i ][ 'value' + p ], glb_maxvalue) + ',' +  glb_green + ',' +  glb_blue  + ')';
				}
				sourceData[ i ][ 'percent' + p ] = 1;
			}
		}
		return sourceData;
	}

	amFunctions.getHeatmapGraphObjects = function(begin_date, end_date){
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
		return graphs;
	}
	
	amFunctions.clearAmChart = function (html_id, error_text) {
		var gaussian_chart = amFunctions.getChart(html_id);
		if (gaussian_chart != null){
			gaussian_chart.clear();
			gaussian_chart=null;
		}
		html_id = '#'+html_id;
		var no_data = utils.getNoDataDiv(error_text);
		$(html_id).html(no_data);
	}
    return amFunctions;
});
