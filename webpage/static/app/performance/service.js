function PerformanceAPI(){
	var WatchStack = function(key){
		this.key = key;
		this.stack = [];
	};

	WatchStack.prototype.mark = function(){
		if(typeof device !== 'undefined') return;
		if(this.stack.length > 0){
			var start = this.stack.shift();
			console.log('result performance for '+this.key, performance.now() - start);
		} else {
			this.stack.push(performance.now());
			console.log('start count performance for '+this.key);
		}
	};

	var PerformanceSlick = function(){
		this.map = {};
	};

	PerformanceSlick.prototype.perform = function(key){
		if(typeof device !== 'undefined') return;
		console.log('mark browser');
		var stack = this.map[key];
		if(angular.isUndefined(stack)){
			stack = new WatchStack(key);
			this.map[key] = stack;
		}
		stack.mark();
	};

	return new PerformanceSlick();
};
