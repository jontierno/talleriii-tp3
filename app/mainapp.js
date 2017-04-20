(function(){
  'use strict';

var matchApp = angular.module('ErrosLog', [
  'ngRoute','angular.filter', 'mgcrea.ngStrap'
]);
matchApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/applications', {
        templateUrl: 'applications.html',
        controller: 'ApplicationController'
      }).
      when('/functions', {
        templateUrl: 'functions.html',
        controller: 'FunctionsController'
      }).
      otherwise({
        redirectTo: '/applications'
      });
  }]);;
})();