function MetricsGraphicsCarouselCtrl ($scope, $element, $controller, $timeout, $interval, $mdMedia, MetricsGraphicsCarouselService, AppService) {
	$controller('MetricsGraphicsCtrl', {
		$scope: $scope,
		$element: $element,
		$interval: $interval,
		$timeout: $timeout
	});

	$scope.loading = true;
	$scope.menuFontIcon = 'bar-chart';

	var Carousel = MetricsGraphicsCarouselService;
	var GraphTypes = MetricsGraphicsCarouselService.graphs;
	var Exchange = MetricsGraphicsCarouselService.exchange;

	$scope.types = GraphTypes.getViewTypes().map(function(type){
		type.class = 'md-raised';
		return type;
	});

	$scope.setChartType = function(label){
		var selectedType = GraphTypes.getChartTypeByLabel(label);
		$scope.types.forEach(function(type){
			if(type.label === label){
				type.class = 'md-primary';
			} else {
				type.class = '';
			}
		});
		var selectedType = GraphTypes.getChartTypeByLabel(label);
		$scope.menuFontIcon = selectedType.font_icon_name;
		$scope.graphicOptions = $scope.extendGraphic(selectedType.options);
	};

	$scope.setChartTypeAndReplot = function(label){
		$scope.setChartType(label);
		$scope.graphic($scope.graphicOptions);
		AppService.publish('toast', $scope.menuFontIcon);
	};

	$scope.minDate = new Date();
	$scope.maxDate = new Date();
	$scope.startDate = new Date();
	$scope.endDate = new Date();
	$scope.updateDatepickInterval = function(){
		if($scope.data.length === 0){
			$scope.startDate = new Date();
			$scope.endDate = new Date();
			$scope.minDate = new Date();
			$scope.maxDate = new Date();
		} else {
			$scope.startDate = $scope.data[0]['date'];
			$scope.endDate = $scope.data[$scope.data.length - 1]['date'];
			$scope.minDate = angular.copy($scope.startDate);
			$scope.maxDate = angular.copy($scope.endDate);
		}
	};

	$scope.replot = function(startDate, endDate){
		var subset = _.filter($scope.data, function(point) {
		  return (point.date >= startDate) && (point.date <= endDate);
		});
		//alert(subset.length);
		$scope.plot(subset);
	};

	$scope.styleMetricsOverlayer = function(){
		var css = {
			position: 'relative'
		};
		if($mdMedia('sm')){
			css.top = '-100px';
		} else {
			css.top = '-50px';
		}
		return css;
	};

	var innerElement = jQuery($element.children()[0]);
	var controlMenu= $element.find('#control_menu');
	$scope.layoutMetrics = function(){
		if(AppService.isDevice() === false) return;
		var innerHeight = parseInt(innerElement.css('height'));
		var menuHeight = parseInt(controlMenu.css('height'));
		return {
			'max-height': 'inherit',
			'height': (innerHeight-menuHeight)+'px'
		};
	};

	$scope.menuStyle = {
		display: 'block',
		height: ' 84px'
	};

	$scope.spacer = {
		float: 'left'
	};

	$scope.styleSpacer = function(){
		if(AppService.isDevice() === false) return;
		var containerWidth = parseInt(controlMenu.css('width'));
		var contentWidth = (controlMenu.children()['length']-1) * parseInt(jQuery(controlMenu.find('.md-menu')[1]).css('width'));
		var space = (containerWidth - contentWidth)/2;
		$scope.spacer.width = space+'px';
		$scope.spacer.height = '10px';
	};
	$scope.styleSpacer();

	$scope.plotCarousel = function(data){
		$scope.setChartType($scope.types[0].label);
		$scope.plot(data);
		$scope.updateDatepickInterval();
		$scope.loading = false;
	};

	var development = true;
	if(AppService.isDevice() === false){
		if(development){
			devMode();
		} else {
			$scope.plotCarousel([]);
			$scope.$apply();
			instantRequests();
		}
	}

	function devMode(){
		jQuery.getJSON('/getVisualTest', function(json){
			console.log(json);
			json = json.map(function(data){
				data.date = parseDate(data.date);
				return data;
			});
			$scope.plotCarousel(json);
			$scope.$apply();
		}).fail(function(err) {
			console.log(err);
		});
		eachWeekExecute();
	};

	function parseDate(raw){
		return moment(raw, "DD-MM-YYYY").toDate();
	};

	function eachDayExecute(){
		var value = 10;
		var count = moment();
		$interval(function(){
			value += 10;
			count = count.add(1, 'days');
			console.log(count.toDate(), value);
			$scope.addPoint({
				date: new Date(count.toDate().toString()),
				value: value
			});
		}, 1000);
	};

	//eachDayExecute();

	function eachWeekExecute(){
		var value = 10;
		var count = moment();
		var week = [];
		$interval(function(){
			week = [];
			for(var i = 0; i < 5; i += 1){
				value += 10;
				count = count.add(1, 'days');
				week.push({
					date: new Date(count.toDate().toString()),
					value: value
				});
			}
			value += 10;
			count = count.add(1, 'days');
			console.log(count.toDate(), value);
			$scope.addCollectionPoints(week);
		}, 1000);
	};

	//eachWeekExecute();

	function instantRequests(){
		alert('instantRequests');
		$interval(function(){
			jQuery.getJSON('/realtime', function(json){
				console.log(json);
				json = json.map(function(data){
					data.date = parseDate(data.date);
					return data;
				});
				$scope.addCollectionPoints(json);
				$scope.$apply();
			}).fail(function(err) {
				alert('Flask failed to send or is it your cause?');
				console.log('error', err);
			});
		}, 1000);
	};

	//instantRequests();

	function apply(json){
		var rates = json.dataset.data.map(function(point){
			return {
				value: point[5],
				date: point[0]
			};
		}).reverse().slice(0, 100);
		rates = MG.convert.date(rates, 'date');
		$scope.plotCarousel(rates);
		$scope.$apply();
	};

	function download(srcFile, destFile){
		Exchange.download(srcFile, destFile, {
			finished: function(result){
				AppService.publish('toast', "download compvare");
				readFile(destFile, function(content){
					apply(JSON.parse(content));
					AppService.publish('toast', "plot compvare");
				});
			},
			err: function(err){
				AppService.publish('toast', "error");
			},
			progress: function(progress){
				//AppService.publish('toast', "progress updates");
			}
		});
	};

	function readFile(filename, callback){
		Exchange.getFile(filename, {
			success: function(content){
				callback(content);
			},
			error: function(error){
				AppService.publish('toast', "error on file reading");
			},
			nofile: function(error){
				AppService.publish('toast', "there is no file: "+filename);
			}
		});
	};

	function upload(srcFile, destFile){
		Exchange.upload(srcFile, destFile, {
			finished: function(result){
				AppService.publish('toast', "upload compvare");
			},
			err: function(err){
				AppService.publish('toast', "error");
			},
			progress: function(progress){
				//AppService.publish('toast', "progress updates");
			}
		});
	};

	AppService.onDeviceReady(function(){
		var srcFile = 'json.php';
		var destFile = 'test.json';

		Exchange.fileExists(destFile, function(result){
			download(srcFile, destFile);
		}, function(err){
			AppService.publish('toast', "fileExists: error!!!");
		});

	});
};
