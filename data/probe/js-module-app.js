if (typeof mydnnBusinessDirectoryApp == 'undefined') {
    var mydnnBusinessDirectoryApp = angular.module('BusinessEngineApp', ['ngSanitize', 'ngFileUpload', 'ui.tree',
        'angular.filter', 'ui.bootstrap', 'selectize', 'select2', 'ngTagsInput', 'mbd-autocomplete', 'ya.nouislider', 'ckeditor','ADM-dateTimePicker']);

    mydnnBusinessDirectoryApp.config(['$httpProvider', '$locationProvider', function ($httpProvider, $locationProvider) {
        $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';

        $locationProvider.html5Mode({ enabled: true, requireBase: false, rewriteLinks: false });
    }]);

    //inject any instance 
    //mydnnBusinessDirectoryApp.run(function ($rootScope, panelService) {
    //    panelService.ajax({
    //        method: 'GET',
    //        url: mydnnBusinessDirectoryGlobal.serviceUrl + 'PublicService/GetLocalResources',
    //    }).then(function (data) {
    //        mydnnBusinessDirectoryGlobal.localResources = data;

    //        $rootScope.$broadcast('localResourceLoadCompleted');
    //    });
    //});

    var mbdAppRegistered = [];

    var bEngineModules = [];
}

$(document).ready(function () {
    setTimeout(function () {
        $('*[mbd-ng-app]').each(function () {
            var id = $(this).attr('id');
            if (mbdAppRegistered.indexOf(id) == -1) {
                angular.bootstrap($(this), ['BusinessEngineApp']);

                mbdAppRegistered.push(id);
            }
        });
    });
});
