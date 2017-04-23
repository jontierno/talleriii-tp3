
var app= angular.module('ErrosLog');

app.controller("ApplicationController", function($scope, $http, $timeout){
	var self = this;
	
	

 	self.reload = function (next){
 		var params = {};
 		if(next){
 			params.next = next;
 		}
 		var append= next; 
 		$http({
	    	url: "rest/applications", 
	    	method: "GET",
	    	params: params
	 	}).then(function(response){
	 		if(append){
				self.applications = self.applications.concat(response.data.result)
	 		} else {
	 			self.applications = response.data.result;
	 		}
			
			self.more = response.data.more;
			self.next = response.data.next;
		});	

 	};

 	self.loadMore = function (){
 		self.reload(self.next);
 	};
 	self.reload();


});
app.controller("FunctionsController", function($scope, $http, $location){
	var self = this;
	self.time=12;
 	self.reload = function (next){
 		var params = {time: self.time};
 		if(next){
 			params.next = next;
 		}
 		var append= next; 
 		$http({
	    	url: "rest/functions", 
	    	method: "GET",
	    	params: params
	 	}).then(function(response){
	 		if(append){
				self.functions = self.functions.concat(response.data.result)
	 		} else {
	 			self.functions = response.data.result;
	 		}
			
			self.more = response.data.more;
			self.next = response.data.next;
		});	

 	};

 	self.loadMore = function (){
 		self.reload(self.next);
 	};	

 	$scope.$watch(function(){
 		return self.time;
 	},function(){
 		self.reload()	
 	} );
});

app.controller("ReportingController", function($scope, $http, $location){
	var self = this;
	self.timestamp = moment();
	self.trace = "";
	self.app = "";
	self.report = function (){
		if(self.trace.length > 0 && self.timestamp && self.app.length >0){
			var params = {timestamp: self.timestamp, application : self.app, trace: self.trace};
			$http.post("/rest/report",params).then(function(){
				self.timestamp=moment();
				self.trace="";
				self.app="";
				alert("Reportado correctamente");
			}).catch(function(){
				alert("Error al reportar");
			});
		}
	}
});
