function createEvaluator(funcAsString){
  var code = math.compile(funcAsString);
  return function(scope){
    return code.eval(scope);
  };
};

function createInterpolationOn(evaluate, render){
  if(_.isUndefined(render)){
    return function(scopes){
      return _.map(scopes, evaluate);
    };
  }

  return function(scopes){
    return _.map(scopes, function(scope){
      return render(scope, evaluate(scope));
    });
  };
};

//console.log(interpolate([{ x: 8 }, { x: 12 }, { x: 14 }]));

function draw(chart){
  var args = chart.args;
  //console.log('args', args.mf, args.data, args);
  if(_.isUndefined(args.mf)) {
    d3.select(args.target).select(".line").remove();
    return;
  }

  //console.log(args.data[0]['length']);
  var ray = _.map(args.data[0], function(item, index){
    return { x: index+1 };
  });

  var evaluate = createEvaluator(args.mf);
  var interpolate = createInterpolationOn(evaluate, function(scope, value){
    return [scope.x, value];
  });
  //console.log(evaluate({ x: 8 }));
  var mfValues = interpolate(ray);

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  /*var x = d3.time.scale()
    .range([0, width]);
  var y = d3.scale.linear()
    .range([height, 0]);*/

  //console.log(args.scales.X);

  var line = d3.svg.line()
    .x(function(d) { return args.scales.X(d.date); })
    .y(function(d, index) {
      //console.log(d, index, mfValues[index][1]*800);
      return args.scales.Y(mfValues[index][1]*10-5);
      //return mfValues[index][1];
    });
    //.y(function(d) { return args.scales.Y(d.value); })
    //.y(function(d) { return args.scales.Y(70); return args.scales.Y(d.value); });

  var data = args.data[0];

  var svg = d3.select(args.target).select('svg');

  d3.select(args.target).select(".line").remove();

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
};

MG.add_hook('line.after_init', function(chart) {
    //console.log("chart:", chart);
    draw(chart);
});
