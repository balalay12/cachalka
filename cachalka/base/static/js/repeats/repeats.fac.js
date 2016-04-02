(function() {

    'use strict';

    angular
        .module('app')
        .factory('repeatsFactory', function($resource) {

            function repeats() {
                return $resource('/api/repeats/');
            }

            return {
                repeats: repeats
            }
        });
})();