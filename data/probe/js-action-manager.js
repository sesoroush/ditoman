mydnnBusinessDirectoryApp.service('actionManagerService', function ($q, $rootScope, $timeout, $filter, $parse, panelService) {
    var actionManager = this;
    const scriptTemplate =
        'window["preActionScript[ACTION-ID]"] = function($scope,$q) { \n\
            var defer = $q.defer(); \n\
            try { \n\
                [SCRIPT-CONTENT] \n\
                //{SCRIPT-DONE} \n\
            } catch (e) { \n\
                defer.resolve(0,e); \n\
            } \n\
            return defer.promise; \n\
        }';


    this.callActionsByEvent = function ($scope, event, actions, filterActions) {
        var currentActions = [];
        if (filterActions)
            currentActions = $filter('filter')(filterActions, function (a) { return a.Event == event });
        else if (actions)
            currentActions = $filter('filter')(actions, function (a) { return a.Event == event });

        angular.forEach($filter('orderBy')(currentActions, 'ViewOrder'), function (action) {
            actionManager.callAction($scope, action).then(function (type) {
                actionManager.callActionsOnCompletedAction($scope, action, actions, type);
            });
        });
    }

    this.callActionByActionID = function ($scope, actionID, params) {
        var actions = $filter('filter')($scope.allActions, function (a) { return a.ActionID == actionID });
        if (actions.length) {
            actions[0].Params = params;
            actionManager.callActionsByEvent($scope, actions[0].Event, $scope.allActions, actions);
        }
    }

    this.callActionByName = function ($scope, actionName, params) {
        var actions = $filter('filter')($scope.allActions, function (a) { return a.ActionName == actionName });
        if (actions.length) {
            actions[0].Params = params;
            actionManager.callActionsByEvent($scope, actions[0].Event, $scope.allActions, actions);
        }
    }

    this.callActionsOnCompletedAction = function ($scope, action, actions, resultType) {
        var conditionalActions = $filter('filter')(actions, function (a) { return a.ParentID == action.ActionID && (a.ParentResultMode == 0 || a.ParentResultMode == resultType) });
        actionManager.callActionsByEvent($scope, 'OnActionCompleted', actions, conditionalActions);
    }

    this.callAction = function ($scope, action) {
        var defer = $q.defer();

        if (!action) defer.reject();

        try {
            for (let key in action.Params) {
                $scope['MBDAP_' + key] = typeof action.Params[key] == 'string' ? panelService.getScopePropertyValue($scope, action.Params[key]) : action.Params[key];
            }

            $scope.customActions = $scope.customActions || {};
            $scope.customActions[action.ActionName] = {};

            if (panelService.checkConditions($scope, action.Conditions)) {
                actionManager.execPreOrPostActionScript($scope, action, 1).then(function () {
                    actionManager[action.ActionType]($scope, action).then(function (type) {
                        actionManager.execPreOrPostActionScript($scope, action, 2).then(function () {
                            defer.resolve(type);
                        });
                    });
                });
            }
        } catch (e) {
            defer.reject(e);
        }

        return defer.promise;
    }

    actionManager['SetProperty'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            panelService.setPropertiesValue($scope, action.ActionDetails.Properties);

            defer.resolve(1);

        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['ValidateForm'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            $scope.validateForm();

            defer.resolve(1);
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['ValidateField'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            var field = $scope.getFieldByID(action.ActionDetails.FieldID);
            $scope.validateField(field);

            defer.resolve();
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['DashboardRedirectPage'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            $scope.onPageClick(panelService.getScopePropertyValue($scope, action.ActionDetails.PageName), panelService.getScopePropertyValue($scope, action.ActionDetails.PageParams), true);

            defer.resolve();
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['RunJavascript'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            var newScript = document.createElement('script');
            newScript.innerHTML = panelService.getScopePropertyValue($scope, action.ActionDetails.Code);
            $('body').append(newScript);

            defer.resolve(1);
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['RedirectUrl'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            var url = panelService.getScopePropertyValue($scope, action.ActionDetails.Url);
            location.href = url;

            defer.resolve(1);
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['RunService'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            isPromise = true;

            var currentService = action.ActionDetails || {};

            var params = {};
            angular.forEach(currentService.Params, function (p) {
                params[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            $scope.waiting = true;
            panelService.runService($scope, action.ServiceID, params).then(function (r) {
                $scope.waiting = false;

                var result = r.Data;
                if (result && typeof result == 'object') {
                    panelService.parseJsonItems(result);
                }

                $scope.customActions[action.ActionName].Data = result;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = false;
                $scope.customActions[action.ActionName].IsSuccess = true;

                if (currentService.OnCompleted) {
                    $filter('filter')(currentService.OnCompleted, function (p) { return p.FieldValue }).map(function (property) {
                        property.FieldValue = property.FieldValue.replace('{ServiceResult', '{customActions.' + action.ActionName + '.Data');
                    });
                }

                panelService.setPropertiesValue($scope, currentService.OnCompleted);

                defer.resolve(1);
            }, function (error) {
                $scope.waiting = false;

                $scope.customActions[action.ActionName].Data = error.data.Data;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = true;

                if (currentService.OnCompleted) {
                    $filter('filter')(currentService.OnCompleted, function (p) { return p.FieldValue }).map(function (property) {
                        property.FieldValue = property.FieldValue.replace('{ServiceResult', '{customActions.' + action.ActionName + '.Data');
                    });
                }
                panelService.setPropertiesValue($scope, currentService.OnCompleted);

                defer.resolve(2);
            });
        }
        catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['SubmitEntity'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            isPromise = true;

            var submitEntityService = action.ActionDetails || {};

            var submitEntityServiceParams = {};
            angular.forEach(submitEntityService.Params, function (p) {
                submitEntityServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            $scope.waiting = true;
            panelService.runService($scope, action.ServiceID, submitEntityServiceParams).then(function (r) {
                $scope.waiting = false;

                var result = r.Data;
                if (result && typeof result == 'object') {
                    panelService.parseJsonItems(result);
                }

                $scope.customActions[action.ActionName].Data = result;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = false;
                $scope.customActions[action.ActionName].IsSuccess = true;

                var ds = panelService.getScopeProperty($scope, action.ActionDetails.ResultName);
                if (ds) ds.assign($scope, result);

                defer.resolve(1);
            }, function (error) {
                $scope.waiting = false;

                $scope.customActions[action.ActionName].Data = error.data.Data;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = true;

                defer.resolve(2);
            });
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['GetDataRow'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            isPromise = true;

            var dataRowService = action.ActionDetails || {};

            var dataRowServiceParams = {};
            angular.forEach(dataRowService.Params, function (p) {
                dataRowServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            $scope.waiting = true;
            panelService.runService($scope, action.ServiceID, dataRowServiceParams).then(function (r) {
                $scope.waiting = false;

                var result = r.Data;
                if (result && typeof result == 'object') {
                    panelService.parseJsonItems(result);
                }

                $scope.customActions[action.ActionName].Data = result;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = false;
                $scope.customActions[action.ActionName].IsSuccess = true;

                var ds = panelService.getScopeProperty($scope, action.ActionDetails.ResultName);
                if (ds) ds.assign($scope, result);

                defer.resolve(1);
            }, function (error) {
                $scope.waiting = false;

                $scope.customActions[action.ActionName].Data = error.data.Data;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = true;

                defer.resolve(2);
            });
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['GetListDataSource'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            isPromise = true;

            var dataSourceService = action.ActionDetails || {};

            var dataSourceServiceParams = {};
            angular.forEach(dataSourceService.Params, function (p) {
                dataSourceServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            $scope.waiting = true;
            panelService.runService($scope, action.ServiceID, dataSourceServiceParams).then(function (r) {
                $scope.waiting = false;

                var result = r.Data;
                if (result && typeof result == 'object') {
                    panelService.parseJsonItems(result);
                }

                $scope.customActions[action.ActionName].Data = result;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = false;
                $scope.customActions[action.ActionName].IsSuccess = true;

                var ds = panelService.getScopeProperty($scope, action.ActionDetails.ResultListName);
                if (ds) ds.assign($scope, result);

                if (result) {
                    var ds1 = panelService.getScopeProperty($scope, action.ActionDetails.TotalCountIn);
                    if (ds1) ds1.assign($scope, result.length ? result[0].bEngine_TotalCount : 0);
                }

                defer.resolve(1);
            }, function (error) {
                $scope.waiting = false;

                $scope.customActions[action.ActionName].Data = error.data.Data;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = true;

                defer.resolve(2);
            });

        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['Payment'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            var amount = action.ActionDetails.Amount = panelService.getScopePropertyValue($scope, action.ActionDetails.Amount);

            var paymentParams = {
                PaymentMethodID: action.ActionDetails.PaymentMethodID,
                PaymentGateway: action.ActionDetails.PaymentGateway,
                Amount: amount,
                PortalID: mydnnBusinessDirectoryGlobal.portalID,
                ModuleID: $scope.moduleID,
                moduleID: $scope.moduleID,
                AjaxHeader: $scope.ajaxHeaders
            };

            angular.forEach(action.ActionDetails.PaymentParams, function (p) {
                paymentParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            location.href = mydnnBusinessDirectoryGlobal.modulePath + 'PaymentGateway/Send.aspx?q=' + panelService.encode64(JSON.stringify(paymentParams));

            defer.resolve(1);
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['CallAnotherAction'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            var allActions = angular.copy($scope.actions);
            if ($scope.fields && $scope.fields.length)
                $scope.fields.map(function (f) {
                    if (f.Actions && f.Actions.length) allActions = allActions.concat(f.Actions);
                });

            $filter('filter')(allActions, function (a) { return a.ActionID == action.ActionDetails.ActionID }).map(function (a) {
                var anotherAction = angular.copy(a);
                anotherAction.Event = event;
                actionManager.callActionsByEvent($scope, event, allActions, [anotherAction]);
            });

            defer.resolve(1);
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['CallWebService'] = function ($scope, action) {
        var defer = $q.defer();

        try {
            isPromise = true;

            var webServiceParams = {};

            var webService = action.ActionDetails || {};

            angular.forEach(webService.UrlParams, function (p) {
                webServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            angular.forEach(webService.Params, function (p) {
                webServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            angular.forEach(webService.HeaderParams, function (p) {
                webServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            angular.forEach(webService.BodyParams, function (p) {
                webServiceParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            $scope.waiting = true;
            panelService.runService($scope, action.ServiceID, webServiceParams).then(function (r) {
                $scope.waiting = false;

                var result = r.Data;
                if (result && typeof result == 'object') {
                    panelService.parseJsonItems(result);
                }

                $scope.customActions[action.ActionName].Data = result;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = false;
                $scope.customActions[action.ActionName].IsSuccess = true;

                if (webService.OnCompleted) {
                    $filter('filter')(webService.OnCompleted, function (p) { return p.FieldValue }).map(function (property) {
                        property.FieldValue = property.FieldValue.replace('{ServiceResult', '{customActions.' + action.ActionName + '.Data');
                    });
                }

                panelService.setPropertiesValue($scope, webService.OnCompleted);

                defer.resolve(1);
            }, function (error) {
                $scope.waiting = false;

                $scope.customActions[action.ActionName].Data = error.data.Data;
                $scope.customActions[action.ActionName].IsCompleted = true;
                $scope.customActions[action.ActionName].IsError = true;

                if (webService.OnCompleted) {
                    $filter('filter')(webService.OnCompleted, function (p) { return p.FieldValue }).map(function (property) {
                        property.FieldValue = property.FieldValue.replace('{ServiceResult', '{customActions.' + action.ActionName + '.Data');
                    });
                }

                panelService.setPropertiesValue($scope, webService.OnCompleted);

                defer.resolve(2);
            });
        } catch (e) {
            defer.resolve(2);
        }

        return defer.promise;
    }

    actionManager['ListProcessing'] = function ($scope, action) {
        var defer = $q.defer();

        var lpService = action.ActionDetails || {};

        if (action.ActionDetails.ActionType == 'SetProperty') {
            angular.forEach(action.ActionDetails.PropertiesBeforeListProcessing, function (property) {
                var propertyStr = property.Condition ? property.Condition : '';
                var model = panelService.getScopeProperty($scope, propertyStr);

                var propertyValue = panelService.getScopePropertyValue($scope, property.FieldValue);

                if (model) model.assign($scope, propertyValue);
            });
        }

        var list = panelService.evalateToken(panelService.getScopePropertyValue($scope, action.ActionDetails.ListName));
        var listItemCount = list ? list.length : 0;
        var index = 0;
        angular.forEach(list, function (lpListItem) {
            $scope['LP_' + action.ActionDetails.ListItemName] = lpListItem;

            if (action.ActionDetails.ActionType == 'RunService') {
                isPromise = true;

                var lpParams = {};
                angular.forEach(lpService.Params, function (p) {
                    if (p.ParamValue && p.ParamValue.indexOf('LP_') == -1) p.ParamValue = p.ParamValue.replace(lpService.ListItemName, 'LP_' + lpService.ListItemName);

                    lpParams[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
                });

                $scope.waiting = true;
                panelService.runService($scope, action.ServiceID, lpParams).then(function (r) {
                    $scope.waiting = false;

                    var result = r.Data;
                    if (result && typeof result == 'object') {
                        panelService.parseJsonItems(result);
                    }

                    angular.forEach(lpService.OnServiceCompleted, function (property) {
                        $scope['LP_' + action.ActionDetails.ListItemName] = lpListItem;

                        var indx = panelService.getScopeProperty2($scope, action.ActionDetails.ListName).indexOf($scope['LP_' + lpService.ListItemName]);

                        var listName = /{?(.[^}]+)}?/.exec(action.ActionDetails.ListName)[1];
                        var propertyStr = property.Condition ? property.Condition : '';
                        propertyStr = propertyStr.replace(new RegExp(lpService.ListItemName, 'g'), listName + '[' + indx + ']');

                        var model = panelService.getScopeProperty($scope, propertyStr);

                        var val = property.FieldValue ? property.FieldValue.toString().replace('{ServiceResult}', result) : '';
                        var propertyValue = panelService.getScopePropertyValue($scope, val);

                        if (model) model.assign($scope, propertyValue);
                    });

                    if (++index >= listItemCount) actionManager.callActionsByEventOnCompletedAction($scope, action, actions, 1);
                }, function (error) {
                    $scope.waiting = false;

                    if (++index >= listItemCount) actionManager.callActionsByEventOnCompletedAction($scope, action, actions, 2);
                });
            }
            else if (action.ActionDetails.ActionType == 'SetProperty') {
                angular.forEach(action.ActionDetails.PropertiesIntoListProcessing, function (property) {
                    var fieldValue = property.FieldValue;
                    fieldValue = fieldValue || '';
                    fieldValue = fieldValue.replace(new RegExp(lpService.ListItemName, 'g'), 'LP_' + lpService.ListItemName);

                    var propertyStr = property.Condition ? property.Condition : '';
                    propertyStr = propertyStr.replace(new RegExp(lpService.ListItemName, 'g'), 'LP_' + lpService.ListItemName);

                    var model = panelService.getScopeProperty($scope, propertyStr);

                    var propertyValue = panelService.getScopePropertyValue($scope, fieldValue);

                    if (model) model.assign($scope, propertyValue);

                    if (++index >= listItemCount) actionManager.callActionsByEventOnCompletedAction($scope, action, actions, 1);
                });
            }
        });

        defer.resolve();

        return defer.promise;
    }

    actionManager['SendEmail'] = function ($scope, action) {
        var defer = $q.defer();
        action.ActionDetails.EmailTo = panelService.getScopePropertyValue($scope, JSON.stringify(action.ActionDetails.EmailTo));
        action.ActionDetails.Subject = panelService.getScopePropertyValue($scope, action.ActionDetails.Subject);
        action.ActionDetails.Body = panelService.getScopePropertyValue($scope, action.ActionDetails.Body);

        var $obj = $('<div>' + action.ActionDetails.Body + '</div>');
        $compile($obj.contents())($scope);

        $timeout(function () {
            action.ActionDetails.Body = $obj.html();

            panelService.ajax({
                method: 'POST',
                url: mydnnBusinessDirectoryGlobal.serviceUrl + 'Service/CallAction',
                headers: $scope.ajaxHeaders,
                data: action
            }).then(function (data) {
            });

        }, 500);

        defer.resolve();

        return defer.promise;
    }

    actionManager['CallActionFromAnotherModule'] = function ($scope, action) {
        var defer = $q.defer();
        var moduleName = action.ActionDetails.ModuleName;
        var actionName = action.ActionDetails.ActionName;
        var actionParams = action.ActionDetails.ActionParams;

        $filter('filter')(bEngineModules, function (m) { return m.ModuleName == moduleName }).map(function (module) {
            var params = {};
            angular.forEach(actionParams, function (p) {
                params[p.ParamName] = panelService.getScopePropertyValue($scope, p.ParamValue);
            });

            var $moduleScope = angular.element(document.getElementById('pnlBusinessDirectory' + module.ModuleID)).scope();

            $moduleScope.callAction(actionName, params);
            $moduleScope.$apply();
        });

        defer.resolve();

        return defer.promise;
    }

    actionManager['SetPageParams'] = function ($scope, action) {
        var defer = $q.defer();
        var pageParams = [];
        var paramName;
        var paramValue;

        angular.forEach(action.ActionDetails.PageParams, function (property) {
            paramName = property.Condition ? property.Condition : '';
            paramValue = panelService.getScopePropertyValue($scope, property.FieldValue);

            pageParams.push(paramName + '=' + paramValue);
        });
        $timeout(function () {
            $window.history.pushState({ pageTitle: document.title }, '', panelService.updateURLParameter(document.URL, paramName, paramValue));
        });

        defer.resolve();

        return defer.promise;
    }

    this.execPreOrPostActionScript = function ($scope, action, type) {
        var scriptStr = scriptTemplate;

        var actionScript = type == 1 ? (action.ActionDetails.PreScript || '') : (action.ActionDetails.PostScript || '');

        if (actionScript.indexOf('//{SCRIPT-DONE}') >= 0) scriptStr = scriptStr.replace('//{SCRIPT-DONE}', '');

        scriptStr = scriptStr.replace('[ACTION-ID]', action.ActionID);
        scriptStr = scriptStr.replace('[SCRIPT-CONTENT]', actionScript);
        scriptStr = scriptStr.replace('//{SCRIPT-DONE}', 'defer.resolve()');

        var newScript = document.createElement('script');
        newScript.innerHTML = scriptStr;
        $('body').append(newScript);

        return window['preActionScript' + action.ActionID]($scope, $q);
    }
});