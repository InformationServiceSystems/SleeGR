/**
 * setup module
 * includes functions to dynamically load content
 */

define (['jquery', 'common.functions', 'charts.updater'], function ($, utils, updater){
    var setup = {};  

    
    /**
     * setup page functions
     */
    setup.set_default_picker = function (time, dateRange, picker_id){

        var d = new Date();
        var curr_date = d.getDate();
        var curr_month = d.getMonth()+1;
        var curr_year = d.getFullYear();
    
        var startDay = curr_date;
        var startMonth = curr_month-dateRange;
        var startYear = curr_year;
    
        if (startDay>28){
            startDay=28;
        }
    
        while(startMonth<1){
            startYear--;
            startMonth = 12 + startMonth;
        }
        time.date_from 	= startDay.toString()+'.' + startMonth.toString() + '.' +startYear.toString();
        time.datepicker_date_from = startMonth.toString() + '/' + startDay.toString() + '/' + startYear.toString();
    
        time.date_to 	= curr_date.toString()+'.'+curr_month.toString()+'.'+curr_year.toString();
        time.datepicker_date_to = (curr_month).toString() + '/' + curr_date.toString() + '/' + curr_year.toString();

        $(picker_id).attr ('value', time.datepicker_date_from + " - " + time.datepicker_date_to);
    }


    setup.select_all = function (checkboxes){
        checkboxes.forEach(function(html_id){
            $(html_id).attr('checked', true);
        });
    }


    setup.fillInXlabels = function(linearData){
        var temp = "";
        var xLabels = [];
        for (var i = 0; i<linearData.length; i++){
            if (!(utils.contains(xLabels, linearData[i].x_label))){
                xLabels.push(linearData[i].x_label);
                temp += "<option>" + linearData[i].x_label + "</option>";
            }
        }
        $('#xLabel').html(temp);
    }
    setup.fillInYlabels = function (url, user_id, linearData, correlations_id){
        var currXlabel = $('#xLabel').val();
        var temp = "";
        for (var i = 0; i<linearData.length; i++){
            if (linearData[i].x_label==currXlabel){
                temp += "<option>" + linearData[i].y_label + "</option>";
            }
        }
        $('#yLabel').html(temp);
        updater.update_correlations(url, user_id, linearData, correlations_id);
    }
    

    setup.setup_datepicker = function (picker_id, time, update_function) {
        $(picker_id).daterangepicker(
					{
						locale: {
							format: 'DD.MM.YYYY'
						},
						"startDate": time.datepicker_date_from,
						"endDate": time.datepicker_date_to
					},
					function(start, end, label) {
						time.date_from=start.format('DD.MM.YYYY');
						time.date_to=end.format('DD.MM.YYYY');
						update_function ();
					}
			);
    }
    
    setup.get_correlationsList = function(url){
        var correlationsUrl = utils.format_url(url, 'get_correlations_list');
        var list;
        $.ajax({type : 'GET', url: correlationsUrl, success: function (data) {
                list=JSON.parse(data);
            },
            async: false
        });
        return list;
    }
    
    return setup;

});