// config.js

requirejs.config({
    baseUrl: 'static',
    paths: {
        //unfortunately does not work with am charts...
        // amCharts:   'amcharts/amcharts',
        // serial:     'amcharts/serial',
        // amStock:    'amcharts/amstock',
        // themeLight: 'http://www.amcharts.com/lib/3/themes/light',
        // gauge:      'http://www.amcharts.com/lib/3/gauge',
        jquery:     'plugins/jQuery/jQuery-2.1.4.min',
        jqueryui:  'jquery-ui',
        bootstrap:  'bootstrap/js/bootstrap.min',
        app:        'dist/js/app.min',
        charts:     'charts',
        moment:     'http://momentjs.com/downloads/moment',
        highcharts: 'https://code.highcharts.com/highcharts',
        exporting:  'https://code.highcharts.com/modules/exporting',
        datepicker: 'plugins/daterangepicker/daterangepicker',
        datatables: 'plugins/datatables/jquery.dataTables.min',
        tablesbootstrap:    'plugins/datatables/dataTables.bootstrap.min',
        slimScroll: 'plugins/slimScroll/jquery.slimscroll.min',
        fastClick:  'plugins/fastclick/fastclick.min',
        setup:      'setup'
    }
});