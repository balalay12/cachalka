(function() {

	'use strict';

	angular
		.module('app')
		.controller('editExerciseCtrl', function($scope, $rootScope, $filter, $uibModalInstance, categoryFactory, exerciseFactory, setsFactory) {

			categoryFactory.categories()
				.query(function(data) {
					$scope.categories= data;
				});

			setsFactory.query({id: $rootScope.editSetId}, function(data) {
				$scope.cat = {category_id:data[0].items.category_id, name:data[0].items.category_name};
				$scope.exercise = {exercise_id: data[0].exercise, name:data[0].items.exercise_name};
				$scope.date = new Date(data[0].date);
			});

			$scope.$watch('cat', function(newVal, oldVal) {
				if(angular.isDefined(oldVal) | angular.isDefined(newVal)) {
					exerciseFactory.exercises()
						.query({category_id:newVal.category_id}, function(data) {
							$scope.exercises = data;
						});
				}
			});

			$scope.cancel = function() {
			    $uibModalInstance.close();
			};

			$scope.delete = function() {
			    setsFactory.delete({id: $rootScope.editSetId}, function() {
			        // $scope.event();
			        console.log('deleted');
			    });
			};

			$scope.submit = function() {
				var upd_exercise = {'date': $filter('date')($scope.date, 'yyyy-MM-dd'), 'exercise': $scope.exercise.exercise_id, 'user': user_id };
				setsFactory.save({update:upd_exercise, id: $rootScope.editSetId,}, function() {
					// $scope.event();
					console.log('updated');
				});
			}

		});
})();