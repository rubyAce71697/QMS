var routeApp = angular.module('routeApp',[ui.router]);

routerApp.config(function($stateProvider, $urlRouterProvider){

    $urlRouterProvider.otherwise('/home')

    $stateProvider

        .state(home,{
            url: 'quiz/login',
            templateUrl: 'quiz/login.html'
        })
        
})