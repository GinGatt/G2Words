(function () {
  'use strict';
  angular.module('WordFrequencyAndLocationApp', [])
    .controller('WordFrequencyAndLocationController', ['$scope', '$log', '$http', '$timeout',
      function($scope, $log, $http, $timeout) {
        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.getResults = function() {
          $log.log('test');
          $http.post('/start', {}).then(function(results) {
            $log.log("HEY", results.data);
            // getFrequencyAndLocation(results.data);
            $scope.wordTree = null;
            $scope.loading = true;
            $scope.submitButtonText = 'Loading...';
          }).catch(function(error) {
            $log.log(error);
          });
        };

        // function getFrequencyAndLocation(jobID) {
        //   var timeout = '';
        //   var poller = function() {
        //     // fire followup request, once results calc in background
        //     $http.get('/results/'+jobID).then(function(data) {
        //       console.log(data);
        //       if(data.status === 204) {
        //         $log.log(data);
        //       } else if (data.status === 200){
        //         $log.log(data);
        //         $scope.loading = false;
        //         $scope.submitButtonText = "Submit";
        //         $scope.wordTree = data;
        //         $timeout.cancel(timeout);
        //         return false;
        //       }
        //       // poll until 2 sec timeout
        //       timeout = $timeout(poller, 30000);
        //     }).catch(function(error) {
        //       $log.log(error);
        //       $scope.loading = false;
        //       $scope.submitButtonText = "Submit";
        //     });
        //   };
        //   poller();
        // }
      }])

    // .directive('wordCountTable', ['$parse', function ($parse) {
    //   return {
    //     restrict: 'E',
    //     replace: true,
    //     template: '<div id="chart"></div>',
    //     link: function (scope) {
    //       scope.$watch('wordcounts', function() {
    //         d3.select('#chart').selectAll('*').remove();
    //         var data = scope.wordcounts;
    //         for (var word in data) {
    //           d3.select('#chart')
    //             .append('div')
    //             .selectAll('div')
    //             .data(word[0])
    //             .enter()
    //             .append('div')
    //             .style('width', function() {
    //               return (data[word] * 20) + 'px';
    //             })
    //             .text(function(d){
    //               return word;
    //             });
    //         }
    //       }, true);
    //     }
    //   };
    // }]);

}());
