module = angular.module("jupiter.admin");
module.controller('SidebarController', SidebarController);


function SidebarController($location, $scope) {
    var ctrl = this;
    ctrl.items = [];

    this.valueIfPath = function(path, value) {
        return ($location.path().substr(0, path.length) === path) ? value : '';
    };

    this.initItems = function() {
        if ($scope.user.isAdmin()) {
            ctrl._addItem('/overview/', 'Сводка', 'fa fa-pie-chart');
            ctrl._addItem('/clients/', 'Клиенты', 'fa fa-users');
            ctrl._addItem('/accounts/', 'Cчета', 'fa fa-tasks');
            ctrl._addItem('/credits/', 'Кредиты', 'fa fa-money');
            ctrl._addItem('/deposits/', 'Вклады', 'fa fa-line-chart');
            ctrl._addItem('/transactions/', 'Транзакции', 'fa fa-exchange');
            ctrl._addItem('/finance-settings/', 'Настройки скоринга', 'fa fa-cog fa-spin fa-fw');
        }
        if ($scope.user.isClient()) {
            ctrl._addItem('/clients/me/', "Мой профайл", 'fa fa-address-card');
            ctrl._addItem('/accounts/', 'Мои счета', 'fa fa-credit-card-alt');
            ctrl._addItem('/credits/', 'Мои кредиты', 'fa fa-database');
            ctrl._addItem('/deposits/', 'Мои вклады', 'fa fa-bar-chart');
            ctrl._addItem('/transactions/', 'Мои транзакции', 'fa fa-exchange');
            ctrl._addItem('/credit-templates/', 'Оформление кредитов', 'fa fa-money');
            ctrl._addItem('/deposit-templates/', 'Оформление вкладов', 'fa fa-line-chart');
        }
    };

    this._addItem = function(url, label, icon) {
        ctrl.items.push({
            url: url,
            label: label,
            icon: icon
        });
    };
}
