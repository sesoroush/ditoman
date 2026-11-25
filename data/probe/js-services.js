mydnnBusinessDirectoryApp.service('panelService', function ($q, $rootScope, $http, $location, $timeout, $compile, $filter, $parse, $window, Upload) {
    var service = this;

    this.ajax = function (options) {
        var defer = $q.defer();
        var $ajaxbar;

        if (options.showAjaxbar && options.ajaxbarID) {
            $timeout(function () {
                $ajaxbar = angular.element('#' + options.ajaxbarID);
                $ajaxbar.removeClass('error shadow');
                $ajaxbar.find('>.content').text(options.ajaxMessage);
                $ajaxbar.addClass('show');
            }, 100);
        }
        $http({
            method: options.method,
            url: options.url,
            params: options.params,
            data: options.data,
            headers: options.headers,
        }).then(function (data) {
            $timeout(function () {
                if ($ajaxbar) $ajaxbar.removeClass('show');
            }, 100);
            defer.resolve(data.data);
        }, function (error) {
            var errorMessage = '';
            if (error && typeof error.data == 'string')
                errorMessage = error.data;
            else
                errorMessage = error.statusText;

            $timeout(function () {
                if ($ajaxbar) {
                    $ajaxbar.addClass('error');
                    $ajaxbar.find('>.ajax-error').data('content', errorMessage);
                    $ajaxbar.find('>.ajax-error').popover({ container: "body" });
                    if (options.showErrorMessage)
                        setTimeout(function () {
                            $ajaxbar.find('>.ajax-error').popover('show');
                        }, 500);

                    angular.element('html, body').animate({
                        scrollTop: $ajaxbar.offset().top - 100
                    }, 1300, 'swing', function () {
                        $ajaxbar.addClass('shadow');
                    });
                }
            }, 100);

            if (error.status == 401) {
                $http.get(mydnnBusinessDirectoryGlobal.serviceUrl + 'PanelService/GetUserID', { headers: mydnnBusinessDirectoryGlobal.ajaxHeaders }).success(function (userID) // check user for login user
                {
                    mydnnBusinessDirectoryGlobal.userID = userID;

                    if (userID == -1) { //the user not logon
                        var url = $location.path();
                        $location.path('/login' + url);
                    }
                    else //The user does not have access to this method
                    {
                        $location.path('/access-denied');
                    }
                });
            }
            else if (error.status == 403) { // access denied
                $location.path('/access-denied');

            }
            defer.reject(error);
        });

        return defer.promise;
    }

    this.uploadFile = function ($scope, $file) {
        var defer = $q.defer();

        if (!$file) defer.resolve({ status: -1 });
        else {
            var headers = {
                TabId: $scope.ajaxHeaders.TabId,
                ModuleId: $scope.ajaxHeaders.ModuleId,
                'Content-Type': $file.type
            }

            if (!$file) {
                defer.resolve({ status: -1 });
            }
            else
                return Upload.upload({
                    url: mydnnBusinessDirectoryGlobal.serviceUrl + 'Service/UploadFile',
                    headers: headers,
                    data: { files: $file, FileUploadType: 1 },
                });
        }

        return defer.promise
    }

    this.uploadFiles1 = function (url, headers, params) {
        var defer = $q.defer();

        var $files = params.files;

        if (!$files) {
            defer.resolve({ status: -1 });
        }
        else
            return Upload.upload({
                url: url,
                headers: headers,
                data: params,
            });

        return defer.promise
    }

    this.upload = function ($scope, files) {

    };

    this.uploadFiles = function (files, type, url, headers, params, maxFiles, $files, $file, $newFiles, $duplicateFiles, $invalidFiles, $event) {
        var defer = $q.defer();

        angular.forEach($invalidFiles, function (f) {
            var file = {
                File: f,
                FileName: f.name,
                FileType: f.type,
                FileSize: f.size,
                Status: -1,
                Message: f.$error,
            }

            files.push(file);

            if (type == "Photo")
                service.previewImage(f).then(function (data) {
                    file.PreviewImage = data;
                });
        });

        angular.forEach($files, function (f) {
            var file = {
                File: f,
                FileName: f.name,
                FileType: f.type,
                FileSize: f.size,
                Status: 0,
            }

            files.push(file);

            if ($filter('filter')(files, function (ff) { return ff.Status != -1 }).length > maxFiles) {
                file.Status = -1;
                file.Message = 'maxFiles';
            }

            if (type == "Photo")
                service.previewImage(f).then(function (data) {
                    file.PreviewImage = data;
                });
        });

        processUploads(files, url, headers, params).then(function (data) {
            defer.resolve(files);
        });

        return defer.promise
    }

    function processUploads(files, url, headers, params) {
        var defer = $q.defer();

        var result = $filter('filter')(files, function (f) { return f.Status == 0 });
        var file = result.length ? result[0] : undefined;

        return processUpload(file, url, headers, params).then(function (data) {
            if (data.isFinal)
                defer.resolve();
            else
                return processUploads(files, url, headers, params);
        })

        return defer.promise
    }

    function processUpload(file, url, headers, params) {
        var defer = $q.defer();

        if (!file) {
            defer.resolve({ isFinal: true });
        }
        else {
            params.files = file.File;
            headers['Content-Type'] = file.File.type;

            Upload.upload({
                url: url,
                headers: headers,
                data: params,
            }).then(function (data) {
                file.Status = 1;

                file.Data = data.data;

                defer.resolve({ isFinal: false });
            }, function (error) {
                file.Status = -1;

                file.Message = error.data.Message;

                defer.resolve({ isFinal: false });
            }, function (evt) {
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                file.Progress = progressPercentage;
            });
        }

        return defer.promise
    }

    this.previewImage = function ($file) {
        var defer = $q.defer();

        var reader = new FileReader();
        reader.onload = function (e) {
            defer.resolve(e.target.result)
        };
        reader.readAsDataURL($file);

        return defer.promise;
    };

    this.groupBy = function (xs, key) {
        return xs.reduce(function (rv, x) {
            (rv[x[key]] = rv[x[key]] || []).push(x);
            return rv;
        }, {});
    };

    this.parseJsonItems = function (items) {
        if (!items) return items;

        if (typeof items == 'object' && items instanceof Array == false) {
            for (key in items) {
                var value = items[key];
                if (value && value instanceof Array)
                    service.parseJsonItems();
                else if (typeof key == 'string' && typeof value == 'string' && value && /^[\],:{}\s]*$/.test(value.toLowerCase().replace(/\\["\\\/bfnrtu]/g, '@').
                    replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
                    replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
                    try {
                        items[key] = JSON.parse(value);
                        if (typeof items[key] == 'object' && items[key] instanceof Array == false)
                            service.parseJsonItems(items[key]);
                        else if (typeof items[key] == 'object' && items[key] instanceof Array == true)
                            service.parseJsonItems(items[key]);
                    } catch (e) {
                        items[key] = value;
                        console.log(e);
                    }
                }
            }
        }
        else if (items instanceof Array) {
            angular.forEach(items, function (item) {
                if (typeof item == 'object' && item instanceof Array == false)
                    service.parseJsonItems(item);
                if (typeof item == 'object' && item instanceof Array == true)
                    service.parseJsonItems(item);
            });
        }
    }

    this.parseJsonItemsOld = function (items) {
        if (!items) return items;

        if (typeof items == 'object' && items instanceof Array == false) {
            for (key in items) {
                var value = items[key];
                if (typeof key == 'string' && typeof value == 'string' && value && /^[\],:{}\s]*$/.test(value.toLowerCase().replace(/\\["\\\/bfnrtu]/g, '@').
                    replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
                    replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
                    try {
                        items[key] = JSON.parse(value);
                    } catch (e) {
                    }
                }
            }
        }
        else if (items instanceof Array == true) {
            angular.forEach(items, function (item) {
                for (key in item) {
                    var value = item[key];
                    if (typeof key == 'string' && typeof value == 'string' && value && /^[\],:{}\s]*$/.test(value.toLowerCase().replace(/\\["\\\/bfnrtu]/g, '@').
                        replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
                        replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
                        try {
                            item[key] = JSON.parse(value);
                        } catch (e) {
                        }
                    }
                }
            });
        }
    }

    this.isJsonString = function (str) {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    }

    this.getJsonString = function (str) {
        try {
            var result = JSON.parse(str);
            return result;
        } catch (e) {
            return str;
        }
    }

    this.findOne = function (haystack, arr) {
        return arr.some(function (v) {
            return haystack.indexOf(v) >= 0;
        });
    };

    this.getUrlParams = function (url) {
        var params = {};
        var parser = document.createElement('a');
        parser.href = url;
        var query = parser.search.substring(1);
        var vars = query.split('&');
        for (var i = 0; i < vars.length; i++) {
            if (vars[i]) {
                var pair = vars[i].split('=');
                params[pair[0].toLowerCase()] = decodeURIComponent(pair[1]);
            }
        }

        //parse friendly params
        var friendlyParams = location.pathname.toLowerCase().split('/');
        var index = friendlyParams.length - 2;
        while (index >= 0) {
            if (friendlyParams[index] && friendlyParams.length >= index + 2) params[friendlyParams[index].toLowerCase()] = decodeURIComponent(friendlyParams[index + 1]);

            index = index - 2;
        }

        return params;
    }

    this.getParameterByName = function (name, url) {
        if (!url) url = decodeURIComponent(window.location.href);
        url = url.toString();//.toLowerCase();
        name = name.toLowerCase();
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) {
            //parse friendly params
            var friendlyParams = location.pathname.toLowerCase().replace(/=/g, '/').split('/');
            if (friendlyParams.indexOf(name) >= 0 && friendlyParams.length >= friendlyParams.indexOf(name) + 2) return friendlyParams[friendlyParams.indexOf(name) + 1];

            return null;
        }
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    this.getHashParameterByName = function (name, url) {
        if (!url) url = window.location.hash;
        url = url.replace('#/', '?').replace('#', '?');
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    this.runService = function ($scope, serviceID, params) {
        for (p in params) {
            if (params[p] === undefined || params[p] === '') params[p] = null;
        }

        return service.ajax({
            method: 'POST',
            url: mydnnBusinessDirectoryGlobal.serviceUrl + 'Service/RunService',
            headers: $scope.ajaxHeaders,
            data: { ServiceID: serviceID, Params: params },
        });
    }

    this.getItemValue = function (item, fieldName, IsSelective) {
        var values;
        var columnValue = item[fieldName];
        if (!columnValue) return columnValue;
        if (IsSelective) {
            if (columnValue instanceof Array) {
                values = [];
                angular.forEach(columnValue, function (v) {
                    if (v && v.OptionValue) values.push(v.OptionValue);
                });
            }
            else
                values = columnValue && columnValue.OptionValue ? columnValue.OptionValue : columnValue;
        }
        else
            values = typeof columnValue == 'string' ? columnValue : JSON.stringify(columnValue)

        return values;
    }

    this.checkConditions = function ($scope, conditions) {
        if (!conditions || !conditions.length) return true;

        var andResult = true;

        var groups = $filter('groupBy')(conditions, 'GroupName');
        for (key in groups) {
            var orResult = false;
            angular.forEach(groups[key], function (c) {
                var leftValue = service.getScopePropertyValue($scope, c.LeftExpression);
                var rightValue = service.getScopePropertyValue($scope, c.RightExpression);

                if (typeof leftValue == 'string') leftValue = service.getJsonString(leftValue);
                if (typeof rightValue == 'string') rightValue = service.getJsonString(rightValue);

                var compareResult = service.compareTwoValue(leftValue, rightValue, c.EvalType);

                if (!orResult && compareResult) orResult = true;
            });
            if (!orResult) {
                andResult = false;
                break;
            }
        }

        return andResult;
    }

    this.compareTwoValue = function (val2, val1, evalType) {
        if (val2 == undefined || val2 == null) val2 = '';
        if (val1 == undefined || val1 == null) val1 = '';

        var result = false;
        switch (evalType) {
            case '=':
                if (val2 instanceof Array == false)
                    result = val2 == val1;
                else {
                    var isTrue = undefined;
                    angular.forEach(val2, function (v) {
                        if ((isTrue == undefined || isTrue) && v == val1)
                            isTrue = true;
                        else
                            isTrue = false;
                    })
                    result = isTrue;
                }
                break;
            case '!=':
                if (val2 instanceof Array == false)
                    result = val2 != val1;
                else {
                    var isTrue = undefined;
                    angular.forEach(val2, function (v) {
                        if ((isTrue == undefined || isTrue) && v != val1)
                            isTrue = true;
                        else
                            isTrue = false;
                    })
                    result = isTrue;
                }
                break;
            case 'in':
                if (val2 instanceof Array == false)
                    result = val2 == val1;
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (v == val1) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case 'not in':
                if (val2 instanceof Array == false)
                    result = val2 != val1;
                else {
                    var isTrue = true;
                    angular.forEach(val2, function (v) {
                        if (v == val1) isTrue = false;
                    })
                    result = isTrue;
                }
                break;
            case 'like':
                if (val2 instanceof Array == false)
                    result = val2.indexOf(val1) >= 0;
                else { //in
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (v.indexOf(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case 'not like':
                if (val2 instanceof Array == false)
                    result = val2.indexOf(val1) == -1;
                else { //not in
                    var isTrue = true;
                    angular.forEach(val2, function (v) {
                        if (v.indexOf(val1)) isTrue = false;
                    })
                    result = isTrue;
                }
                break;
            case '>':
                if (val2 instanceof Array == false)
                    result = parseFloat(val2) > parseFloat(val1)
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (parseFloat(v) > parseFloat(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case '>=':
                if (val2 instanceof Array == false)
                    result = parseFloat(val2) >= parseFloat(val1)
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (parseFloat(v) >= parseFloat(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case '<':
                if (val2 instanceof Array == false)
                    result = parseFloat(val2) < parseFloat(val1)
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (parseFloat(v) < parseFloat(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case '<=':
                if (val2 instanceof Array == false)
                    result = parseFloat(val2) <= parseFloat(val1)
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (parseFloat(v) <= parseFloat(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case '=:':
                if (val2 instanceof Array == false)
                    result = val2.startsWith(val1);
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (v.startsWith(val1)) isTrue = true;
                    });
                    result = isTrue;
                }
                break;
            case ':=':
                if (val2 instanceof Array == false)
                    result = val2.endsWith(val1);
                else {
                    var isTrue = false;
                    angular.forEach(val2, function (v) {
                        if (v.endsWith(val1)) isTrue = true;
                    })
                    result = isTrue;
                }
                break;
            case 'isfilled':
                if (val2 != undefined && val2 != null && val2 != '') result = true;
                break;
            case 'isnull':
                if (val2 == undefined || val2 == 'undefined' || val2 == null || val2 == '') result = true;
                break;
            default:
        }

        return result;
    }

    this.fillItemByFields = function (fields, item) {
        item = item || {};

        angular.forEach(fields, function (f) {
            if ((f.Value == undefined || f.Value == null) && service.isNumericType(f.ColumnType)) {
                item[f.FieldName] = 0;
            }
            else
                item[f.FieldName] = f.Value;
        });

        return item;
    }

    this.isNumericType = function (columnType) {
        if (!columnType) return false;

        else if (columnType.toLowerCase().startsWith("decimal")) return true;
        else if (columnType.toLowerCase().startsWith("numeric")) return true;
        else if (columnType.toLowerCase().startsWith("float")) return true;
        else if (columnType.toLowerCase().startsWith("real")) return true;
        else if (columnType.toLowerCase().startsWith("int")) return true;
        else if (columnType.toLowerCase().startsWith("bigint")) return true;
        else if (columnType.toLowerCase().startsWith("smallint")) return true;
        else if (columnType.toLowerCase().startsWith("tinyint")) return true;
        else if (columnType.toLowerCase().startsWith("money")) return true;
        else if (columnType.toLowerCase().startsWith("smallmoney")) return true;

        return false;
    }

    this.encode64 = function (input, key) {
        key = key ? key : "ABCDEFGHIJKLMNOP" +
            "QRSTUVWXYZabcdef" +
            "ghijklmnopqrstuv" +
            "wxyz0123456789+/" +
            "=";

        input = escape(input);
        var output = "";
        var chr1, chr2, chr3 = "";
        var enc1, enc2, enc3, enc4 = "";
        var i = 0;

        do {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);

            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;

            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }

            output = output +
                key.charAt(enc1) +
                key.charAt(enc2) +
                key.charAt(enc3) +
                key.charAt(enc4);
            chr1 = chr2 = chr3 = "";
            enc1 = enc2 = enc3 = enc4 = "";
        } while (i < input.length);

        return output;
    }

    this.decode64 = function (input, key) {
        key = key ? key : "ABCDEFGHIJKLMNOP" +
            "QRSTUVWXYZabcdef" +
            "ghijklmnopqrstuv" +
            "wxyz0123456789+/" +
            "=";

        var output = "";
        var chr1, chr2, chr3 = "";
        var enc1, enc2, enc3, enc4 = "";
        var i = 0;

        // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
        var base64test = /[^A-Za-z0-9\+\/\=]/g;
        if (base64test.exec(input)) {
            alert("There were invalid base64 characters in the input text.\n" +
                "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                "Expect errors in decoding.");
        }
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

        do {
            enc1 = key.indexOf(input.charAt(i++));
            enc2 = key.indexOf(input.charAt(i++));
            enc3 = key.indexOf(input.charAt(i++));
            enc4 = key.indexOf(input.charAt(i++));

            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;

            output = output + String.fromCharCode(chr1);

            if (enc3 != 64) {
                output = output + String.fromCharCode(chr2);
            }
            if (enc4 != 64) {
                output = output + String.fromCharCode(chr3);
            }

            chr1 = chr2 = chr3 = "";
            enc1 = enc2 = enc3 = enc4 = "";

        } while (i < input.length);

        return unescape(output);
    }

    this.copyToClipboard = function (str) {
        const el = document.createElement('textarea');
        el.value = str;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    }

    this.sort = function (a, b, field, desc) {
        var aName = a[field];
        var bName = b[field];
        if (!desc)
            return ((aName < bName) ? -1 : ((aName > bName) ? 1 : 0));
        else
            return ((aName > bName) ? -1 : ((aName < bName) ? 1 : 0));
    }

    this.getCategoryField = function (fields) {
        var result = $filter('filter')(fields, function (f) { return f.FieldType == 'Categories' });
        return result.length ? result[0] : undefined;
    }

    this.getCleanUrlForMbdSearch = function (url) {
        if (!url) return '';
        return url.endsWith("/") ? url.substr(0, url.length - 1) : url;
    }

    this.decodeHtml = function (html) {
        var txt = document.createElement("textarea");
        txt.innerHTML = html;
        return txt.value;
    }

    this.evalateToken = function (token, $scope) {
        try {
            if (service.isNonComputational(token))
                return $scope && 1 == 2 ? $parse(token)($scope) : eval(token);
            else
                return token;
        } catch (e) {
            return token;
        }
    };

    this.isNonComputational = function (str) {
        var result = true;

        if (typeof str == 'number' || typeof str == 'boolean' || $.isNumeric(str)) return false;

        if (str && typeof str == 'string' && (/^-?\d+,+/.test(str) || /^['|"].*['|"],/.test(str) || /^\{.*\}$/.test(str))) return false;

        if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(str)) return false; //date

        return result;
    }

    this.compileElement = function ($scope, content) {
        debugger

        var defer = $q.defer();

        var compiled = $compile(content)($scope);

        $timeout(function () {
            defer.resolve(compiled[0].outerHTML);
        });

        return defer.promise;

    }

    this.getScopePropertyValue = function ($scope, propertyStr, forDisplay) {
        if (!propertyStr)
            return propertyStr;
        else
            propertyStr = propertyStr.toString();

        var isEval = false;

        if (typeof propertyStr == 'string') {
            //parse user
            matches = propertyStr.match(/{Eval:(.+)}/gim);
            angular.forEach(matches, function (m) {
                match = /{Eval:(.+)}/gim.exec(m);
                if (match && match.length > 1) {
                    propertyStr = match[1];
                    isEval = true;
                }
            });
        }

        var value = propertyStr;
        var matches;
        var match;

        //parse Scope
        if ($scope && $scope.ajaxHeaders) value = propertyStr = propertyStr.replace(/{MBDScope}/gim, 'angular.element(document.getElementById("pnlBusinessDirectory' + $scope.moduleID + '")).scope()');

        //parse actions
        if (typeof propertyStr == 'string' && $scope.customActions) {
            matches = propertyStr.match(/{Action:(\w+)(.*)?}/gim);
            angular.forEach(matches, function (m) {
                match = /{Action:(\w+)(.*)?}/gim.exec(m);
                if (match && match.length > 1) {
                    value = $scope.customActions[match[1]];

                    if (match[2]) {
                        var params = service.splitObjectPropertiesByString(match[2]);

                        value = service.getValueOfObject(params, value);
                    }
                    if (m != propertyStr) {
                        value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                    }
                }
            });
        }

        if (typeof propertyStr == 'string') {
            //parse action param
            matches = propertyStr.match(/{ActionParam:(\w+)([\.|\[\]\w]*)?}/gim);
            angular.forEach(matches, function (m) {
                match = /{ActionParam:(\w+)([\.|\[\]\w]*)?}/gim.exec(m);
                if (match && match.length > 1) {
                    value = $scope['MBDAP_' + match[1]];

                    if (match[2]) {
                        var params = service.splitObjectPropertiesByString(match[2]);
                        value = service.getValueOfObject(params, value);
                    }
                    if (m != propertyStr) {
                        if (value && typeof value == 'object')
                            value = propertyStr = propertyStr.replace(m, '$scope.MBDAP_' + match[1] + (match[2] ? match[2] : ''));
                        else
                            value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                    }
                }
            });
        }

        if (typeof propertyStr == 'string') {
            //parse page params
            matches = propertyStr.match(/{PageParam:(\w+)}/gim);
            angular.forEach(matches, function (m) {
                match = /{PageParam:(\w+)}/gim.exec(m);
                if (match && match.length > 1) {
                    var paramValue = service.getParameterByName(match[1]);
                    value = paramValue ? decodeURIComponent(paramValue) : paramValue;

                    if (m != propertyStr) {
                        value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                    }
                }
            });
        }

        if (typeof propertyStr == 'string') {
            //parse local storage
            matches = propertyStr.match(/{LocalStorage:(\w+)}/gim);
            angular.forEach(matches, function (m) {
                match = /{LocalStorage:(\w+)}/gim.exec(m);
                if (match && match.length > 1) {
                    value = localStorage.getItem(match[1]);

                    if (m != propertyStr) {
                        value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                    }

                    if (service.isJsonString(value)) {
                        value = service.getJsonString(value);
                        service.parseJsonItems(value);
                    }
                }
            });
        }

        if (typeof propertyStr == 'string') {
            //parse session storage
            matches = propertyStr.match(/{SessionStorage:(\w+)}/gim);
            angular.forEach(matches, function (m) {
                match = /{SessionStorage:(\w+)}/gim.exec(m);
                if (match && match.length > 1) {
                    value = sessionStorage.getItem(match[1]);

                    if (m != propertyStr) {
                        value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                    }
                }
            });
        }

        if (typeof propertyStr == 'string') {
            //parse user
            matches = propertyStr.match(/{CurrentUser:(\w+)}/gim);
            angular.forEach(matches, function (m) {
                match = /{CurrentUser:(\w+)}/gim.exec(m);
                if (match && match.length > 1) {
                    switch (match[1].toLowerCase()) {
                        case 'userid':
                            value = mydnnBusinessDirectoryGlobal.userID;

                            if (m != propertyStr) {
                                value = propertyStr = propertyStr.replace(m, value != undefined && value != null ? value.toString() : 'undefined');
                            }

                            break;
                    }
                }
            });
        }

        var experssions = [];
        //parse angular {experssion}
        do {
            if (typeof propertyStr == 'string') {
                matches = propertyStr.match(/\{(.[^{}:\$]+)\}/gim);
                if (!matches) break;
                angular.forEach(matches, function (m) {
                    match = /\{(.[^{}:\$]+)\}/gim.exec(m);
                    if (match && match.length > 1) {
                        try {
                            value = service.getValueOfObject(service.splitObjectPropertiesByString(match[1]), $scope);
                        } catch (e) {
                            value = undefined;
                        }

                        if (forDisplay && (value == undefined || value == null)) value = '';

                        if (m != propertyStr) {
                            if (value && typeof value == 'object') {
                                if (forDisplay)
                                    value = propertyStr.replace(m, '{$' + match[1] + '$}');
                                else
                                    value = propertyStr.replace(m, '$scope.' + match[1]);
                            }
                            else {
                                value = propertyStr = propertyStr.replace(m, value);
                            }
                        }

                        propertyStr = value;
                    }
                });
            }
            else
                break;

        }
        while (true)

        if (typeof value == 'string') value = value.replace(/{\$(.[^\$}]+)\$}/gm, '{$1}');

        if (isEval) value = service.evalateToken(value, $scope);

        return value;
    }

    this.getScopeProperty = function ($scope, propertyStr) {
        var match;

        if (!propertyStr) return undefined;

        propertyStr = propertyStr.toString();

        //parse actions param
        if (!match && $scope.customActions) {
            match = /{ActionParam:(\w+)([\.|\[\]\w]*)?}/gim.exec(propertyStr);
            if (match && match.length > 1) {
                propertyStr = 'MBDAP_' + match[1];

                if (match.length > 2 && match[2]) propertyStr += match[2];
            }
        }

        //parse actions param
        match = /{(\w+.[^{}\\+-]+)}$/gim.exec(propertyStr);
        if (match && match.length > 1) propertyStr = match[1];


        return $parse(propertyStr);
    }

    this.isScopeProperty = function ($scope, propertyStr) {
        if (!propertyStr) return false;

        propertyStr = propertyStr.toString();

        if (Object.keys($scope).indexOf(propertyStr.split('.')[0]) >= 0 || $scope[propertyStr] != undefined)
            return true;
        else
            return false;
    }

    this.getValueOfObject = function (a, b) {
        const getNestedObject = (nestedObj, pathArr) => {
            return pathArr.reduce((obj, key) =>
                (obj && obj[key] !== undefined) ? obj[key] : undefined, nestedObj);
        }

        return getNestedObject(b, a);
    }

    this.setPropertiesValue = function ($scope, properties) {
        angular.forEach(properties, function (property) {
            var isTrue = true;

            if (property.Conditions && property.Conditions.length) isTrue = service.checkConditions($scope, property.Conditions);

            if (isTrue) {
                var propertyStr = property.Condition ? property.Condition : '';
                var model = service.getScopeProperty($scope, propertyStr);

                var propertyValue = service.getScopePropertyValue($scope, property.FieldValue);

                if (model) model.assign($scope, propertyValue);
            }
        });
    }

    this.splitObjectPropertiesByString = function (str) {
        var arr = [];
        var key = '';
        var status = '';
        for (var i = 0; i < str.length; i++) {
            if (str[i] == '.') {
                if (key) arr.push(key);
                key = '';
                continue;
            }
            else if (str[i] == '[') {
                if (key) arr.push(key);
                status = 'array';
                key = '';
                continue;
            }
            else if (str[i] == ']') {
                if (key) arr.push(key);
                status = '';
                key = '';
                continue;
            }

            key += str[i];
        }
        if (key) arr.push(key);

        return arr;
    }

    this.compare2Obj = function (obj1, obj2, inAllProperties) {
        if ((obj1 && !obj2) || (!obj1 && obj2)) return false;

        for (key in obj1) {
            if (obj2.hasOwnProperty(key) &&
                (
                    (obj1[key] instanceof Array == false && obj2[key] instanceof Array == false && obj1[key] != obj2[key]) ||
                    (obj1[key] instanceof Array && obj1[key].indexOf(obj2[key]) == -1) ||
                    (obj2[key] instanceof Array && obj2[key].indexOf(obj1[key]) == -1)
                )
            )
                return false;
        }

        return true;
    }

    this.hasObjectValue = function (obj, propertyName, value) {
        if (!obj || !propertyName) return false;

        var find = false;

        angular.forEach(obj, function (o) {
            if (o[propertyName] == value) find = true;
        });

        return find;
    }

    this.sum = function (items, prop) {
        if (items == null) {
            return 0;
        }
        return items.reduce(function (a, b) {
            return b[prop] == null ? a : a + b[prop];
        }, 0);
    };

    this.getImageFromUrl = function (url) {
        var defer = $q.defer();

        var img = new Image();
        img.src = url;
        img.setAttribute('crossOrigin', 'anonymous');
        img.onload = function (a) {
            var canvas = document.createElement("canvas");
            canvas.width = this.width;
            canvas.height = this.height;
            var ctx = canvas.getContext("2d");
            ctx.drawImage(this, 0, 0);

            var dataURI = canvas.toDataURL("image/jpg");

            // convert base64/URLEncoded data component to raw binary data held in a string
            var byteString;
            if (dataURI.split(',')[0].indexOf('base64') >= 0)
                byteString = atob(dataURI.split(',')[1]);
            else
                byteString = unescape(dataURI.split(',')[1]);

            // separate out the mime component
            var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

            // write the bytes of the string to a typed array
            var ia = new Uint8Array(byteString.length);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }

            defer.resolve(new Blob([ia], { type: mimeString }));
        }

        return defer.promise
    }

    this.parsePublicTokens = function (input, item, $scope) {
        if (!input) return '';

        var tokenName = input.toString();

        var matches = tokenName.match(/{Field:(\w+)((\[(\d)\])?\.(\w+))?}/gmi);
        angular.forEach(matches, function (match) {
            var m = /{Field:(\w+)((\[(\d)\])?\.(\w+))?}/gmi.exec(match)
            var value = item[m[1]];
            if (typeof value == 'object') {
                if (!value)
                    value = '';
                else if (!m[5] && value.OptionValue)
                    value = value.OptionValue;
                else if (!m[5] && value.OptionText)
                    value = value.OptionText;
                else if (!m[5] && value instanceof Array && value.length) {
                    var newValue = '';
                    for (var j = 0; j < value.length; j++) {
                        var v = value[j];

                        if (v.OptionValue)
                            newValue += v.OptionValue
                        else if (v.OptionText)
                            newValue += v.OptionText
                        else
                            newValue += JSON.stringify(v);

                        if (j < value.length - 1) newValue += ", ";
                    }
                    value = newValue;
                }
                else if (m[5]) {
                    if (m[4] && value instanceof Array && value.length > parseInt(m[4]))
                        value = value[parseInt(m[4])][m[5]];
                    else {
                        if (value instanceof Array && value.length == 1) value = value[0];
                        value = value[m[5]];
                    }

                    if (value && typeof value == 'object') value = JSON.stringify(value);
                }
                else
                    value = JSON.stringify(value);
            }

            tokenName = tokenName.replace(match, value != undefined && value != null ? value : '');
        });

        match = tokenName.match(/{PageParam:(\w+)}/gmi);
        angular.forEach(match, function (m) {
            var value = service.getParameterByName(m.match(/{PageParam:(\w+)}/i)[1]);
            tokenName = tokenName.replace(m, value != undefined && value != null ? value : '');
        });

        match = tokenName.match(/{LocalStorage:(\w+)}/gmi);
        angular.forEach(match, function (m) {
            var value = localStorage.getItem(m.match(/{LocalStorage:(\w+)}/i)[1]);
            tokenName = tokenName.replace(m, value != undefined && value != null ? value : '');
        });

        if ($scope) {
            tokenName = tokenName.replace(/{CurrentStepNumber}/ig, $scope.currentStep);

            if ($scope.mbdPublicVariables) {
                matches = tokenName.match(/{ServiceResult:(\w+)((\[(\d)\])?(\.(\w+))?)?}/gim);
                angular.forEach(matches, function (match) {
                    var m = /{ServiceResult:(\w+)((\[(\d)\])?(\.(\w+))?)?}/gim.exec(match);

                    var serviceName = m[1];

                    var result = $filter('filter')($scope.mbdPublicVariables, function (v) { return v.Type == 'ServiceResult', Name == serviceName });
                    if (result.length) {
                        var serviceResult = result[0].Value;

                        var value;
                        if (m[6] && m[4] && serviceResult instanceof Array && serviceResult.length >= m[4])
                            value = serviceResult[m[4]][m[6]];
                        else if (!m[6] && m[4] && serviceResult instanceof Array && serviceResult.length >= m[4])
                            value = serviceResult[m[4]];
                        else if (m[6] && !m[4])
                            value = serviceResult[m[6]];
                        else
                            value = serviceResult;

                        tokenName = tokenName.replace(m, value != undefined && value != null ? value : '');
                    }
                });
            }
        }

        tokenName = tokenName.replace('{CurrentUser:UserID}', mydnnBusinessDirectoryGlobal.userID);

        return tokenName;
    }

    this.updateURLParameter = function (url, param, paramVal) {
        var newAdditionalURL = "";
        var tempArray = url.split("?");
        var baseURL = tempArray[0];
        var additionalURL = tempArray[1];
        var temp = "";
        if (additionalURL) {
            tempArray = additionalURL.split("&");
            for (var i = 0; i < tempArray.length; i++) {
                if (tempArray[i].split('=')[0] != param) {
                    newAdditionalURL += temp + tempArray[i];
                    temp = "&";
                }
            }
        }

        var rows_txt = temp + "" + param + "=" + paramVal;
        return baseURL + "?" + newAdditionalURL + rows_txt;
    }

    this.loadJsFile = function () {
        var defer = $q.defer();

        var script = document.createElement('script');
        script.onload = function () {
            defer.resolve();
        };
        script.src = something;

        document.body.appendChild(script); //or something of the likes

        return defer.promise;
    }

    this.extendParams = function (params, currentParams) {
        var result = [];

        angular.forEach(params, function (param) {
            if (currentParams && currentParams.length) {
                $filter('filter')(currentParams, function (p) { return p.ParamName == param.ParamName }).map(function (p) {
                    param.ParamValue = p.ParamValue;
                });
            }

            result.push(param);
        });

        return result;
    }

    this.getTokensFromText = function (text) {
        if (!text) return [];

        var result = [];

        angular.forEach(text.match(/{Token:(\w+)}/gim), function (m) {
            var paramName = /{Token:(\w+)}/gim.exec(m)[1];
            if ($filter('filter')(result, function (i) { return i.ParamName == paramName }).length == 0)
                result.push({ ParamName: paramName });
        });

        return result;
    }

    this.processTokenValue = function (text, tokens) {
        if (!text) return '';

        angular.forEach(text.match(/{Token:(\w+)}/gim), function (m) {
            var paramName = /{Token:(\w+)}/gim.exec(m)[1];
            $filter('filter')(tokens, function (i) { return i.ParamName == paramName }).map(function (token) {
                text = text.replace(new RegExp(m, 'g'), token.ParamValue);
            });
        });

        return text;
    }

    this.getModuleData = function (actions, services) {
        var result = {};

        angular.forEach(actions, function (action) {
            if (action.ActionType == 'GetListDataSource') {
                result[action.ActionDetails.ResultName] = {
                    Name: action.ActionDetails.ResultName,
                    Type: 'List'
                }

                $filter('filter')(services, function (s) { return s.ServiceID == action.ActionDetails.ServiceID }).map(function (service) {
                    if (service.Settings) result[action.ActionDetails.ResultName].Columns = service.Settings.DataSourceColumns;
                });
            }
        });

        return result;
    }

    this.isHtml = function (str) {
        if (!str || typeof str != 'string') return false;

        var result;

        try {
            result = $(str);

            return true;
        } catch (e) {
            return false;
        }

        //return /^<\/?[a-z][\s\S]*>/im.test(str.trim());
    }

    function runJavascriptAction($scope, action) {
        var defer = $q.defer();

        var newScript = document.createElement('script');
        newScript.innerHTML = service.getScopePropertyValue($scope, action.ActionDetails.Code);
        $('body').append(newScript);

    }
});

function IsNull(a, b) {
    if (a == undefined || a == null)
        return b;
    else
        return a;
}