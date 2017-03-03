var routeApp = angular.module('quiz',[ui.router]);
routeApp.config(['$stateProvider',function($stateProvider){

    var home = {
        name : 'login',
        url: '/quiz/login',
        templateUrl: "login.html"
    },
    profile ={
        name: 'profile',
        url: '../profile',
        templateUrl: "profile.html"
    };

    $stateProvider.state(home);
    $stateProvider.state(profile);
}])
.run(['$state',function($state){
    $state.transitionTo('home');
}])
.controller('navigationCtrl',function($scope,$state){
    $scope.setPage = function($page){
        $state.transitionTo(page);
    };
})