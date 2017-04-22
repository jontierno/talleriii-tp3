
var app= angular.module('ErrosLog');

app.controller("ApplicationController", function($scope, $http, $timeout){
	var self = this;
	$http({
    	url: "rest/applications", 
    	method: "GET",
 	}).then(function(response){
		self.applications = response.data.result;
		self.more = response.data.more;
		self.cursor = response.data.cursor;
	});		

});
app.controller("FunctionsController", function($scope, $http, $location){
	var self = this;
	$http({
    	url: "rest/functions", 
    	method: "GET",
    	params: {time: 6}
 	}).then(function(response){
		self.functions = response.data.result;
		self.more = response.data.more;
		self.cursor = response.data.cursor;
	});		
});


