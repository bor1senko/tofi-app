urls = {
    "/": "src/core/views/main.view.html",
    "/landing/": "src/core/views/landing.view.html",
    "/error/": "src/core/views/error.view.html",

    "/sign-in/": "src/auth/views/sign-in.view.html",
    '/sign-up/': "src/auth/views/sign-up.view.html",
    '/password-reset/': "src/auth/views/password-reset.view.html",
    '/password-reset-confirm': "src/auth/views/password-reset-confirm.view.html",


    '/credit-templates/:id/': 'src/public/views/credit-template-detail.view.html',
    '/credit-templates/:id/apply/': 'src/public/views/credit-apply.view.html',
    '/credit-templates/': 'src/public/views/credit-template-list.view.html',
    '/deposit-templates/:id/': 'src/public/views/deposit-template-detail.view.html',
    '/deposit-templates/:id/apply/': 'src/public/views/deposit-apply.view.html',
    '/deposit-templates/': 'src/public/views/deposit-template-list.view.html',

    '/overview/': 'src/admin/views/overview.view.html',
    '/accounts/': 'src/admin/views/accounts-list.view.html',
    '/clients/': 'src/admin/views/clients-list.view.html',
    '/clients/:id/': 'src/admin/views/clients-profile.view.html',
    '/credits/': 'src/admin/views/credits-list.view.html',
    '/credits/:id/': 'src/admin/views/credit-detail.view.html',
    '/deposits/': 'src/admin/views/deposits-list.view.html',
    '/deposits/:id/': 'src/admin/views/deposit-detail.view.html',
    '/transactions/': 'src/admin/views/transactions-list.view.html',
    '/finance-settings/': 'src/admin/views/finance-settings.view.html'
};


var app = angular.module(
    "jupiter",
    [
        "ngRoute",
        "ui.bootstrap",
        "jupiter.core",
        "jupiter.auth",
        "jupiter.public",
        "jupiter.admin"
    ]
);
app.config(function ($routeProvider, $locationProvider) {
    var routes = $routeProvider;
    for (var url in urls) {
        if (urls.hasOwnProperty(url)) {
            routes = routes.when(url, {templateUrl: urls[url]})
        }
    }
    $locationProvider.html5Mode({enabled: true, requireBase: true});
});
