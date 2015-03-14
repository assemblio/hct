jQuery(function ($) {
	var LOGINMODAL = {
		container: null,
		init: function () {
			$("input.login, a.login").click(function (e) {
				e.preventDefault();	

				$("#login-modal-content").modal({
					overlayId: 'login-overlay',
					containerId: 'login-container',
					closeHTML: null,
					minHeight: 80,
					opacity: 65, 
					position: ['0',],
					overlayClose: true,
					onOpen: LOGINMODAL.open,
					onClose: LOGINMODAL.close
				});
			});
		},
		open: function (d) {
			var self = this;
			self.container = d.container[0];
			d.overlay.fadeIn('slow', function () {
				$("#login-modal-content", self.container).show();
				var title = $("#login-modal-title", self.container);
				title.show();
				d.container.slideDown('slow', function () {
					setTimeout(function () {
						var h = $("#login-modal-data", self.container).height()
							+ title.height()
							+ 20; // padding
						d.container.animate(
							{height: h}, 
							200,
							function () {
								$("div.close", self.container).show();
								$("#login-modal-data", self.container).show();
							}
						);
					}, 300);
				});
			})
		},
		close: function (d) {
			var self = this; // this = SimpleModal object
			d.container.animate(
				{top:"-" + (d.container.height() + 20)},
				500,
				function () {
					self.close(); // or $.modal.close();
				}
			);
		}
	};

	LOGINMODAL.init();

});