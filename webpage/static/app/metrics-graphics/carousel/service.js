function MetricsGraphicsCarouselService (Files, AppService) {
	var GraphicTypes = function(){
		this.types = [{
			label: 'line',
			font_icon_name: 'line-chart',
			options: {
				chart_type: 'line'
			}
		}, {
			label: 'point',
			font_icon_name: 'dot-circle-o',
			options: {
				chart_type: 'point'
			}
		}, {
			label: 'scatter',
			font_icon_name: 'bar-chart',
			options: {
				chart_type: 'point',
				least_squares: true
			}
		}];
	};

	GraphicTypes.prototype.getLabels = function(){
		if(angular.isUndefined(this.labels)){
			this.labels = this.types.map(function(type){
				return type.label;
			});
		}
		return this.labels;
	};

	GraphicTypes.prototype.getViewTypes = function(){
		if(angular.isUndefined(this.labels)){
			this.labels = this.types.map(function(type){
				return {
					label: type.label,
					font_icon_name: type.font_icon_name
				};
			});
		}
		return this.labels;
	};

	GraphicTypes.prototype.getChartTypeByLabel = function(label){
		return this.types.filter(function(type){
			return type.label == label;
		})[0];
	};

	var DataEndpoint = function(options){
		this.src = options.src;
	};

	DataEndpoint.prototype.getJSON = function(callback){
		jQuery.getJSON(this.src+'/json.php', callback);
	};

	DataEndpoint.prototype.getFile = function(srcFile, callbacks){
		AppService.onDeviceReady(function(){
			Files.getFile(srcFile, callbacks);
		});
	};

	DataEndpoint.prototype.download = function(srcFile, destFile, callbacks){
		AppService.ready(function(){
			AppService.publish('toast', 'is a device: ' + AppService.isDevice().toString());
		});
		var url = this.src+'/'+srcFile;
		AppService.onDeviceReady(function(){
			Files.download({
				url: url,
				targetPath: cordova.file.dataDirectory + destFile,
				trustHosts: true,
				options: {}
			}, function(result) {
				if(callbacks.finished) callbacks.finished(result);
			}, function(err) {
				if(callbacks.err) callbacks.err(err);
			}, function (progress) {
				if(callbacks.progress) callbacks.progress(progress);
			});
		});
	};

	DataEndpoint.prototype.upload = function(srcFile, destFile, callbacks){
		var server = this.src+'/'+destFile;
		AppService.onDeviceReady(function(){
			Files.download({
				server: server,
				targetPath: cordova.file.dataDirectory + srcFile,
				trustHosts: true,
				options: {}
			}, function(result) {
				if(callbacks.success) callbacks.success(result);
			}, function(err) {
				if(callbacks.error) callbacks.error(err);
			}, function (progress) {
				if(callbacks.progress) callbacks.progress(progress);
			});
		});
	};

	DataEndpoint.prototype.fileExists = function(filename, success, error){
		Files.fileExists(filename, success, error);
	};

 	return {
		graphs: new GraphicTypes(),
		exchange: new DataEndpoint({
			src: 'http://wiquation.net'
		})
	};
};
