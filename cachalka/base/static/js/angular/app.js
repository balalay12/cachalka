
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

app.config(['$resourceProvider', function($resourceProvider) {
	$resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.config(function($routeProvider, $locationProvider) {
	$routeProvider.when('/', {
		templateUrl: template_dirs + '/main.html',
//		controller: 'MainController'
	});
	$routeProvider.when('/diary/', {
		templateUrl: template_dirs + '/diary.html',
		controller: 'DiaryController'
	});
	$routeProvider.when('/profile/', {
		templateUrl: template_dirs + '/profile.html',
		controller: 'ProfileController'
	});
	$routeProvider.when('/trainday/', {
		templateUrl: template_dirs + '/day.html',
		controller: 'DayController'
	});
	$routeProvider.when('/reg/', {
		templateUrl: template_dirs + '/reg.html',
//		controller: 'RegistrationController'
	});
	$routeProvider.when('/login/', {
		templateUrl: template_dirs + '/login.html',
//		controller: 'LoginController'
	});
	$routeProvider.when('/logout/', {
		templateUrl: template_dirs + '/logout.html',
//		controller: 'LogoutController'
	});
	$routeProvider.otherwise({
		redirectTo: '/'
	});
});

app.factory('Exercises', ['$resource', function($resource) {
	return $resource('/api/exercises/');
}]);

app.factory('Categories', ['$resource', function($resource) {
	return $resource('/api/categories/');
}]);

app.factory('Sets', ['$resource', function($resource) {
	return $resource('/api/sets/', {}, {
		getAllSets: {method:'GET', isArray: false}
	});
}]);

app.factory('Repeats', ['$resource', function($resource) {
	return $resource('/api/repeats/');
}]);

app.factory('AddDay', ['$resource', function($resource) {
	return $resource('/api/addtraining/');
}]);

app.factory('UserProfile', ['$resource', function($resource) {
	return $resource('/api/profile/');
}]);

app.factory('BodySize', ['$resource', function($resource) {
    return $resource('/api/bodysize/');
}]);

app.controller('ProfileController', [
				'$scope', '$http', 'UserProfile', 'BodySize', '$modal', '$rootScope',
				function($scope, $http, UserProfile, BodySize, $modal, $rootScope)
{
	// Check user authorization
	$http.post('api/check/auth/')
	.error(function(data, status) {
		$location.path('/login/')
	});

	UserProfile.query({id:user_id}, function(data) {
		console.log(data[0]);
		$scope.user = data[0];
	});

	$scope.BodySizeQuery = function() {
	    BodySize.query(function(data) {
            $scope.bodySize = data;
            for(var i=0; i<$scope.bodySize.length; i++ ) {
            	$scope.bodySize[i].date = new Date($scope.bodySize[i].date);
            }
        });
    };
	$scope.BodySizeQuery();

	$scope.$on('bodySizeAdded', function() {
	    $scope.BodySizeQuery();
	})

	$scope.addBodySize = function() {
	    var addBodySizeModal = $modal.open({
	        templateUrl: template_dirs + '/body_size.html',
	        controller: 'AddBodySizeController'
	    });
	};

	$scope.edit = function(id) {
		$rootScope.editBodySizeId = id;

		var editBodySizeModal = $modal.open({
			templateUrl: template_dirs + '/body_size.html',
			controller: 'EditBodySizeController'
		});
	};
}]);

app.controller('EditBodySizeController', [
				'$scope', '$modalInstance', '$rootScope', 'BodySize', '$filter',
				function($scope, $modalInstance, $rootScope, BodySize, $filter)
{
	$scope.adding = false;
	$scope.title = 'Изменить замеры тела';

	BodySize.query({id:$rootScope.editBodySizeId}, function(data) {
		$scope.bodySize = data[0];
		$scope.bodySize.date = new Date($scope.bodySize.date);
	});
	
	$scope.cancel = function() {
		$modalInstance.close();
	};
	$scope.delete = function() {
		BodySize.delete({id:$scope.bodySize.id}, function() {
			$rootScope.$broadcast('bodySizeAdded');
			$scope.cancel();
		})
	};
	$scope.submit = function() {
		$scope.bodySize.date = $filter('date')($scope.bodySize.date, 'yyyy-MM-dd');
		BodySize.save({update:$scope.bodySize, id:$scope.bodySize.id}, function() {
			$rootScope.$broadcast('bodySizeAdded');
			$scope.cancel();
		});
	};

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
		startingDay: 7
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
}])

app.controller('AddBodySizeController', [
                '$scope', '$modalInstance', '$filter', 'BodySize', '$rootScope',
                function($scope, $modalInstance, $filter, BodySize, $rootScope)
{
    $scope.cancel = function() {
        $modalInstance.close();
    };

    $scope.adding = true;
    $scope.title = 'Добавить замеры тела';

    $scope.submit = function() {
        $scope.bodySize.date = $filter('date')($scope.bodySize.date, 'yyyy-MM-dd');
        $scope.bodySize.user = user_id;
        BodySize.save({add: $scope.bodySize}, function() {
            $rootScope.$broadcast('bodySizeAdded');
            $scope.cancel();
        });
    };

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
		startingDay: 7
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
}])

app.controller('NavController', [
				'$scope', '$location', '$http',
				function($scope, $location, $http)
{
	var viewItems = function(bool) {
		$scope.auth = bool;
	}

	// Check user authorization
	$http.post('api/check/auth/')
	.success(function() {
		viewItems(true);
	})
	.error(function() {
		console.l
		viewItems(false);
	});

	$scope.$on('userIn', function() {
		viewItems(true);
	});

	$scope.$on('userOut', function() {
		viewItems(false);
	});
}]);

app.controller('DiaryController', [
				'$rootScope', '$scope', '$http', '$location', '$log', '$modal', 'Sets',
				function($rootScope, $scope, $http, $location, $log, $modal, Sets
){
	// Check user authorization
	$http.post('api/check/auth/')
	.error(function(data, status) {
		$location.path('/login/')
	});

	$scope.allSets = function() {
		Sets.getAllSets(function(data) {
			$scope.sets = data;
		});
	};
	$scope.allSets();

	$scope.$on('dayAdded', function() {
		$scope.allSets();
	});

    var myDate = new Date();
	$scope.month = myDate.getMonth() + 1;
	$scope.year = myDate.getFullYear();

	var getSetsByDate = function(_month, _year) {
	    Sets.getAllSets({month:_month, year: _year}, function(data) {
            $scope.sets = data;
        });
	};

	$scope.monthIncrement = function() {
	    if($scope.month >= 12) {
	        $scope.month = 1;
	        $scope.year = $scope.year + 1;
	        getSetsByDate($scope.month, $scope.year)
	    } else {
	        $scope.month = $scope.month + 1;
	        getSetsByDate($scope.month, $scope.year)
        }
	};

	$scope.monthDecrement = function() {
	    if($scope.month <= 1) {
	        $scope.month = 12;
	        $scope.year = $scope.year - 1;
	        getSetsByDate($scope.month, $scope.year)
	    } else {
	        $scope.month = $scope.month - 1;
	        getSetsByDate($scope.month, $scope.year)
        }
	};

	$scope.addDayTraining = function() {
		var addDayTraining = $modal.open({
			templateUrl: template_dirs + '/add_day.html',
			controller: 'AddDayTrainingController'
		});
	};

	$scope.dayLocation = function(_date) {
		$location.path('/trainday/').search({date: _date});
	}
}]);

app.controller('DayController', [
				'$scope', '$rootScope', '$http', '$location', '$routeParams', '$modal', 'Sets',
				function($scope, $rootScope, $http, $location, $routeParams, $modal, Sets
){
	// Check user authorization
	$http.post('api/check/auth/')
	.error(function(data, status) {
		$location.path('/login/')
	});

	$scope.allSets = function() {
		Sets.getAllSets({date_train: $routeParams.date}, function(data) {
			$scope.sets = data;
		});
	};
	$scope.allSets();

	$scope.$on('setsChange', function() {
		$scope.allSets();
	});

	$scope.addExercise = function(_date) {
		$rootScope.date = _date;
		var addExerciseModal = $modal.open({
			templateUrl: template_dirs + '/add_exercise.html',
			controller: 'AddExerciseController',
		});
	};

	$scope.editExercise = function(set_id) {
		$rootScope.editSetId = set_id;
		var editExerciseModal = $modal.open({
			templateUrl: template_dirs + '/edit_exercise.html',
			controller: 'EditExerciseController'
		});
	};

	$scope.addRepeat = function(set_id) {
		$rootScope.AddRepeatSetId = set_id
		var addRepeatModal = $modal.open({
			templateUrl: template_dirs + '/add_repeat.html',
			controller: 'AddRepeatController'
		})
	};

	$scope.editRepeat = function(repeat_id) {
		$rootScope.editRepeatId = repeat_id;
		var editRepeatModal = $modal.open({
			templateUrl: template_dirs + '/edit_repeat.html',
			controller: 'EditRepeatController'
		});
	}
}]);

app.controller('AddExerciseController', [
				'$scope', '$rootScope', 'Categories', 'Exercises', 'Sets', 'Repeats', 'AddDay', '$modalInstance',
				function($scope, $rootScope, Categories, Exercises, Sets, Repeats, AddDay, $modalInstance
){
	$scope.day = $rootScope.date;
	Categories.query(function(data) {
		$scope.categories = data;
		console.log(data);
	});

	$scope.$watch('cat', function(newVal, oldVal) {
		if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
			Exercises.query({category_id:newVal.category_id}, function(data) {
				$scope.exercises = data;
			});
		}
	});

	$scope.sets = [];
	$scope.addSet = function() {
		$scope.sets.push({weight: $scope.weight, repeats: $scope.repeats});
		console.log('in function' + $scope.sets);
		$scope.weight = null;
		$scope.repeats = null;
		return $scope.sets
	};

	$scope.cancel = function() {
	    $modalInstance.close();
	};

	$scope.submit = function() {
		var set = [];
		set.push({'date':$scope.day, 'user':user_id, 'exercise':$scope.exercise.exercise_id, 'repeats': $scope.sets});
		AddDay.save({add:set}, function() {
			$rootScope.$broadcast('setsChange');
			$scope.cancel();
		});
	};
}]);

app.controller('AddRepeatController', [
				'$scope', '$rootScope', 'Repeats', '$modalInstance',
				function($scope, $rootScope, Repeats, $modalInstance
){
	$scope.cancel = function() {
		$modalInstance.close();
	};

	$scope.submit = function() {
		$scope.set['set'] = $rootScope.AddRepeatSetId;
		console.log($scope.set);
 		Repeats.save({add:$scope.set}, function() {
 			$rootScope.$broadcast('setsChange');
			$modalInstance.close();
 		});
	};
}]);

app.controller('EditRepeatController', [
				'$scope', '$rootScope', 'Repeats', '$modalInstance',
				function($scope, $rootScope, Repeats, $modalInstance
){
	Repeats.query({id: $rootScope.editRepeatId}, function(data) {
		$scope.set = data[0];
	});

	$scope.cancel = function() {
		$modalInstance.close();
	};

	$scope.editEvent = function() {
		$rootScope.$broadcast('setsChange');
		$scope.cancel();
	}

	$scope.submit = function() {
		Repeats.save({update:$scope.set, id:$rootScope.editRepeatId}, function(){
			$scope.editEvent();
		});
	};

	$scope.delete = function() {
		Repeats.delete({id:$rootScope.editRepeatId}, function() {
			$scope.editEvent();
		});
	};
}]);

app.controller('EditExerciseController', [
				'$scope', '$rootScope', '$filter', 'Sets', 'Categories', 'Exercises', '$modalInstance',
				function($scope, $rootScope, $filter, Sets, Categories, Exercises, $modalInstance
){
	Categories.query(function(data) {
		$scope.categories = data;
		console.log(data);
	});

	Sets.query({id:$rootScope.editSetId}, function(data) {
		$scope.cat = {category_id:data[0].items.category_id, name:data[0].items.category_name};
		$scope.exercise = {exercise_id: data[0].exercise, name:data[0].items.exercise_name};
		$scope.date = new Date(data[0].date);
	});

	$scope.$watch('cat', function(newVal, oldVal) {
		if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
			Exercises.query({category_id:newVal.category_id}, function(data) {
				$scope.exercises = data;
			});
		}
	});

	$scope.cancel = function() {
		$modalInstance.close();
	};

	$scope.event = function() {
	    $rootScope.$broadcast('setsChange');
	    $scope.cancel();
	}

	$scope.delete = function() {
	    Sets.delete({id: $rootScope.editSetId}, function() {
	        $scope.event();
	    })
	};

	$scope.submit = function() {
		var upd_exercise = {'date': $filter('date')($scope.date, 'yyyy-MM-dd'), 'exercise': $scope.exercise.exercise_id, 'user': user_id };
		Sets.save({update:upd_exercise, id: $rootScope.editSetId,}, function() {
			$scope.event();
		});
	}

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
		startingDay: 7
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
}])

app.controller('AddDayTrainingController', [
				'$scope', '$rootScope', '$http', 'Categories', 'Exercises', 'AddDay', '$filter', '$modalInstance',
				function($scope, $rootScope, $http, Categories, Exercises, AddDay, $filter, $modalInstance
){
	Categories.query(function(data) {
		$scope.categories = data;
		console.log(data);
	});

	$scope.$watch('cat', function(newVal, oldVal) {
		if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
			Exercises.query({category_id:newVal.category_id}, function(data) {
				$scope.exercises = data;
			});
		}
	});

	$scope.sets = [];
	$scope.addSet = function() {
		$scope.sets.push({weight: $scope.weight, repeats: $scope.repeats});
		console.log('in function' + $scope.sets);
		$scope.weight = null;
		$scope.repeats = null;
		return $scope.sets
	};

	$scope.training = [];
	$scope.addExercise = function() {
		$scope.training.push({date:$filter('date')($scope.date, 'yyyy-MM-dd'), exercise: $scope.exercise.exercise_id, exercise_name: $scope.exercise.name, repeats: $scope.sets, user: user_id});
		$scope.exercise = null;
		$scope.sets = [];
	};

	$scope.cancel = function() {
		$modalInstance.close();
	};

	$scope.submit = function() {
		AddDay.save({add: $scope.training}, function() {
			$rootScope.$broadcast('dayAdded');
			$scope.cancel();
		});
	};

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
		startingDay: 7
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

app.controller('LoginController', [
				'$scope', '$http', '$log', '$location', '$rootScope',
				function($scope, $http, $log, $location, $rootScope
) {
	$scope.submit = function() {
		var inData = { login: $scope.user };
		$http.post('/login/', angular.toJson(inData))
		.success(function(data, status) {
			$log.debug(data);
			$rootScope.$broadcast('userIn');
			$location.path('#/');
		})
		.error(function(data, status) {
			if (status == '404') { $scope.error = data['error']; }
			if (status == '403') { $scope.error = data['auth']; }
		});
	}
}]);

app.controller('LogoutController', [
				'$http', '$location', '$log', '$rootScope',
				function($http, $location, $log, $rootScope
) {
	$http.post('/logout/')
		.success(function() {
			$log.debug('logout success');
			$rootScope.$broadcast('userOut')
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
