/**************************************************************************************************

					Public Functions

**************************************************************************************************/
var glb_mean = 0; 
var glb_dev  = 0;
/*
		function name: charts_createGaussian
*/
function charts_createGaussian(rooturl_points, rooturl_settings, user_id, begin_date, end_date, html_id){
	log('charts_drawGaussian', 'start'); 
	var url_points 		= format_url(rooturl_points, user_id, begin_date, end_date);
	var url_settings 	= format_url(rooturl_settings, user_id, begin_date, end_date);
	var points		= request_data(url_points);
	var settings		= request_data(url_settings);
	var lowerbound 		= -5;
	var upperbound 		= 5.1;
	var verticals		= [];
	var y_values 		= [];
	var dates 		= [];

	glb_mean 		= settings[0].avg;
	glb_dev  		= settings[0].std;
	// extract data points
	for(i=0; i < points.length; i++){
		verticals.push(points[i].x);
		y_values.push(points[i].y);
		dates.push(points[i].date);
	}

	// Calculate data
	var 	chartData = [];
	var	index = 0;
	for (var i = lowerbound; i < upperbound; i += 0.1 ) {
		var dp = {
		    category: i,
		    value: NormalDensityZx(i, glb_mean, glb_dev)
		};
		if (verticals.indexOf( Math.round( i * 10 ) / 10 ) !== -1 ) {
			dp.vertical	= y_values[index];
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
	   		"gridAlpha": 0.05,
			"startOnAxis": true,
			"tickLength": 5,
			"labelFunction": function( label, item ) {
	      			return '' + Math.round( item.dataContext.category * 10 ) / 10;
	    		}
	 	}

	} );

}// charts_createGaussian

/*
		function name: charts_createHeatmap
*/
var glb_maxhour		= 12;
var glb_hours 		= [];
var glb_blue 		= 70;
var glb_green 		= 45;
var glb_maxvalue	= 0;
function  charts_createHeatmap(rooturl_points, user_id, begin_date, end_date, html_id){
	log('charts_createHeatmap', 'start'); 
	var url_points 		= format_url(rooturl_points, user_id, begin_date, end_date);
	var points		= request_data(url_points);

	// for each hour find the relevant percents
	for(var h=0; h<=glb_maxhour; h++){
		var percents = []; // for each hour there is a colomn percent
		for(var j=0; j<=95; j+=5){
			percents[j/5] = {end: j + '%', value: 0};
		}
		for(var i=0; i<points.length; i++){
			var x = points[i].x;
			var y = points[i].y;
			if(x > h && x <= (h+1)){
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
	for(var h = 0; h <= glb_maxhour; h++ ) {  
		var dataPoint = {
			hour: h
		}
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
	    sourceData[ i ][ 'color' + p ] = 'rgb(' + getColor(sourceData[ i ][ 'value' + p ]) + ',' +  glb_green + ',' +  glb_blue  + ')';
	    sourceData[ i ][ 'percent' + p ] = 1;
	  }
	}
	// define graph objects for each percent
	var graphs = [];
	for (var p = 0; p < 20; p++) {
		graphs.push( {
			"balloonText": "Original value: [[value" + p + "]]",
			"fillAlphas": 1,
			"lineAlpha": 0,
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
			"baseValue": 0,
			"stackType": "regular",
			"axisAlpha": 0,
			"gridAlpha": 0,
			"maximum": 20,
			"labelFunction":function( value, valueText, valueAxis) {
		    			return value * 5 + '%';
				} 
		} ],
		"graphs": graphs,
		"columnWidth": 1,
		"categoryField": "hour",
		"categoryAxis": {
			"gridPosition": "start",
			"axisAlpha": 0,
			"gridAlpha": 0,
			"position": "left"
	  	}
	} );

	
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
	console.log('[%s]:%s', fun_name, msg);
}

/*
	function name: format_url
*/
function format_url(root, user_id, begin_date, end_date){
	var url = encodeURI(root  + '/' + user_id + '/' + begin_date + '/' + end_date);
	log('format_url', url);
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
