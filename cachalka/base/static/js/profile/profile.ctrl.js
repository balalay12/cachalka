(function() {

	"use strict";

	angular
		.module("app")
		.controller("profileCtrl", function($scope, $uibModal, $rootScope, profileFactory, bodySizeFactory) {

			var vm = this;

			vm.addBodySize = addBodySize;
			vm.editBodySize = editBodySize

			profileFactory.userProfile()
				.query({id:user_id}, function(data) {
					vm.user = data[0];
				});

			var bodySizeQuery = function() {
				bodySizeFactory.bodySize()
					.query(function(data) {
						vm.bodySize = data;
					});
			}
			bodySizeQuery();

			$scope.$on("bodySizeEdited", function() {
				bodySizeQuery();
			});

			function addBodySize() {
				$rootScope.bodySizeId = null;
				var addBodySizeModal = $uibModal.open({
					templateUrl: template_dirs + "/bodysize/body_size.html",
					controller: "bodySizeCtrl"
				});
			}

			function editBodySize(id) {
				$rootScope.bodySizeId = id;
				var editBodySizeModal = $uibModal.open({
					templateUrl: template_dirs + "/bodysize/body_size.html",
					controller: "bodySizeCtrl"
				})
			}

		});
})();