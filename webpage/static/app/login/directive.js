app.factory('User', function($q, $cookies) {
    var User = function(){
       this.profile;
       this.expires = moment().add(10, 'm').toDate();
    };

    User.prototype.get = function(callback){
       if(angular.isDefined(this.name)){
          callback(this.json());
       } else {
          var that = this;
          google.script.run.withSuccessHandler(function(options){
             that.init(options);
             callback(that.json());
          }).getUser();
       }
    };

    User.prototype.init = function(options){
       angular.extend(this, options);
       //console.log(this.email);
       this.name = this.email.split("@")[0];
    };

    User.prototype.json = function(){
       return {
          name: this.name,
          email: this.email,
          locale: this.locale,
          admins: this.admins
       };
    };

    User.prototype.recall = function(callback){
       this.profile = $cookies.getObject('profile');
       if(angular.isDefined(this.profile)){
          callback();
       }
    };

    User.prototype.auth = function(credentials, callback){
       var that = this;
       this.profile = $cookies.getObject('profile');
       if(angular.isUndefined(this.profile)){
          google.script.run.withSuccessHandler(function(profile){
             //console.log(profile);
             if(angular.isDefined(profile)){
                that.profile = {
                   email: profile.email,
                   authority: profile.authority,
                   duties: profile.duty,
                   password: profile.password,
                   duties: profile.duties,
                   index: profile.index
                };
                $cookies.putObject('profile', that.profile, {expires: that.expires});
             }
             callback();
          }).authUser(credentials);
       } else {
          callback();
       }
    };

    User.prototype.signoff = function(){
       this.profile = undefined;
       $cookies.putObject('profile', this.profile);
       this.signedoff = true;
    };

    User.prototype.isEntitledAs = function(title){
       if(angular.isUndefined(this.profile)){
         return false;
       }
       var target = this.profile.duties.filter(function(duty){
          return title === duty.name;
       });
       if(target.length === 0){
         return false;
       } else {
         return target[0].status;
       }
    };

    User.prototype.equals = function(user){
       return this.profile.index === user.index;
    };

    return new User();
});

app.directive('login', function (User, $timeout) {
    return {
        restrict: 'E',
        templateUrl: 'static/app/login/login.tpl.html',
        scope: {logedin: "="},
        controller: function ($scope, $mdDialog) {
           $scope.signing = false;
           $scope.logedin = false;

           User.recall(function(){
              $scope.logedin = true;
           });

           $scope.signin = function(email, password){
               $scope.signing = true;
               //$scope.$apply();
               User.auth({email: email, password: password}, function(){
                  $scope.signing = false;
                  if(angular.isUndefined(User.profile)){
                     $mdDialog.show(
                       $mdDialog.alert()
                       .parent(angular.element(document.body))
                       .title('Sign In Notification')
                       .content('Email or password is not correct!')
                       .ariaLabel('')
                       .ok('ok')
                     );
                  } else {
                     $scope.logedin = true;
                     User.signedoff = false;
                  }
                  $scope.$apply();
               });
           };

           $scope.$watch(function(){return User.signedoff}, function (signedoff) {
               if(signedoff){
                  $scope.logedin = false;
                  $scope.password = undefined;
               }
           });
        },
        link: function (scope, element) {

        }
    };
});
