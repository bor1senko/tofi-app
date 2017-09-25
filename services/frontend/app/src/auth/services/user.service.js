module = angular.module("jupiter.auth");
module.service("$user", UserService);
module.constant("clientsGroupName", "Clients");
module.constant("adminsGroupName", "Admins");


function UserService($localStorage, clientsGroupName, adminsGroupName) {
    var service = this;
    service.data = $localStorage.user;
    service.token = $localStorage.token;

    this.isAuthenticated = function() {
        service.token = $localStorage.token;
        return !!service.token;
    };

    this.isAdmin = function() {
        service.user = $localStorage.user;
        return service.user &&
               (service.user.is_superuser ||
               service.user.groups.some(function(group, i, groups) {
            return group.name == adminsGroupName;
        }));
    };

    this.isClient = function() {
        service.user = $localStorage.user;
        return service.user && !service.isAdmin() && service.user.groups.some(
            function(group, i, groups) {
                return group.name == clientsGroupName;
        });
    };
}
