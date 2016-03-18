var DatepickIntervalDirective = function() {
	return {
        restrict: 'E',
				scope: {
					min: "=",
					max: "=",
					start: "=",
					end: "=",
					change: "="
				},
        templateUrl: 'static/app/templates/datepick-interval.tpl.html',
        controller: DatepickIntervalCtrl
    };
};
