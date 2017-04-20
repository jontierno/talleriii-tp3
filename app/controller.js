
var app= angular.module('ErrorsLog');

app.controller("ApplicationsController", function($scope, $http, $timeout){

});
app.controller("FunctionController", function($scope, $http, $location){

});
app.controller("MainController", function($scope, $http, $timeout){
		$scope.msgInfoOperacion = "";
		$scope.messageclass = "";
		$scope.serverurl = "";
		$scope.hasMessage = false;
		$scope.limpiarMsgInfo = function(){
		
			$scope.messageclass = "";
			$scope.hasMessage = false;
		}
		$scope.printMessage = function(message){
			$scope.hasMessage = true;
			$scope.msgInfoOperacion = message;
			$scope.messageclass = "";
		}
		$scope.errorMessage = function(message){
			$scope.hasMessage = true;
			$scope.msgInfoOperacion = message;
			$scope.messageclass = "bg-danger";
			$timeout(function() {
				$scope.limpiarMsgInfo();	
			},3000);
		}
		$scope.successMessage = function(message){
			$scope.hasMessage = true;
			$scope.msgInfoOperacion = message;
			$scope.messageclass = "bg-success";
			$timeout(function() {
				$scope.limpiarMsgInfo();	
			},3000);
		}
	});