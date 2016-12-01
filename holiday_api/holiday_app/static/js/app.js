(function () {
    //'use strict';

    function b64EncodeUnicode(str) {
        return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, function(match, p1) {
            return String.fromCharCode('0x' + p1);
        }));
    }

    var HolidayApp = angular.module('holiday_app', [
        'ngSanitize',
        'ngResource',
    ]);

    HolidayApp.factory('Users', ['$resource', '$rootScope', function ($resource, $rootScope) {
        return $resource($rootScope.restUrl + 'user/:userId', {}, {
            options: {method: 'OPTIONS', params: {format: 'json'}},
            update: {
                method: 'PUT',
                headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
            },
        });
    }]).factory('Recipients', ['$resource', '$rootScope', function ($resource, $rootScope) {
        return $resource($rootScope.restUrl + 'recipient/:recipientId', {}, {
            options: {method: 'OPTIONS', params: {format: 'json'}},
            update: {
                method: 'PUT',
                headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
            },
        });
    }]).factory('Gifts', ['$resource', '$rootScope', function ($resource, $rootScope) {
        return $resource($rootScope.restUrl + 'recipient/:recipientId/gift/:giftId', {}, {
            options: {
                method: 'OPTIONS',
                params: {format: 'json'}
            },
            update: {
                method: 'PUT',
                headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}
            },
        });
    }]);

    HolidayApp.config(function() {});

    /* App.run, lets you initialize global stuff. */
    HolidayApp.run(function($rootScope, $http) {

        $rootScope.loggedin = false;
        $rootScope.restUrl = '/api/v1/';

        $rootScope.setToken = function(token) {
            if (token) {
                $rootScope.token = token;
                localStorage.setItem('token', token);
                $http.defaults.headers.common['Authorization'] = "Token " + token;
            }
        };

        $rootScope.clearAuth = function() {
            delete $rootScope.token;
            localStorage.removeItem('token');
            delete $http.defaults.headers.common['Authorization'];

            delete $rootScope.user;
            localStorage.removeItem('user');
        }

        $rootScope.setUser = function(user) {
            if (user) {
                $rootScope.user = user;
                localStorage.setItem('user', JSON.stringify(user));
            }
        }

        $rootScope.setToken(localStorage.getItem('token'));
        $rootScope.setUser(JSON.parse(localStorage.getItem('user')));
    });

    HolidayApp.controller('indexController',
                          ['$rootScope', '$scope', '$http',
                           '$location', '$window', '$q',
                           'Recipients', 'Gifts', 'Users',
                           function($rootScope, $scope, $http,
                                    $location, $window, $q,
                                    Recipients, Gifts, Users) {

        $scope.config = {recipient: {}, gift: {}};

        var initializer = function() {
            /* ugly code here... should be elsewhere! */
            $scope.recipients = Recipients.query();

            Recipients.options().$promise
                .then(function(result) {
                    angular.copy(result.actions.POST, $scope.config.recipient);
                    angular.copy(result.actions.POST.gifts.child, $scope.config.gift);

                    var choices = [];

                    // just to clean it up, i was doing status.value in the ng-options but then it wasn't initializign
                    // correctly from the simpler ng-model value.
                    angular.forEach($scope.config.gift.children.status.choices, function(option) {
                        choices.push(option.value);
                    });

                    $scope.config.gift.children.status.choices = choices;
                });
        }

        /* hmm. */
        initializer();

        /* should use routes or states for this, it'd be cleaner. */
        $scope.tryLogin = function() {
            var u = $scope.username;
            var p = $scope.password;

            $http({
                url: '/auth/login/',
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + b64EncodeUnicode(u + ':' + p)
                }
            }).then(function success(response) {
                console.log('Logged in!', new Date());
                console.log('response: ' + JSON.stringify(response));

                $rootScope.loggedin = true;
                $rootScope.setUser(response.data.user);
                $rootScope.setToken(response.data.token);

                initializer();
            });
        };

        $scope.createRecipient = function() {
            var nrecipient = {
                giver: $rootScope.user.id,
                name: $scope.recipients[0].name,
                relation: $scope.recipients[0].relation,
            };

            Recipients.save(nrecipient).$promise
                .then(function(result) {
                    $scope.recipients[0] = result;
                });
        }

        $scope.saveGift = function(gift, recipient) {
            var ngift = {
                item: gift.item,
                status: gift.status,
                cost: gift.cost,
                notes: gift.notes,
            };

            if (gift.id === undefined) {
                Gifts.save({recipientId: recipient.id}, ngift).$promise
                    .then(function(result) {
                        recipient.gifts[0] = result;
                    });
            } else {
                /* we need to update the specific one. */
                Gifts.update({recipientId: recipient.id, giftId: gift.id}, ngift).$promise
                    .then(function(result) {
                        for (var i = 0; i < recipient.gifts.length; i++) {
                            if (recipient.gifts[i].id === gift.id) {
                                recipient.gifts[i] = result;
                                break;
                            }
                        }
                    });
            }
        }

        $scope.deleteGift = function(gift_id, recipient) {
            Gifts.delete({recipientId: recipient.id, giftId: gift_id}).$promise
                .then(function(result) {
                    for (var i = 0; i < recipient.gifts.length; i++) {
                        if (recipient.gifts[i].id === gift_id) {
                            recipient.gifts.splice(i, 1);
                            break;
                        }
                    }
                });
        }

        $scope.addGift = function(recipient_id) {
            console.log('recipient_id ' + recipient_id);

            for (var i = 0; i < $scope.recipients.length; i++) {
                if ($scope.recipients[i].id === recipient_id) {
                    if ($scope.recipients[i].gifts.length > 0) {
                        if ($scope.recipients[i].gifts[0].id === undefined) {
                            /* don't let them add multiple empty rows. */
                            return;
                        }
                    }

                    $scope.recipients[i].gifts.unshift({
                        item: '',
                        cost: 0,
                    });

                    break;
                }
            }
        }

        $scope.addRecipient = function() {
            if ($scope.recipients.length > 0) {
                if ($scope.recipients[0].id === undefined) {
                    /* don't let them add multiple empty rows. */
                    return;
                }
            }

            $scope.recipients.unshift({
                name: '',
                gifts: [],
            });
        }

    }]);
})();
