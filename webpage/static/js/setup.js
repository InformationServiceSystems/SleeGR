/**
 * setup module
 * includes functions to dynamically load content
 */

define (['jquery', 'charts'], function ($, chart){
    var setup = {};  

    
    /**
     * setup page functions
     */
    setup.set_default_picker = function (time, dateRange){

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
    
        document.getElementById('reservation').setAttribute("value", time.datepicker_date_from + " - " + time.datepicker_date_to);
    }


    setup.select_all = function (){
        $('#chk_type1').attr("checked",true);
        $('#chk_data').attr("checked",true);
    }


    setup.fillInXlabels = function(linearData){
        var temp = "";
        var xLabels = [];
        for (var i = 0; i<linearData.length; i++){
            if (!(setup.contains(xLabels, linearData[i].x_label))){
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
        chart.update_correlations(url, user_id, linearData, correlations_id);
    }
    setup.contains = function (a, obj) {
        for (var i = 0; i < a.length; i++) {
            if (a[i] == obj) {
                return true;
            }
        }
        return false;
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
    
    return setup;

});