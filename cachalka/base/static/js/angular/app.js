var app = angular.module('app', ['ngRoute', 'ngResource', 'ngCookies', 'ui.bootstrap']);

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

 app.factory('Exercises', ['$resource', function($resource) {
     return $resource('/api/exercises');
 }]);

 app.factory('Sets', ['$resource', function($resource) {
 	return $resource('/api/sets');
 }]);

app.controller('MainController', ['$scope', '$http', '$location', '$log', 'Sets', function($scope, $http, $location, $log, Sets) {
	$http.post('api/check/auth/')
	.error(function(data, status) {
		$location.path('/login/')
	});

	Sets.query(function(data) {
		$log.debug(data);
		$scope.set = data.sets;
	});

	// Calendar
	$scope.today = function() {
		$scope.dt = new Date();
	};
	$scope.today();

	$scope.clear = function () {
		$scope.dt = null;
	};

	// Disable weekend selection
	//  $scope.disabled = function(date, mode) {
	//    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
	//  };

	$scope.toggleMin = function() {
		$scope.minDate = $scope.minDate ? null : new Date();
	};
	$scope.toggleMin();
	$scope.maxDate = new Date(2020, 5, 22);

	$scope.open = function($event) {
		$scope.status.opened = true;
	};

	$scope.dateOptions = {
		formatYear: 'yy',
		startingDay: 0
	};

	$scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
	$scope.format = $scope.formats[0];

	$scope.status = {
		opened: false
	};

	var tomorrow = new Date();
	tomorrow.setDate(tomorrow.getDate() + 1);
	var afterTomorrow = new Date();
	afterTomorrow.setDate(tomorrow.getDate() + 2);
	$scope.events =
	[
		{
			date: tomorrow,
			status: 'full'
		},
		{
			date: afterTomorrow,
			status: 'partially'
		}
	];

	$scope.getDayClass = function(date, mode) {
		if (mode === 'day') {
			var dayToCheck = new Date(date).setHours(0,0,0,0);

			for (var i=0;i<$scope.events.length;i++){
				var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

				if (dayToCheck === currentDay) {
					return $scope.events[i].status;
				}
			}
		}

		return '';
	};
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
