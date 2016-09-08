/**
 * Created by Mirco on 07.09.2016.
 */

define(['jquery', 'charts', 'common.functions'], function ($, Chart, utils) {
   
    var updater = new Object();
	var chart = new Chart(0, 0, 12, [], 0, 0, 0);
    var multichart_points;


    /**
     * update utils
     */
    updater.update_correlations = function (url, user_id, linearData, correlations_id){
        var nextDay;
        var xLabel = $('#xLabel').val();
        var yLabel = $('#yLabel').val();
        for (var i = 0; i<linearData.length; i++){
            if (linearData[i].x_label==xLabel&&linearData[i].y_label==yLabel){
                nextDay=linearData[i].next_day;
            }
        }
        var currentTitle = 'Correlation between <strong>' + xLabel + '</strong> and <strong>' + yLabel + '</strong>';
        var reqUrl = utils.format_url(url, 'correlation');
        updater.charts_getCorrelations(reqUrl, true, user_id, correlations_id, currentTitle, xLabel, yLabel, nextDay);
    }
    
    /*
	 function name: charts_createLinearCurve
	 */
	
	updater.charts_getCorrelations = function (rooturl, show_data, user_id, html_id, title, xLabel, yLabel, nextDay){
		var data = {
					userId: user_id,
					xAxis: xLabel,
					yAxis: yLabel,
					nextDay: nextDay
					};

		$.ajax({type: "POST", url: rooturl, data: data, success: function(result){
			var data_points = JSON.parse(result);
			if (data_points!=null){
				console.log('data from  %s', rooturl);
                chart.draw_linearChart(data_points, title, xLabel, yLabel, html_id);
			}
			else{
				var error_text = 'There is no correlation data available from ' + xLabel + ' to ' + yLabel + '. Please choose other labels.';
				chart.clearHighchart(html_id, error_text);
			}
			return;
	
		}});
	
	}

    updater.update_mutlichart = function (url, user_id, date_from, date_to, multichart_id, table_id, chk_data, only5min,newData){
        var show_type1 	= $("#chk_type1").is(':checked');
        var show_data 	= $("#chk_data").is(':checked');

        if (newData){
            var reqUrl = utils.format_url(url, 'heartrate');
            updater.charts_createMultiChart(reqUrl, show_type1, show_data, user_id, date_from, date_to, multichart_id, table_id, chk_data, only5min);
        }
        else{
            updater.charts_switchMultiChart(show_type1, show_data, multichart_id, chk_data, only5min);
        }
    }

    updater.charts_createMultiChart = function (rooturl, show_type1, show_data, user_id, begin_date, end_date, html_id, table_id, data_select_id, only_5mins){
		var data = {
					userId: user_id,
					type: "Cooldown",
					beginDate: begin_date,
					endDate: end_date
					};
		$.ajax({type: "POST", url: rooturl, data: data, success: function(result){
				multichart_points = eval(result);
				if (multichart_points.length!=0){
					console.log('data from  %s len: %d', rooturl, multichart_points.length);
					// the following commented lines are for getting type2 uncomment to get the results
					//$.ajax({url: type2_url, success: function(result_type2){
					//    	var points2 = eval(result_type2);
					//	console.log('data from  %s len: %d', type2_url, points2.length);
					//	addSerieses(points2, show_data, 'Type2', true, data_select_id, serieses,  'triangle');
					chart.draw_multiChart(multichart_points, show_data, 'Type1', show_type1, data_select_id, 'circle', html_id, only_5mins);
					utils.fadeInHtmlTable(multichart_points, table_id);
					//}});
				}
				else{
					var error_text = 'There is no heartrate data measured in the given time period. Please choose another period to analyse your personal heartrate data.';
					chart.clearHighchart(html_id, error_text);

					var no_data = utils.getNoDataDiv(error_text);
					$(table_id).html(no_data);
				}

			}});

	}


    updater.charts_switchMultiChart = function (show_type1, show_data, html_id, data_select_id, only_5mins){
		if (multichart_points.length != 0){
			chart.draw_multiChart(multichart_points, show_data, 'Type1', show_type1, data_select_id, 'circle', html_id, only_5mins);
		}
	}

	updater.setScatterVisible = function (html_id, visible){
		chart.setScatterVisible(html_id, visible);
	}

	updater.setTypeVisible = function (html_id, type, visible, showdata){
		chart.setTypeVisible(html_id, type, visible, showdata);
	}



    updater.update_heatmap = function (url, user_id, date_from, date_to, heatmap_id){
        var reqUrl = utils.format_url(url, 'sleepPoints');
        updater.charts_createHeatmap(reqUrl, user_id, date_from, date_to, heatmap_id);
    }

	updater.charts_createHeatmap = function (rooturl, user_id, begin_date, end_date, html_id){
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
				chart.create_heatmap(points, html_id, begin_date, end_date);
			}
			else{
				var error_text = 'There is no sleep data measured in the given time period. Please choose another period to analyse your personal sleep data.';
				chart.clearAmChart(html_id, error_text);
			}
		 }});

	}

    updater.update_gaussian = function (url, user_id,  date_from, date_to , gaussian_id){
        var reqUrl = utils.format_url(url, 'sleepPoints');
        updater.charts_createGaussian(reqUrl, user_id,  date_from, date_to , gaussian_id);
    }
	
	updater.charts_createGaussian = function (rooturl, user_id, begin_date, end_date, html_id){
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
						chart.create_gaussian(settings, points, html_id);
					}
					else{
						var error_text = 'There is no sleep data measured in the given time period. Please choose another period to analyse your personal sleep data.';
						chart.clearAmChart(html_id, error_text);
					}
	
					}});
			}});
		}
		catch(e){
			utils.logerr('charts_createGaussian', e);
		}
	
	
	}

    return updater;
});
