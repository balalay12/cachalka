(function() {

	"use strict";

	angular
		.module("app")
		.factory("profileFactory", function($resource) {
			
			function userProfile() {
				return $resource("/api/profile/");
			}

			return {
				userProfile: userProfile
			}
		});
})();