function AppService($window){
	var Sandbox = function(){
		this.register = {};
		this.loading = true;
	};

	Sandbox.prototype.subscribe = function(key, callback){
		this.register[key] = callback;
	};

	Sandbox.prototype.publish = function(key, options){
		this.register[key](options);
	};

	Sandbox.prototype.ready = function(callback){
		this.loading = false;
		if($window.cordova){
			document.addEventListener('deviceready', callback, false);
		} else {
			callback();
		}
	};

	Sandbox.prototype.isDevice = function(){
		return $window.cordova !== undefined;
	};

	Sandbox.prototype.onDeviceReady = function(callback){
		if(this.isDevice()){
			this.ready(callback);
		}
	};

	return new Sandbox();
};
