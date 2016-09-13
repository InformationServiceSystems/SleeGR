/**
 * Created by Mirco on 07.09.2016.
 */

define(['jquery'], function ($) {
	
	var weekday = new Array(7);
	weekday[0]=  "Sunday";
	weekday[1] = "Monday";
	weekday[2] = "Tuesday";
	weekday[3] = "Wednesday";
	weekday[4] = "Thursday";
	weekday[5] = "Friday";
	weekday[6] = "Saturday";
    
    var utils = new Object();
    
    /*
		function name: log
	*/
	utils.log = function (fun_name, msg){
		console.log('[%s]:%s', fun_name, msg);
	}
    
    /*
		function name: logerr
	*/
	utils.logerr = function (fun_name, msg){
		console.error('ERROR [%s]:%s', fun_name, msg);
	}
    
    
    /*
		function name: toDate
		function Desc: converts a string of format mm.dd.yyyy to a date object
	*/
    utils.toDate = function (str){
		var chunks = str.split('.');
		return new Date(chunks[2], chunks[1]-1, chunks[0]);
	}// toDate
	
	utils.getWeekday = function (day){
		return weekday[day];
	}

    utils.secondsToMinutes = function (seconds){
		var totalMins = Math.round(seconds/60);
		var mins = totalMins%60;
		var hours = (totalMins-mins)/60;
		if (hours===0){
			return mins + ' minutes';
		}
		return hours + ' hours ' + mins + ' minutes';
	}//secondsToMinutes

	utils.contains = function (a, obj) {
        for (var i = 0; i < a.length; i++) {
            if (a[i] == obj) {
                return true;
            }
        }
        return false;
    }

    utils.getNoDataDiv = function (text){
		var error_page = '<div class="error-content" align="center"> ' +
			'<h3><i class="fa fa-warning text-yellow"></i> No data available.</h3> ' +
			'<p>' +
			'Sorry! ' + text +
			'</p> ' +
			'</div>';

		return error_page;

	}

	utils.getHtmlDataTable = function (data_points){

		var content = "";
		content += "<thead class='datathead'>" +
			"<tr class='datatr'>" +
			"<th class='datath'>Date</th>" +
			"<th class='datath'>a</th>" +
			"<th class='datath'>T</th>" +
			"<th class='datath'>c</th>" +
			"</tr>" +
			"</thead>" +
			"<tbody class='datatbody'>";
		if (data_points.length != 0) {
			try {
				for (var i = 0; i < data_points.length; i++) {
					if (!(data_points[i].a == null) && !(data_points[i].t == null) && !(data_points[i].c == null)) {
						content += "<tr class='datatr'>";
						content += "<td class=\"datatd filterable-cell\">" + data_points[i].date + "</td>";
						content += "<td  class=\"datatd filterable-cell\">" + Math.round(data_points[i].a * 100) / 100 + "</td>";
						content += "<td  class=\"datatd filterable-cell\">" + Math.round(data_points[i].t * 100) / 100 + "</td>";
						content += "<td  class=\"datatd filterable-cell\">" + Math.round(data_points[i].c * 100) / 100 + "</td>";
						content += "</tr>";
					}
				}
			}
			catch (e) {
				utils.logerr(arguments.callee.name, e)
				return "";
			}// catch
			content += "</tbody>";

		}
		return content;


	}

	utils.fadeInHtmlTable = function  (points, table_div){
		var content;
		if(table_div!=null){
			content = utils.getHtmlDataTable(points);
		}
		$(table_div).html(content);
	}
    
    /*
		function name: format_url
	*/
	utils.format_url = function (root, type){
		var url =  encodeURI(root);
		if(type){
			var url = encodeURI(root  +   '/' + type);
		}
		return url;
	}
    
    /*
		function name: NormalDensityZx
	*/
	utils.NormalDensityZx = function ( x, Mean, StdDev ) {
		var a = x - Mean;
		return Math.exp( -( a * a ) / ( 2 * StdDev * StdDev ) ) / ( Math.sqrt( 2 * Math.PI ) * StdDev );
	}
    
    /*
		function name:	standartNormalQx
		Description:	Calculates Q(x), the right tail area under the Standard Normal Curve.
	*/
	utils.standardNormalQx = function (x, glb_mean, glb_dev) {
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
		qx = utils.NormalDensityZx( x, glb_mean, glb_dev) * ( ( 0.319381530 * t1 ) + ( -0.356563782 * t2 ) +
		  ( 1.781477937 * t3 ) + ( -1.821255978 * t4 ) + ( 1.330274429 * t5 ) );
		if ( negative == true )
		  qx = 1 - qx;
		return qx;
	}
    
    /*
		function name:	StandardNormalPx
		Description:	Calculates P(x), the left tail area under the Standard Normal Curve, which is 1 - Q(x).
	*/
	utils.standardNormalPx = function ( x, glb_mean, glb_dev) {
		return 1 - utils.standardNormalQx(x, glb_mean, glb_dev);
	}
	/*
		function name:	StandardNormalAx
		Description:	Calculates A(x), the area under the Standard Normal Curve between +x and -x.
	*/
	utils.standardNormalAx = function ( x , glb_mean, glb_dev) {
		return 1 - ( 2 * utils.standardNormalQx(Math.abs(x), glb_mean, glb_dev) );
	}
	
	
	
    return utils;

    
    
});
