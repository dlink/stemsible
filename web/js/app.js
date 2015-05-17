(function(){
    var app = angular.module('talkApp', []);

    // Controllers

    app.controller('messageController', function() {
	this.messages = message_model;

	this.new_message = {text: ''};

	this.update = function() {
	    this.messages.push(this.new_message);
	};
    });

    // Directives

    app.directive('headerSection', function() {
	return {
	    restrict: 'E',
	    templateUrl: 'header-section.html'
	};
    });

    app.directive('newMessage', function() {
	return {
	    restrict: 'E',
	    templateUrl: 'new-message.html'
	};
    });

    app.directive('messages', function() {
	return {
	    // template: '{{x}}'
	     restrict: 'E',
	    templateUrl: 'messages.html',
	};
    });

    message_model = [
	{'id': 1,
	 'author': 'Jill Garner',
	 'created': '2015-05-17 11:01:00',
	 'text': "What's up with LCPS closing every other day?? I've had enough of this stuff"},
	{'id': 2,
	 'author': 'Nidhi Mishra',
	 'created': '2015-05-17 10:39:01',
	 'text': 'There is an awesome STEM event in One Loudoun that you may want to check out. Here is the info ...'}
    ];

})();
