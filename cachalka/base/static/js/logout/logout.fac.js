(function() {

	"use strict";

	angular
		.module("app")
		.factory("logoutFactory", function($http) {

			function logout() {

				return $http.post("/logout/");
			}

			return {
				logout: logout
			}
		});
})();