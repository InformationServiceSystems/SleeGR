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
		var x_label_id = '#xLabel';
		var y_label_id = '#yLabel';
		var chk_type1 = '#chk_type1';
		var multi_timerange = '#timerange';
		var picker_id = '#reservation';
		var flask_data = document.getElementById('main_data');
		var correlationList;
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
				setup.select_all([chk_data, chk_type1]);
				setup.setup_datepicker(picker_id, time, update_data);
				setup.set_default_picker(time, dateRange, picker_id);
				correlationList = setup.get_correlationsList(url);
				setup.fillInXlabels(correlationList, x_label_id);
				setup.fillInYlabels(url, user_id, correlationList, correlations_id, x_label_id, y_label_id);

				$('body').on('change', multi_timerange, function() {
					updater.update_mutlichart(url, user_id, time.date_from, time.date_to, multichart_id, table_id, chk_data,$(multi_timerange).val()=='First 5 minutes');
				});
				$('body').on('change', x_label_id, function() {
					setup.fillInYlabels(url, user_id, correlationList, correlations_id, x_label_id, y_label_id);
				});
				$('body').on('change', y_label_id, function() {
					updater.update_correlations(url, user_id, correlationList, correlations_id)
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
	init.initLogin = function () {

		require(['jquery', 'auth0', 'icheck', 'bootstrap'], function ($, Auth0) {
			$(function () {
        		$('input').iCheck({
          			checkboxClass: 'icheckbox_square-blue',
          			radioClass: 'iradio_square-blue',
          			increaseArea: '20%' // optional
				});
      		});

			var auth0 = new Auth0({
				domain:         'mircopp.eu.auth0.com',
				clientID:       '6fP99Tdfa3W2xWgfQGEtSO0EC83GOZ9a',
				callbackURL:    'http://localhost:5000/callback'
			  });

			// sign-in with social provider with plain redirect
			$('.signin-google').on('click', function() {
				auth0.signin({connection: 'google-oauth2'}); // use connection identifier
			  });


			// sign-in with social provider using a popup (window.open)
			$('.signin-google-popup').on('click', function() {
				auth0.signin({popup: true, connection: 'google-oauth2'},
					function(err, profile, id_token, access_token, state) {
						//store the profile and id_token in a cookie or local storage
						//$.cookie('profile', profile);
						//$.cookie('id_token', id_token);

				});
			  });

		});

	}

	return init;
});


