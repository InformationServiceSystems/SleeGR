/**
 * Configuration file for all requirejs dependencies
 * used in order to achieve dynamically loaded javascript files
 */

require.config({
    baseUrl: 'static',
    paths: {
        'amcharts':             'js/amcharts/amcharts',
        'amcharts.serial':      'js/amcharts/serial',
        'amcharts.stock':       'js/amcharts/amstock',
        'amcharts.themeLight':  'http://www.amcharts.com/lib/3/themes/light',
        'amcharts.gauge':       'http://www.amcharts.com/lib/3/gauge',
        'amcharts.export':      'amcharts/plugins/export/export',
        'jquery':               'js/jquery/jquery',
        'jqueryui':             'js/jquery/jquery-ui',
        'bootstrap':            'bootstrap/js/bootstrap.min',
        'app':                  'dist/js/app.min',
        'charts.updater':       'js/chart_updater',
        'charts':               'js/isscharts/charts',
        'common.functions':     'js/utils/common_functions',
        'amcharts.functions':   'js/isscharts/functions/amCharts_functions',
        'highcharts.functions': 'js/isscharts/functions/highcharts_functions',
        'moment':               'http://momentjs.com/downloads/moment',
        'highcharts':           'https://code.highcharts.com/highcharts',
        'highcharts.exporting': 'https://code.highcharts.com/modules/exporting',
        'datepicker':           'plugins/daterangepicker/daterangepicker',
        'jquery.datatables':    'plugins/datatables/jquery.dataTables.min',
        'bootstrap.tables':     'plugins/datatables/dataTables.bootstrap.min',
        'jquery.slimScroll':    'plugins/slimScroll/jquery.slimscroll.min',
        'fastClick':            'plugins/fastclick/fastclick.min',
        'setup':                'js/setup'
    },
    shim:  {
        'highcharts': {
            exports: 'Highcharts',
            deps: ['jquery']
        },
        'highcharts.exporting': {
            deps: ['jquery', 'highcharts']
        },
        'amcharts.gauge': {
			deps: [ 'amcharts' ],
			exports: 'AmCharts',
			init: function() {
				AmCharts.isReady = true;
			}
		},
        'amcharts.themeLight': {
            deps: ['amcharts']
        },
        'amcharts.serial': {
			deps: [ 'amcharts' ],
			exports: 'AmCharts',
			init: function() {
				AmCharts.isReady = true;
			}
		},
        'amcharts.stock': {
            deps: [ 'amcharts' ],
			exports: 'AmCharts',
			init: function() {
				AmCharts.isReady = true;
			}
        },
        'amcharts.export': {
            deps: ['amcharts']
        },
        'bootstrap': {
            deps: ['jquery']
        },
        'app':{
            deps: ['jquery']
        }
    }
});