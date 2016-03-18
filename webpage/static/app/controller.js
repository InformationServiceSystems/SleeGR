function AppCtrl($scope, $element, $mdToast, $document, AppService, $timeout) {
	$scope.loading = true;

	$scope.showCustomToast = function(message) {
    $mdToast.show({
      controller: function($scope, $mdToast) {
				$scope.message = message ? message : 'Hi, User.';
			  $scope.closeToast = function() {
			    $mdToast.hide();
			  };
			},
      templateUrl: 'static/app/templates/toast-template.tpl.html',
      parent : $document[0].querySelector('#deviceready'),
      hideDelay: 2000,
      position: 'top right'
    });
  };

	AppService.subscribe('toast', function(message){
		$scope.showCustomToast(message);
	});

	AppService.ready(function(){
		$scope.loading = false;
	});
};
