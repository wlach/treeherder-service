"use strict";

infra.controller('TotalCtrl', [
    '$state', '$stateParams', '$scope', '$http', '$uibModal', 'dateFilter',
    'thDateFormat',
    function($state, $stateParams, $scope, $http, $uibModal, dateFilter,
             thDateFormat) {
        $http.get('cumulative-try-jobs.json.gz').then(function(response) {
            $scope.cumulativeJobs = response.data;
        });

        $scope.openJobDetail = function(jobDetails) {
            var modalInstance = $uibModal.open({
                templateUrl: 'partials/infra/totaldetailctrl.html',
                controller: 'TotalDetailCtrl',
                size: 'lg',
                resolve: {
                    jobDetails: function() {
                        return jobDetails;
                    }
                }
            });
        };
    }]);

infra.controller('TotalDetailCtrl', [
    '$scope', '$uibModalInstance', 'jobDetails', 'ThResultSetModel',
    function($scope, $uibModalInstance, jobDetails, ThResultSetModel) {
        $scope.jobDetails = jobDetails;
        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        };
        $scope.openJob = function(job) {
            ThResultSetModel.getRevisions(
                'try', job.result_set_id).then(function(revisions) {
                    window.open('index.html#/jobs?repo=try&revision=' + revisions[0] +
                                '&selectedJob=' + job.id + '&group_state=expanded');
                });
        };
    }]);
