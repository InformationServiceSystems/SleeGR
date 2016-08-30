define (['jquery', 'charts'], function ($, chart){
    var setup = {};
    /**
     * update functions
     */
    setup.update_correlations = function (url, user_id, linearData, correlations_id){
        var nextDay;
        var xLabel = $('#xLabel').val();
        var yLabel = $('#yLabel').val();
        for (var i = 0; i<linearData.length; i++){
            if (linearData[i].x_label==xLabel&&linearData[i].y_label==yLabel){
                nextDay=linearData[i].next_day;
            }
        }
        var currentTitle = 'Correlation between <strong>' + xLabel + '</strong> and <strong>' + yLabel + '</strong>';
        chart.charts_getCorrelations(url+'correlation', true, user_id, correlations_id, currentTitle, xLabel, yLabel, nextDay);
    }


    setup.update_mutlichart = function (url, user_id, date_from, date_to, multichart_id, table_id, chk_data, only5min,newData){
        var show_type1 	= $("#chk_type1").is(':checked');
        var show_data 	= $("#chk_data").is(':checked');

        if (newData){
            chart.charts_createMultiChart(url+'heartrate', show_type1, show_data, user_id, date_from, date_to, multichart_id, table_id, chk_data, only5min);
        }
        else{
            chart.charts_switchMultiChart(show_type1, show_data, multichart_id, chk_data, only5min);
        }
    }
    setup.update_heatmap = function (url, user_id, date_from, date_to, heatmap_id){
        chart.charts_createHeatmap(url+'sleepPoints', user_id, date_from, date_to, heatmap_id);
    }

    setup.update_gaussian = function (url, user_id,  date_from, date_to , gaussian_id){
        chart.charts_createGaussian(url+'sleepPoints', user_id,  date_from, date_to , gaussian_id);
    }

    

    
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
        setup.update_correlations(url, user_id, linearData, correlations_id);
    }
    setup.contains = function (a, obj) {
        for (var i = 0; i < a.length; i++) {
            if (a[i] == obj) {
                return true;
            }
        }
        return false;
    }
    
    return setup;

});