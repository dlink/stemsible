(function(){
    var app = angular.module('talkApp', []);

    // Controllers

    app.controller('messageCtrl', ['$scope', '$http', function($scope, $http) {

        $http.get('/api/messages')
            .success(function(data) {
                console.log('http succeeded');
                $scope.messages = data.messages;
            })
            .error(function(data) {
                console.log('http failed');
                $scope.messages = [];
            });

        $scope.new_message = {text: ''};

        $scope.update = function() {
            d = new Date();
            $scope.new_message.created = d.toString();
            $scope.new_message.author = "David Link";
            $scope.messages.unshift($scope.new_message);

            // write back to server
            var rec = {user_id: 1, // hard coded user
                       text: $scope.new_message.text}
            $http.post('/api/messages', rec)
                .success(function(data) {
                    console.log('http post succeeded');
                    console.log(data);
                })
                .error(function(data) {
                    console.log('http post failed.');
                });

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

})();
