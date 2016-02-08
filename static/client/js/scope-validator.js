var validateScope = (function(){
  var getValue = function(anchor){
    return function(){
      return anchor.val();
    };
  };

  var listen = function(state, validator){
    return function(listener){
      listener(state.input, validator.validate);
      return validator;
    };
  };

  var inputIsValid = function(state, validation){
    return function(){
      state.valid = validation(state.input.val());
      return state.valid;
    };
  };

  var emptyInput = function(input){
    return function(){
      input.val('');
    };
  };

  var InputValidation = function(selector, anchor, validation){
    var state = {
      name: selector,
      input: anchor.find('#'+selector),
      valid: false
    };

    var empty = emptyInput(state.input);

    var validator = {};
    validator.val = getValue(state.input);
    validator.validate = inputIsValid(state, validation);
    validator.listen = listen(state, validator);
    validator.valid = function(){
      return state.valid;
    };
    validator.clear = function(){
      empty();
      validator.validate();
    };

    return validator;
  };

  var getValueBy = function(collection){
    return function(selector){
      return collection[selector];
    };
  };

  var pushInputsTo = function(collection, anchor){
    return function(selector, validation){
      var input = InputValidation(selector, anchor, validation);
      collection[selector] = input;
      return input;
    };
  };

  var isFormValid = function(state){
    return function(isValid){
      var valid = true;
      _.forOwn(state.inputs, function(input){
        if(input.valid() === false){
          valid = false;
          return false
        }
      });
      return valid;
    };
  };

  var getValues = function(inputs){
    return function(){
      var values = {};
      _.forOwn(inputs, function(input, name){
        values[name] = input.val();
      });
      return values;
    };
  };

  var clearInputs = function(inputs){
    return function(){
      _.forOwn(inputs, function(input){
        input.clear();
      });
    };
  };

  var FormValidation = function(selector){
    var state = {
      anchor: jQuery('#'+selector),
      inputs: {}
    };

    var clear = clearInputs(state.inputs);
    var scope = {
      get: getValueBy(state.inputs),
      push: pushInputsTo(state.inputs, state.anchor),
      valid: isFormValid(state),
      values: getValues(state.inputs),
      clear: function(){
        clear();
        scope.valid();
      }
    };

    return scope;
  };

  return function(selector){
    return FormValidation(selector);
  };
}());
