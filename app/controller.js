
var app= angular.module('ErrosLog');

app.controller("ApplicationController", function($scope, $http, $timeout){
	var self = this;
	$http.get("rest/applications").then(function(response){
		self.applications = response.data;
	});		

});
app.controller("FunctionsController", function($scope, $http, $location){
		var self = this;
		$http.get("rest/functions").then(function(response){
		self.functions = response.data;
	});		
});


