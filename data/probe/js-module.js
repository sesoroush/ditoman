mydnnBusinessDirectoryApp.controller('moduleBuilder_ModuleController', function ($scope, $filter, $http, $timeout, $q, $parse, $compile, $window, $templateCache, panelService, actionManagerService) {
    $scope.service = panelService;
    $scope.actionManagerService = actionManagerService;
    $scope.userID = mydnnBusinessDirectoryGlobal.userID;

    $scope.$compile = $compile;
    $scope.$window = $window;
    $scope.$q = $q;

    if (typeof window.matchMedia == 'function') {
        var isMobile = window.matchMedia('screen and (max-width: 768px)');
        $scope.isMobile = isMobile ? isMobile.matches : false;
    }

    $scope.Form = {};
    $scope.Field = {};
    $scope.Data = {};
    $scope.Pane = {};

    var watches = [];

    $scope.onInitModule = function (moduleID, tabID, moduleGuid) {
        $scope.ajaxHeaders = {
            TabId: tabID,
            ModuleId: moduleID,
            ModuleGuid: moduleGuid,
        }

        $scope.moduleID = moduleGuid;
    };

    $scope.onLoadModule = function () {
        var defer = $q.defer();

        $scope.submittedStatus = 0;

        panelService.ajax({
            method: 'POST',
            url: mydnnBusinessDirectoryGlobal.serviceUrl + 'Service/GetModuleData',
            headers: $scope.ajaxHeaders,
            data: { PageUrl: document.URL }
        }).then(function (data) {
            $http.get(data.Template, { cache: $templateCache }).then(function (moduleHtml) {
                $scope.fields = data.Fields;

                $scope.actions = data.Actions;
                angular.forEach($scope.actions, function (a) {
                    panelService.parseJsonItems(a);
                });

                $scope.allActions = angular.copy($scope.actions);
                $scope.fields.map(function (f) { if (f.Actions) $scope.allActions = $scope.allActions.concat(f.Actions); });

                var fieldsWatchesBuffer = [];

                angular.forEach($scope.fields, function (field) {
                    field.Settings = field.Settings || {};
                    panelService.parseJsonItems(field.Settings);

                    if (field.IsValuable) {
                        $scope.manageWatches('{Field.' + field.FieldName + '.Value}', 'onFieldValueChange', field.FieldID);
                        $scope.manageWatches('{Field.' + field.FieldName + '.IsShow}', 'onFieldShowChange', field.FieldID);

                        $scope.setFieldValue(field.FieldID);
                    }

                    $scope.showHideField(field.FieldID);

                    angular.forEach(field.Settings.FieldValues, function (v) {
                        $scope.manageWatches(v.FieldValue, 'setFieldValue', field.FieldID);

                        angular.forEach(v.Conditions, function (c) {
                            $scope.manageWatches(c.LeftExpression, 'setFieldValue', field.FieldID);
                        });
                    });

                    $scope.manageWatches('{Field.[FieldName].IsShow}'.replace('[FieldName]', field.FieldName), 'reInitField', field.FieldID);

                    field.IsShowBackup = field.IsShow;
                    angular.forEach(field.Settings.ShowConditions, function (c) {
                        $scope.manageWatches(c.LeftExpression, 'showHideField', field.FieldID);
                        $scope.manageWatches(c.RightExpression, 'showHideField', field.FieldID);
                    });

                    field.Settings.DataSource = field.Settings.DataSource || {};

                    if (field.Settings.DataSource) {
                        $scope.getFieldDataSource(field.FieldID);

                        if (field.Settings.DataSource.Type == 1) {
                            angular.forEach(field.Settings.DataSource.ListFilters, function (filter) {
                                $scope.manageWatches(filter.RightExpression, 'getFieldDataSource', field.FieldID);
                            });
                        }
                        else if (field.Settings.DataSource.Type == 2) {
                            $filter('filter')($scope.allActions, function (a) { return a.ActionID == field.Settings.DataSource.ActionID }).map(function (action) {
                                field.Settings.DataSource.ResultListName = action.ActionDetails.ResultListName;
                                $scope.manageWatches(action.ActionDetails.ResultListName, 'getFieldDataSource', field.FieldID);
                            });
                        }

                        angular.forEach(field.Options, function (o) {
                            if (o.Settings && o.Settings.Conditions) {
                                o.IsHide = !panelService.checkConditions($scope, o.Settings.Conditions);

                                angular.forEach(o.Settings.Conditions, function (c) {
                                    $scope.manageWatches(c.LeftExpression, 'showHideFieldOptions', field.FieldID);
                                });
                            }
                        });

                        if (field.Settings.ShowAll && !field.Settings.AllowMultiple && field.Options && field.Options.length) {
                            field.Options.splice(0, 0, { OptionText: field.Settings.AllText });
                        }
                    }

                    if (field.Settings.WatchesCallBack) fieldsWatchesBuffer.push(field.Settings.WatchesCallBack);

                    $scope.Field[field.FieldName] = field;
                });

                angular.forEach($scope.actions, function (a) {
                    panelService.parseJsonItems(a);
                });

                raiseWatches();

                defer.resolve($compile(moduleHtml.data)($scope));

                $timeout(function () {
                    if (typeof (window['pageLoad_' + $scope.moduleID]) == 'function') {
                        window['pageLoad_' + $scope.moduleID]($scope);

                        angular.forEach(fieldsWatchesBuffer, function (wFn) {
                            try {
                                var fn = $parse(wFn);
                                fn($scope);
                            } catch (e) {
                                console.error(e);
                            }
                        });

                        raiseWatches();
                    }

                    actionManagerService.callActionsByEvent($scope, 'OnPageLoad', $scope.actions);

                    $timeout(function () {
                        if (!panelService.getParameterByName('b-stay-skeleton')) $('.b-skeleton-loading').remove();
                    }, 1000);
                });
            }, function (error) {
                defer.reject('');
            });
        }, function (error) {
            defer.reject(error);
        });

        return defer.promise;
    };

    /* General Methods */
    $scope.getFieldByID = function (fieldID) {
        var result = $filter('filter')($scope.fields, function (f) { return f.FieldID == fieldID });
        return result.length ? result[0] : null;
    };

    $scope.getFieldByName = function (fieldName) {
        var result = $filter('filter')($scope.fields, function (f) { return f.FieldName == fieldName });
        return result.length ? result[0] : null;
    };

    $scope.setFieldValue = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        if (field.Settings && field.Settings.FieldValues && field.Settings.FieldValues.length) {
            angular.forEach(field.Settings.FieldValues, function (fv) {
                if (!fv.Conditions || !fv.Conditions.length || panelService.checkConditions($scope, fv.Conditions)) {
                    let value = panelService.getScopePropertyValue($scope, fv.FieldValue);

                    if (field.Settings.AllowMultiple && !field.IsJsonValue && value && typeof value != 'object')
                        field.Value = value.toString().split(',');
                    else
                        field.Value = value;//panelService.evalateToken(panelService.getJsonString(value));

                    $scope.Form[field.FieldName] = field.Value;
                }
            });
        }
    };

    $scope.reInitField = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);
        if (field && field.IsShow) {
            $timeout(function () {
                callFieldInitFn(field);

                if (field.IsGroup) $scope.populateGroupFieldsAfterShowPane(field.FieldID);
            });
        }
    };

    $scope.reInitPaneFields = function (paneName) {
        $filter('filter')($scope.fields, function (f) { return f.PaneName == paneName }).map(function (f) {
            $scope.reInitField(f);
        });
    };

    $scope.showHideField = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        if (field.Settings && field.Settings.ShowConditions && field.Settings.ShowConditions.length) {
            field.IsShow = panelService.checkConditions($scope, field.Settings.ShowConditions);

            $scope.reInitField(fieldID);
        }
    };

    $scope.showHideFieldOptions = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        angular.forEach(field.Options, function (o) {
            if (o.Settings && o.Settings.Conditions)
                o.IsHide = !panelService.checkConditions($scope, o.Settings.Conditions);
        });
    };

    $scope.getFieldDataSource = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        var datasource = angular.copy(field.Settings.DataSource);

        if (datasource && datasource.Type == 1) {
            angular.forEach(datasource.ListFilters, function (f) {
                f.RightExpression = panelService.getScopePropertyValue($scope, f.RightExpression);
            });

            panelService.ajax({
                method: 'POST',
                url: mydnnBusinessDirectoryGlobal.serviceUrl + 'Service/GetFieldDataSource',
                headers: $scope.ajaxHeaders,
                data: { FieldID: fieldID, DataSource: datasource }
            }).then(function (data) {
                field.Options = data;

                if (field.Value && $filter('filter')(field.Options, function (o) { return o.OptionValue == field.Value }).length == 0)
                    delete field.Value;

                //if (field.Settings.ShowAll && !field.Settings.AllowMultiple && field.Options && field.Options.length)
                //field.Options.splice(0, 0, { OptionText: field.Settings.AllText });
            });
        }
        else if (datasource && datasource.Type == 2) {
            field.Options = panelService.getScopePropertyValue($scope, field.Settings.DataSource.ResultListName);
        }
    };

    $scope.onFieldValueChange = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        if (field.Settings.SaveValueIn) {
            var match = /^{([^}].+)}$/.exec(field.Settings.SaveValueIn);
            if (match && match.length > 1) {
                var model = $parse(match[1]);
                model.assign($scope, field.Value);
            }
        }
        else
            $scope.Form[field.FieldName] = field.Value;

        if (field.IsValidate) $scope.validateField(field);

        if (field.Actions && field.Actions.length) actionManagerService.callActionsByEvent($scope, 'OnFieldValueChange', field.Actions);
    };

    $scope.onFieldShowChange = function (fieldID) {
        var field = $scope.getFieldByID(fieldID);

        if (!field.Settings.DisableNullValueWhenFieldIsHide && !field.IsShow && field.Value) {
            field.ValueBackup = angular.copy(field.Value);
            delete field.Value;
        }
        else if (!field.Settings.DisableNullValueWhenFieldIsHide && field.IsShow && field.ValueBackup) {
            field.Value = angular.copy(field.ValueBackup);
            delete field.ValueBackup;
        }

        $scope.Form[field.FieldName] = field.Value;
    };

    $scope.validateForm = function () {
        $scope.Form._IsValid = true;
        $filter('filter')($scope.fields, function (f) { return f.IsValuable && isFieldShow(f) }).map(function (field) {
            $scope.validateField(field);

            field.IsPatternValidate = true;

            if (!field.IsValid && field.IsShow) $scope.Form._IsValid = false;
        });
    };

    $scope.validateField = function (field) {
        var isValid = true;

        var fields = !field.IsGroup ? [field] : $filter('filter')($scope.fields, function (f) { return f.ParentID == field.FieldID && f.IsValuable && isFieldShow(f) });
        angular.forEach(fields, function (field) {
            field.IsValidate = true;

            if (field.IsRequired) {
                if (field.Settings.ValidationMethod) {
                    var fn = $parse(field.Settings.ValidationMethod);
                    field.IsValid = fn($scope, { field: field });
                }
                else {
                    field.IsValid = !(field.Value === null || field.Value === undefined || field.Value === '');
                }

                field.RequiredError = !field.IsValid;
            }
            else
                field.IsValid = true;


            if (field.IsValid && field.Value && field.Settings && field.Settings.ValidationPattern) {
                try {
                    field.IsValid = new RegExp(field.Settings.ValidationPattern).test(field.Value);
                } catch (e) {
                    field.IsValid = false;
                }
            }

            if (!field.IsValid) isValid = false;
        });

        if (field.IsGroup) field.IsValid = isValid;
    }

    $scope.validatePane = function (paneName) {
        var isValid = true;

        var fields = [].concat($filter('filter')($scope.fields, function (f) { return f.PaneName == paneName && f.IsShow }));

        $filter('filter')(fields, function (f) { return f.IsGroup }).map(function (g) {
            populateChildFields(g);
        });

        function populateChildFields(group) {
            var childs = $filter('filter')($scope.fields, function (f) { return f.ParentID == group.FieldID && f.IsShow });

            fields = fields.concat(childs);

            $filter('filter')(childs, function (f) { return f.IsGroup }).map(function (g) {
                populateChildFields(g);
            });
        }

        angular.forEach(fields, function (field) {
            field.IsValidate = true;

            if (field.IsRequired) {
                if (field.Settings.ValidationMethod) {
                    var fn = $parse(field.Settings.ValidationMethod);
                    field.IsValid = fn($scope, { field: field });
                }
                else {
                    field.IsValid = !(field.Value === null || field.Value === undefined || field.Value === '');
                }

                field.RequiredError = !field.IsValid;
            }
            else
                field.IsValid = true;

            if (field.IsValid && field.Value && field.Settings && field.Settings.ValidationPattern) {
                try {
                    field.IsValid = new RegExp(field.Settings.ValidationPattern).test(field.Value);
                } catch (e) {
                    field.IsValid = false;
                }
            }

            if (!field.IsValid) isValid = false;
        });

        $scope.Pane[paneName] = { IsValid: isValid }

        $scope.$broadcast('onValidatePane', { PaneName: paneName, IsValid: isValid });
    };

    $scope.populateGroupFieldsAfterShowPane = function (groupID) {
        var fields = $filter('filter')($scope.fields, function (f) { return f.ParentID == groupID });

        angular.forEach(fields, function (field) {
            if (field.IsShow) callFieldInitFn(field);
        });
    };

    $scope.populatePaneFieldsAfterShowPane = function (paneName) {
        var fields = [].concat($filter('filter')($scope.fields, function (f) { return f.PaneName == paneName && f.IsShow }));

        $filter('filter')(fields, function (f) { return f.IsGroup }).map(function (g) {
            populateChildFields(g);
        });

        function populateChildFields(group) {
            var childs = $filter('filter')($scope.fields, function (f) { return f.ParentID == group.FieldID });

            fields = fields.concat(childs);

            $filter('filter')(childs, function (f) { return f.IsGroup }).map(function (g) {
                populateChildFields(g);
            });
        }

        angular.forEach(fields, function (field) {
            if (field.IsShow) callFieldInitFn(field);
        });
    };

    $scope.isFieldVisible = function (fieldName) {
        return $('#pnlBusinessDirectory' + $scope.moduleID + ' *[data-field="' + fieldName + '"]').length;
    }

    $scope.callAction = function (actionName, params) {
        actionManagerService.callActionByName($scope, actionName, params);
    };

    $scope.manageWatches = function (expression, methodName, param1, param2, param3, param4) {
        if (!expression || typeof expression != 'string') return;

        var matches = expression.match(/{(\w+([\.|\[\]\w]*)?)}/gim);
        angular.forEach(matches, function (m) {
            var match = /{(\w+([\.|\[\]\w]*)?)}/gim.exec(m);
            var propertyName = match[1];

            var result = $filter('filter')(watches, function (w) { return w.Property == propertyName });
            if (!result.length)
                watches.push({
                    Property: propertyName,
                    Methods: [{ MethodName: methodName, Param1: param1, Param2: param2, Param3: param3, Param4: param4 }]
                });
            else
                result[0].Methods.push({ MethodName: methodName, Param1: param1, Param2: param2, Param3: param3, Param4: param4 });
        });
    }

    function raiseWatches() {
        angular.forEach(watches, function (w) {
            if (w.Property && w.Methods.length) {
                $scope.$watch(w.Property, function (newVal, oldVal) {
                    if (newVal != oldVal) {
                        angular.forEach(w.Methods, function (m) {
                            $scope[m.MethodName](m.Param1, m.Param2, m.Param3, m.Param4);
                        });
                    }
                }, true);
            }
        });

        watches = [];
    }

    function isFieldShow(field) {
        return field.IsShow && $('*[data-pane=' + field.PaneName + ']').length;
    }

    function callFieldInitFn(field) {
        if (typeof window['bField_' + field.FieldType] == 'function') {
            var fn = new window['bField_' + field.FieldType]($scope, field);
            if (typeof fn['init'] == 'function') fn.init();
        }
    }
});