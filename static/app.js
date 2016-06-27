var app = angular.module('rfSwitchApp', []);
app.controller('DoorController',function($scope,$http){
	$scope.open = function() {
		$http.post("/api/open");	
	};
});
