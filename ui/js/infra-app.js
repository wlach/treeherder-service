"use strict";

// configure the router here, after we have defined all the controllers etc
infra.config(function($compileProvider, $httpProvider, $stateProvider, $urlRouterProvider) {
    // Disable debug data, as recommended by https://docs.angularjs.org/guide/production
    $compileProvider.debugInfoEnabled(false);

    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.useApplyAsync(true);

    $stateProvider
        .state('last-finished', {
            title: 'Last finished',
            templateUrl: 'partials/infra/lastctrl.html',
            url: '/last-finished',
            controller: 'LastFinishedCtrl'
        })
        .state('total', {
            title: 'Total',
            templateUrl: 'partials/infra/totalctrl.html',
            url: '/total',
            controller: 'TotalCtrl'
        });

    $urlRouterProvider.otherwise('/last-finished');
}).run(['$rootScope', '$state', '$stateParams',
        function ($rootScope, $state, $stateParams) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
        }]);
