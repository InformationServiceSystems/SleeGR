// config.js

require.config({
    baseUrl: 'static',
    paths: {
        amcharts:   'amcharts/amcharts',
        serial:     'amcharts/serial',
        amStock:    'amcharts/amstock',
        themeLight: 'http://www.amcharts.com/lib/3/themes/light',
        gauge:      'http://www.amcharts.com/lib/3/gauge',
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
    },
    shim:  {
        'highcharts': {
            exports: "Highcharts",
            deps: ["jquery"]
        },
        'exporting': {
            deps: ['highcharts']
        },
        'gauge': {
			deps: [ 'amcharts' ],
			exports: 'AmCharts',
			init: function() {
				AmCharts.isReady = true;
			}
		},
        'themeLight': {
            deps: ['amcharts', 'serial', 'amStock']
        },
        'serial': {
			deps: [ 'amcharts' ],
			exports: 'AmCharts',
			init: function() {
				AmCharts.isReady = true;
			}
		},
        'amStock': {
            deps: ['amcharts', 'serial']
        }
    }
});