var application = (function(){
  var production = false;
  var routing = {
    auth: {
      signup: '',
      signin: ''
    }
  };

  /*var pubsub = function(){
    var topics = {};
    var hOP = topics.hasOwnProperty;
    return {
      subscribe: function(topic, listener) {
        if(!hOP.call(topics, topic)) topics[topic] = [];
        var index = topics[topic].push(listener) -1;
        return {
          remove: function() {
            delete topics[topic][index];
          }
        };
      },
      publish: function(topic, info) {
        if(!hOP.call(topics, topic)) return;
        topics[topic].forEach(function(item) {
        	item(info != undefined ? info : {});
        });
      }
    };
  };*/

  var emailTester = /^[-!#$%&'*+\/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-?\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$/;
  function validateEmail(email){
  	if (!email)
  		return false;

  	if(email.length>254)
  		return false;

  	var valid = emailTester.test(email);
  	if(!valid)
  		return false;

  	var parts = email.split("@");
  	if(parts[0].length>64)
  		return false;

  	var domainParts = parts[1].split(".");
  	if(domainParts.some(function(part) { return part.length>63; }))
  		return false;

  	return true;
  };

  var notEmptyText = function(value){
    var errors = [];
    if(value === ''){
      errors.push('Required field is empty.');
    }
    return (errors.length === 0) ? true : errors;
  };

  var notValidEmail = function(value){
    var errors = [];
    if(value === ''){
      errors.push('Required field is empty.');
    }
    if(validateEmail(value) === false){
      errors.push('Sry, it seems to be not a valid email.');
    }
    return (errors.length === 0) ? true : errors;
  };

  var createAuth = function(){
    var user = {
      email: 'stehle.andre@gmail.com',
      password: '123456'
    };

    function signup(profile, success){
      jQuery.getJSON(routing.auth.signup)
        .success(function(response){
          _.merge(user, profile);
          success();
        })
        .fail(function(err) {

        });
    };

    function signin(values, success){
      jQuery.getJSON(routing.auth.signin)
        .success(function(response){
          if(response.authenticated){
            success();
          }
        })
        .fail(function(err) {

        });
    };

    return {
      set: function(profile, success){
        if(production){
          signup(profile, success);
        } else {
          _.merge(user, profile);
          success();
        }
      },
      get: function(){
        return user;
      },
      is: function(values, success){
        if(production){
          signin(values, success);
        } else {
          if((values.email === user.email) && (values.password === user.password)){
            success();
          }
        }
      }
    };
  };

  var auth = createAuth();
  var recaptchaSuccess;
  var regestrationCaptchaId;
  var onloadCallback = function() {
    regestrationCaptchaId = grecaptcha.render('recaptcha', {
      sitekey : '6LcWnRUTAAAAALoF5HxCrB3wDJGubExCKqV6oG2r',
      callback: function(){
        recaptchaSuccess();
      }
    });
  };

  var createInputValidationHandler = function(input){
    var wrapper = input.parent();
    var errorBox = input.next('div');
    return function (reply){
      if(reply === true){
        errorBox.hide();
        wrapper.removeClass('has-error');
      } else {
        errorBox.show();
        errorBox.text(reply[0]);
        wrapper.addClass('has-error');
      }
    };
  };

  var registration;
  jQuery(document).ready(function(){
    registration = validateScope('registration');

    function isHuman(){
      return grecaptcha.getResponse(regestrationCaptchaId) !== '';
    };

    var submit = jQuery('#submitRegistration');

    submit.click(function(event){
      event.preventDefault();
      auth.set(registration.values(), function(){
        loginSuccess();
      });
    });

    recaptchaSuccess = function(){
      if(registration.valid() && isHuman()){
        submit.removeAttr('disabled');
      } else {
        submit.attr('disabled', 'true');
      }
    };

    var keyup = function(input, validate){
      var errorHandler = createInputValidationHandler(input);
      input.bind('keyup change', function(){
        errorHandler(validate());
        if(registration.valid() && isHuman()){
          submit.removeAttr('disabled');
        } else {
          submit.attr('disabled', 'true');
        }
      });

      submit.parent().mouseover(function(){
        errorHandler(validate());
      });
    };

    var fname = registration.push('fname', notEmptyText).listen(keyup);
    var pname = registration.push('pname', notEmptyText).listen(keyup);
    var email = registration.push('email', notValidEmail).listen(keyup);

    var passwordLength = 5;
    var password = registration.push('password', function(value){
      var errors = [];
      if(value === ''){
        errors.push('Please, type');
      }
      if(value.length < passwordLength){
        errors.push('Sry, the password should be at least '+passwordLength+' chars long.');
      }
      return (errors.length === 0) ? true : errors;
    }).listen(keyup);

    var passwordConfirm = registration.push('passwordValidation', function(value){
      var errors = [];
      if(value === ''){
        errors.push('Please, confirm your password.');
      }
      if(value !== password.val()){
        errors.push('Sry, your input is not equal to your password.');
      }
      return (errors.length === 0) ? true : errors;
    }).listen(keyup);

    /*setTimeout(function(){
      console.log(registration.valid());
    }, 1000);*/
  });

  var signinCaptchaSolved;
  var signinCaptchaId;
  var signinOnloadCallback = function() {
    signinCaptchaId = grecaptcha.render('recaptcha-signin', {
      sitekey : '6LcWnRUTAAAAALoF5HxCrB3wDJGubExCKqV6oG2r',
      callback: function(){
        console.log('sign in recaptcha solved!');
        signinCaptchaSolved();
      }
    });
  };

  var signin;
  jQuery(document).ready(function(){
    signin = validateScope('signin');

    function isHuman(){
      return grecaptcha.getResponse(signinCaptchaId) !== '';
    };

    var submit = jQuery('#submit-signin');

    submit.click(function(event){
      event.preventDefault();
      var values = signin.values();
      auth.is({
          email: values.email,
          password: values.password
        },
        function(){
          loginSuccess();
        }
      );
    });

    signinCaptchaSolved = function(){
      if(signin.valid() && isHuman()){
        submit.removeAttr('disabled');
      } else {
        submit.attr('disabled', 'true');
      }
    };

    var keyup = function(input, validate){
      var errorHandler = createInputValidationHandler(input);
      input.bind('keyup change', function(){
        errorHandler(validate());

        if(signin.valid() && isHuman()){
          submit.removeAttr('disabled');
        } else {
          submit.attr('disabled', 'true');
        }
      });

      submit.parent().mouseover(function(){
        errorHandler(validate());
      });
    };

    var email = signin.push('email', notValidEmail)
      .listen(keyup);
    var password = signin.push('password', notEmptyText)
      .listen(keyup);
  });

  var headerSignUp = jQuery('#signup-btn');
  var registrationBox = jQuery('#registration-box');

  var headerSignIn = jQuery('#signin-btn');
  var signinBox = jQuery('#signin-box');

  var metricsChartsBox = jQuery('#metrics-charts');

  headerSignUp.click(function(){
    registrationBox.show();
    signinBox.hide();
    metricsChartsBox.hide();
  });

  headerSignIn.click(function(){
    registrationBox.hide();
    signinBox.show();
    //metricsChartsBox.show();
  });

  function loginSuccess(){
    signinBox.hide();
    registrationBox.hide();
    metricsChartsBox.show();
    registration.clear();
    signin.clear();
    jQuery('#submitRegistration').attr('disabled', 'true');
    jQuery('#submit-signin').attr('disabled', 'true');
  };


  //charts

  function growth(downloads){
    var past = downloads[0]['downloads'];
    return downloads.reduce(function(rates, point, index){
      rates.push(point.downloads/past*100);
      past += point.downloads;
      return rates;
    }, []);
  };

  function growthByDif(values){
    var past = values[0];
    return values.reduce(function(rates, point, index){
      if(index !== 0){
        rates.push(point/past);
        past += point;
      }
      return rates;
    }, [0]);
  };

  function downloadsGrowthByDif(downloads){
    var past = downloads[0]['downloads'];
    return downloads.reduce(function(rates, point, index){
      if(index !== 0){
        rates.push(point.downloads/past);
        past += point.downloads;
      }
      return rates;
    }, [0]);
  };

  function requestDownloads(name){
    var url = 'https://api.npmjs.org/downloads/range/2012-01-03:2016-01-16/'+encodeURIComponent(name);
    jQuery.getJSON(url)
      .success(function(response){
        if(response.downloads){
          plot(response);
          plotGrowth(response);
        }
      })
      .fail(function(err) {

      });
  };

  function plotGrowth(info){
    //var rate = growth(info.downloads);
    var rate = downloadsGrowthByDif(info.downloads);
    var data = info.downloads.map(function(point, index){
      point.rate = rate[index]*100;
      return point;
    });
    MG.data_graphic({
      title: "Other Linked Graphic",
      description: "Roll over and watch as the graphic to the left triggers.",
      data: data,
      area: false,
      linked: true,
      full_width: true,
      xax_count: 4,
      target: document.getElementById('package-downloads-growthrate'),
      x_accessor: 'day',
      y_accessor: 'rate'
    });
  };

  function plot(info){
    var data = info.downloads;
    MG.convert.date(data, 'day', '%Y-%m-%d');
    MG.data_graphic({
      title: info.package,
      description: "dowloads of last month",
      data: data,
      full_width: true,
      target: document.getElementById('package-downloads'),
      x_accessor: 'day',
      y_accessor: 'downloads'
    });
  };

  /*jQuery(document).ready(function(){
    var input = jQuery('#package-needle');
    requestDownloads('gulp');
    input.keyup(function(event){
      var code = event.keyCode || event.which;
      if(code == 13) {
         var query = input.val();
         requestDownloads(query);
      }
    });
  });*/

  return {
    recaptchaReady: function(){
      onloadCallback();
      signinOnloadCallback();
    }
  }
}());

var recaptchaReady = application.recaptchaReady;
