var app = angular.module('app', ['ngRoute', 'ngResource', 'ngCookies']);

app.run( function run( $http, $cookies ){
    // For CSRF token compatibility with Django
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]);

app.config(function($routeProvider, $locationProvider) {
	$routeProvider.when('/', {
		templateUrl: 'static/templates/main.html',
		controller: 'MainController'
	});
	$routeProvider.when('/reg/', {
		templateUrl: 'static/templates/reg.html',
		controller: 'RegistrationController'
	});
	$routeProvider.when('/login/', {
		templateUrl: 'static/templates/login.html',
		controller: 'LoginController'
	});
	$routeProvider.when('/logout/', {
		templateUrl: 'static/templates/logout.html',
		controller: 'LogoutController'
	});
	$routeProvider.otherwise({
		redirectTo: '/'
	});
});

// app.factory('Exercises', ['$resource', function($resource) {
//     return $resource('/api/exercises');
// }]);

app.controller('MainController', ['$scope', '$http', '$location', '$log', function($scope, $http, $location, $log) {
	$http.post('api/check/auth/')
	.error(function(data, status) {
		$location.path('/login/')
	});
}]);

app.controller('RegistrationController', ['$scope', '$http', '$location', '$log', function($scope, $http, $location, $log) {
	$scope.submit = function() {
		var inData = { reg: $scope.new_user };
		$http.post('/reg/', angular.toJson(inData))
		.success(function(data, status) {
			$location.path('/login');
		})
		.error(function(data, status) {
			if (status == '404') { $log.error(data); }
			if (status == '403') { $scope.error = data['auth']; }
		})
	};
}]);

app.controller('LoginController', ['$scope', '$http', '$log', '$location', function($scope, $http, $log, $location) {
	$scope.submit = function() {
		var inData = { login: $scope.user };
		$http.post('/login/', angular.toJson(inData))
		.success(function(data, status) {
			$log.debug(data);
			$location.path('#/');
		})
		.error(function(data, status) {
			if (status == '404') { $scope.error = data['error']; }
			if (status == '403') { $scope.error = data['auth']; }
		});
	}
}]);

app.controller('LogoutController', ['$http', '$location', '$log', function($http, $location, $log) {
	$http.post('/logout/')
		.success(function() {
			$log.debug('logout success');
			$location.path('/');
		})
		.error(function() {
			$log.warn('logout failure');
		});
}]);

app.directive('usernameUnique', ['$http', function($http) {
	return {
		restrict: 'A',
		require: 'ngModel',
		link: function(scope, element, attrs, c) {
			scope.$watch(attrs.ngModel, function(v) {
				$http({
					method: 'POST',
					url: '/api/check/',	
					data: {'username': v}			
				}).success(function(data, status) {
					c.$setValidity('unique-name', true);
				}).error(function(data, status) {
					c.$setValidity('unique-name', false);
				});
			});
		}
	}
}]);

app.directive('emailUnique', ['$http', function($http) {
	return {
		restrict: 'A',
		require: 'ngModel',
		link: function(scope, element, attrs, c) {
			scope.$watch(attrs.ngModel, function(v) {
				$http({
					method: 'POST',
					url: '/api/check/',
					data: {'email': v}				
				}).success(function(data, status) {
					c.$setValidity('unique-email', true);
				}).error(function(data, status) {
					c.$setValidity('unique-email', false);
				});
			});
		}
	}
}]);
