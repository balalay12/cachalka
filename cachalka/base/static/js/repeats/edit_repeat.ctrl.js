(function() {

    'use strict';

    angular
        .module('app')
        .controller('editRepeatCtrl', function($scope, $rootScope, $uibModalInstance, repeatsFactory) {

            $scope.adding = false;
            $scope.title = 'Изменить подход';

            repeatsFactory.repeats()
                .query({id: $rootScope.editRepeatId}, function(data) {
                    $scope.set = data[0];
                });

            $scope.cancel = function() {
                $uibModalInstance.close();
            };

            $scope.submit = function() {
                repeatsFactory.repeats()
                    .save({update: $scope.set, id: $rootScope.editRepeatId}, function() {
                        $rootScope.$broadcast('setsChanged');
                        $scope.cancel();
                    })
            };

            $scope.delete = function() {
                repeatsFactory.repeats()
                    .delete({id: $rootScope.editRepeatId}, function() {
                        $rootScope.$broadcast('setsChanged');
                        $scope.cancel();
                    });
            }
        });
})();