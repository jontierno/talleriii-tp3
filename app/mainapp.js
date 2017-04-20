(function(){
  'use strict';

var matchApp = angular.module('ErrorsLog', [
  'ngRoute','angular.filter', 'mgcrea.ngStrap'
]);
matchApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/applications', {
        templateUrl: 'applications.html',

      }).
      when('/functions', {
        templateUrl: 'functions.html',
        
      })
      otherwise({
        redirectTo: '/applications'
      });
  }]);;
})();