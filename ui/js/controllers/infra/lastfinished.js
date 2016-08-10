"use strict";

infra.controller('LastFinishedCtrl', [
    '$state', '$stateParams', '$scope', '$http', '$uibModal', 'dateFilter',
    'thDateFormat',
    function($state, $stateParams, $scope, $http, $uibModal, dateFilter,
             thDateFormat) {
        $http.get('last-try-jobs.json').then(function(response) {

            // convert the dates to treeherder format
            $scope.lastJobs = _.map(response.data, function(lastJobDict) {
                lastJobDict.jobs = _.map(lastJobDict.jobs, function(job) {
                    job.submit_timestamp = dateFilter(
                        new Date(job.submit_timestamp), thDateFormat);
                    return job;
                });
                return lastJobDict;
            });

            console.log($scope.lastJobs);
            $scope.openLastJobDetail = function(lastJob) {
                var modalInstance = $uibModal.open({
                    templateUrl: 'partials/infra/lastdetailctrl.html',
                    controller: 'LastFinishedDetailCtrl',
                    size: 'lg',
                    resolve: {
                        lastJob: function() {
                            return lastJob;
                        }
                    }
                });
            };
        });
    }]);

infra.controller('LastFinishedDetailCtrl', [
    '$scope', '$uibModalInstance', 'lastJob', 'ThResultSetModel',
    function($scope, $uibModalInstance, lastJob, ThResultSetModel) {
        $scope.lastJob = lastJob;
        $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
        };
        $scope.openJob = function(job) {
            ThResultSetModel.getRevisions(
                'try', job.result_set_id).then(function(revisions) {
                    window.open('index.html#/jobs?repo=try&revision=' + revisions[0] +
                                '&selectedJob=' + job.id);
                });
        }
    }]);
