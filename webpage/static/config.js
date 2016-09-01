/**
 * Configuration file for all requirejs dependencies
 * used in order to achieve dynamically loaded javascript files
 */

require.config({
    baseUrl: 'static',
    paths: {
        'amcharts':             'amcharts/amcharts',
        'amcharts.serial':      'amcharts/serial',
        'amcharts.stock':       'amcharts/amstock',
        'amcharts.themeLight':  'http://www.amcharts.com/lib/3/themes/light',
        'amcharts.gauge':       'http://www.amcharts.com/lib/3/gauge',
        'amcharts.export':      'amcharts/plugins/export/export',
        'jquery':               'plugins/jQuery/jQuery-2.1.4.min',
        'jqueryui':             'jquery-ui',
        'bootstrap':            'bootstrap/js/bootstrap.min',
        'app':                  'dist/js/app.min',
        'charts':               'charts',
        'moment':               'http://momentjs.com/downloads/moment',
        'highcharts':           'https://code.highcharts.com/highcharts',
        'highcharts.exporting': 'https://code.highcharts.com/modules/exporting',
        'datepicker':           'plugins/daterangepicker/daterangepicker',
        'jquery.datatables':    'plugins/datatables/jquery.dataTables.min',
        'bootstrap.tables':     'plugins/datatables/dataTables.bootstrap.min',
        'jquery.slimScroll':    'plugins/slimScroll/jquery.slimscroll.min',
        'fastClick':            'plugins/fastclick/fastclick.min',
        'setup':                'setup'
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
        }
    }
});