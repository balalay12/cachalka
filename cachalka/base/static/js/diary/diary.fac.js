(function() {

	'use strict';

	angular
		.module('app')
		.factory('setsFactory', function($resource) {

			return $resource('/api/sets/', {}, {
				'getAllSets': {
					method: 'GET',
					isArray: false
				}
			})
		});
})();