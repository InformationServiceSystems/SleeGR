function DatepickSliderCtrl($scope, $element) {
	$scope.update = function() {
		$scope.change($scope.start, $scope.end);
	};
};
