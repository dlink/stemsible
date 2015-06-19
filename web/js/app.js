(function(){
    var app = angular.module('talkApp', []);

    // Controllers

    app.controller('messageCtrl', ['$scope', '$http', function($scope, $http) {

	$http.get('messagesapi.py')
            .success(function(data) {
		console.log('http suceeded');
		$scope.messages = data.messages;
	    })
	    .error(function(data) {
		console.log('http failed.  data = ' + data);
		$scope.messages = [];
	    });

	$scope.new_message = {text: ''};

	$scope.update = function() {
	    d = new Date();
	    $scope.new_message.created = d.toString();
	    // $scope.new_message.author = "David Link";
	    $scope.new_message.author = "David Link";
	    $http.post('messagesapi.py', {'data': $scope.new_message})
		.success(function(data, status, headers, config) {
		    console.log('post successful');
		})
	        .error(function(data, status, headers, config) {
		    console.log('post fail');
		    console.log('data: ' + data);
		    console.log('status: ' + status);
		});

	    $scope.messages.unshift($scope.new_message);

	    // Init
	    $scope.new_message = {text: ''}
	};
    }]);

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
	 'author': 'Fred Barnes',
	 'created': '2015-05-17 10:39:01',
	 'text': 'There is an awesome STEM event in One Loudoun that you may want to check out. Here is the info ...'}
    ];

})();
