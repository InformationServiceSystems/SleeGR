var DatepickSliderDirective = function() {
	return {
        restrict: 'E',
				scope: {
					min: "=",
					max: "=",
					start: "=",
					end: "=",
					change: "="
				},
        templateUrl: 'templates/datepick-slider.tpl.html',
        controller: DatepickSliderCtrl
    };
};
