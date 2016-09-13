/**
 * Created by Mirco on 06.09.2016.
 */
define([], function () {

	var init = new Object();

	init.initDashboard = function () {

		/**
		 * global fields
		 */
		var url = 'http://localhost:5000';
		var multichart_id = '#chartdiv1';
		var table_id = '#tablediv';
		var correlations_id = '#correlationsdiv';
		var heatmap_id = 'heatmapdiv';
		var gaussian_id = 'gaussiandiv';
		var chk_data = '#chk_data';
		var chk_type1 = '#chk_type1';
		var multi_timerange = '#timerange';
		var picker_id = '#reservation';
		var flask_data = document.getElementById('main_data');
		var correlations = flask_data.getAttribute('data-cdn-corellations');
		var linearData;
		var time = new Object();
		var dateRange = 4;
		var user_id	= flask_data.getAttribute('data-cdn-user');
		var dependencies = ['jquery', 'setup', 'charts.updater', 'datepicker','jqueryui', 'bootstrap', 'app', 'jquery.slimScroll', 'fastClick'];

		require(dependencies, function($, setup, updater){

			function update_data(){
				if (time.date_from != null && time.date_to != null){
					updater.update_mutlichart(url, user_id, time.date_from, time.date_to, multichart_id, table_id, chk_data, $(multi_timerange).val()=='First 5 minutes', true);
					updater.update_heatmap(url, user_id, time.date_from, time.date_to, heatmap_id);
					//updater.update_gaussian(url, user_id, time.date_from, time.date_to, gaussian_id);
				}
			}

			/**
			 * on ready function
			 */
			$(function() {
				var linearData = $.parseJSON(correlations);
				setup.select_all([chk_data, chk_type1]);
				setup.set_default_picker(time, dateRange, picker_id);
				setup.fillInXlabels(linearData);
				setup.fillInYlabels(url, user_id, linearData, correlations_id);
				setup.setup_datepicker(picker_id, time, update_data);

				$('body').on('change', '#timerange', function() {
					updater.update_mutlichart(url, user_id, time.date_from, time.date_to, multichart_id, table_id, chk_data,$(multi_timerange).val()=='First 5 minutes');
				});
				$('body').on('change', '#xLabel', function() {
					setup.fillInYlabels(url, user_id, linearData, correlations_id);
				});
				$('body').on('change', '#yLabel', function() {
					updater.update_correlations(url, user_id, linearData, correlations_id)
				});

				$(chk_type1).click(function() {
					var show_data = $(chk_data).is(':checked');
					var visible = $(chk_type1).is(':checked');
					updater.setTypeVisible(multichart_id, 'Type1', visible, show_data);
				});

				$(chk_data).click(function() {
					var checked = $(chk_data).is(':checked');
					updater.setScatterVisible(multichart_id, checked);
				});
				update_data();

			});

		});

	}

	return init;
});


