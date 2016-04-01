(function() {

	"use strict";

	angular
		.module("app")
		.factory("bodySizeFactory", function($resource) {

			function bodySize() {
				return $resource("/api/bodysize/");
			}

			return {
				bodySize: bodySize
			}
		});
})();