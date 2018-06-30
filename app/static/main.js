(function () {
  'use strict';
  angular.module('WordFrequencyAndLocationApp', [])
    .controller('WordFrequencyAndLocationController', ['$scope', '$log', '$http', '$sce',
      function($scope, $log, $http, $sce) {
        $scope.calculateButtonText = 'Calculate';
        $scope.topWords = null;

        $scope.getResults = function() {
          $scope.calculateButtonText = 'Loading...';
          $http.post('/start', {}).then(function(results) {
            $scope.calculateButtonText = 'Calculate';
            $scope.topWords = results.data;
          }).catch(function(error) {
            $log.log(error);
          });
        };

        var fileTableText = '{0}';
        $scope.getFileTableText = function(fileArray){
          return fileTableText.replace('{0}', fileArray.toString()).replace(/,/g, ", ");
        };

        var sentenceTableText = '{0}';
        $scope.getSentenceTableText = function(sentenceArray){
          return sentenceTableText.replace('{0}', sentenceArray.toString()).replace(/,/g, ", ");
        };

        $scope.bold = function(textToSearch, searchTerm) {
          if (!searchTerm) {
            return $sce.trustAsHtml(textToSearch);
          }
          var newText = textToSearch.replace(new RegExp("\\b" + searchTerm + "\\b", 'gi'), "<span class='boldedText'>$&</span>");
          return $sce.trustAsHtml(newText);
        }
      }])
}());
