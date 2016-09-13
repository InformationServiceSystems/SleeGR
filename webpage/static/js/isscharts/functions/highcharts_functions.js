/**
 * Created by Mirco on 07.09.2016.
 */

define(['jquery', 'common.functions', 'highcharts'], function ($, utils) {
	
   
    var highchartFunctions = new Object();
    
    highchartFunctions.highcharts_newRandomColor = function () {
        var color = [];
        color.push((Math.random() * 255).toFixed());
        color.push((Math.random() * 255).toFixed());
        color.push((Math.random() * 255).toFixed());
			
        //opacity fixed to 100%
        color.push(1);
		color = 'rgba(' + color.join(',') + ')';
        return color;
	}
    
	highchartFunctions.highcharts_getColor = function (html_id, name){
		if ($(html_id).highcharts()!=null){
			var chart = $(html_id).highcharts();
			var serieses = chart.series;
			for (var i = 0; i<serieses.length; i++){
				if (serieses[i].options.type=='line'&& serieses[i].options.name==name){
					return serieses[i].options.color;
				}
			}
		}
		return highchartFunctions.highcharts_newRandomColor();
	
	}

	highchartFunctions.highcharts_getFormatter = function(xlabel){
		var formatter = null;
		if (xlabel=="Sleep start"){
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
		if (xlabel=="Day of week"){
			formatter = function(){
				if (this.value-Math.round(this.value)==0){
					return utils.getWeekday(Math.round(this.value));
				}
			}
		}

		return formatter;
	}

	highchartFunctions.createLineSeries = function (id, grp_type, visible, name, color, data,showInLegend, data_select_id, legendClickFunction){

		//tooltip.valuePrefix = legend;
		var series 			= new Object();
		series.id			= id;
		series.type			= 'line';
		series.grp			= String(grp_type);
		series.visible	 	= visible;
		series.showInLegend	= showInLegend;
		series.name			= name;
		series.data			= data;
		series.color		= color;

		if (showInLegend){series.selected 	= visible;
			series.events 		= new Object();
			series.events.legendItemClick 	= legendClickFunction;
		}

		return series;
	}
    
	highchartFunctions.createScatterSeries = function (name, color, type, visible, linkedId, data, point_symbol, show_data){
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
    
	highchartFunctions.getScatterData = function (points, only_5mins){
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
	
	highchartFunctions.getTwoDotLinePoints = function (x1, y1, x2, y2, step){
		var m = (y2-y1)/(x2-x1);
		var n = y1 - m*x1;
		var points = [];
		for (var x = x1; x <= x2; x+= step) {
			var y =m*x+n;
			points.push([x, y]);
		}
		points.push([x2, y2]);
		return points;

	}

	highchartFunctions.getExponentialPoints = function(a, t , c, step, max_x){
		var series_data	= [];
		var start_HR = 180;
		for (var x = 0; x <= max_x; x+= step) {
			var y = (start_HR-c)*Math.exp(-(x-t)/a) + c;
			series_data.push([x, y]);
		}
		return series_data;
	}
	
	highchartFunctions.getCorellSeries = function (x1, y1, x2, y2, data_points, point_symbol, id){
		var step = (x2-x1)/200;
		var lineData = highchartFunctions.getTwoDotLinePoints(x1, y1, x2, y2, step);
		var lineColor = 'rgba(0, 85, 213, 1)';
		var scatterColor = 'rgba(228, 6, 6, 1)';
		var scatter = highchartFunctions.createScatterSeries("scatter " + id, scatterColor, "scatter", true, id, data_points, point_symbol, true);
		var line = highchartFunctions.createLineSeries(id, null, true, 'line ' + id, lineColor, lineData, false);
		var serieses = [];
		serieses.push(line);
		serieses.push(scatter);
		return serieses;
	
	}
	
	highchartFunctions.getMultichartSeries = function (points, show_data,  type, visible, data_select_id,  point_symbol, only_5mins, html_id){
		var serieses = [];
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
					var dateObj = utils.toDate(date);
					
					var line_data 		= highchartFunctions.getExponentialPoints(a, t, c, step, max_x);
					var scatter_data 	= highchartFunctions.getScatterData(dataPoints,  only_5mins);
	
					var scatter_name	= utils.getWeekday(dateObj.getDay()) + ' ' + date;
					var line_name		= utils.getWeekday(dateObj.getDay()) + ' ' + date;
					var legend		= 'maximum: ' + line_data[0][1] + ', minimum: ' + line_data[line_data.length-1][1] + ', current: ';
					
					var color = highchartFunctions.highcharts_getColor(html_id, line_name);
					
					var id 			= type + '_' + i;

					var legendClickFunction = function (event) {
						this.options.selected = !this.visible;

						this.linkedSeries[0].options.selected = !this.visible;


						this.setVisible(!this.visible, false);

						this.linkedSeries[0].setVisible($(data_select_id).is(':checked') && this.visible, false);


						this.chart.redraw();
						return false;
					};

					var lineSeries 		= highchartFunctions.createLineSeries(id, type, visible, line_name, color, line_data, true, data_select_id, legendClickFunction);

					var scatterSeries 	= highchartFunctions.createScatterSeries	(scatter_name, color, type, visible, id, scatter_data, point_symbol, show_data);
	
					serieses.push(lineSeries);
					serieses.push(scatterSeries);
				}

	
	
			}catch(e){
				console.error(e);
			}// catch
	
		}//for
		return serieses;
	}
	
	highchartFunctions.clearHighchart = function (html_id, error_text) {
		if ($(html_id).highcharts()!=null){
						$(html_id).highcharts().destroy();
		}
		var no_data = utils.getNoDataDiv(error_text);
		$(html_id).html(no_data);
	}

	
    return highchartFunctions;
});
