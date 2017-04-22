(function(){
  'use strict';

var matchApp = angular.module('ErrosLog', [
  'ngRoute','angular.filter', 'ui.bootstrap','moment-picker',
]);
matchApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/applications', {
        templateUrl: 'applications.html',
        controller: 'ApplicationController as ctrl'
      }).
      when('/functions', {
        templateUrl: 'functions.html',
        controller: 'FunctionsController as ctrl'
      }).
      when('/reporting', {
        templateUrl: 'reporting.html',
        controller: 'ReportingController as ctrl'
      }).
      otherwise({
        redirectTo: '/applications'
      });
  }]);;
})();