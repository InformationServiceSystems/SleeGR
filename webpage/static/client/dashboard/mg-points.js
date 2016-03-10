function showPoints(chart){
  var args = chart.args;
  if(args.showPoints) {
    //console.log('show points: ', args.showPointsData);


    var svg = d3.select(args.target).select('svg');

    //d3.select(args.target).select(".line").remove();

    _.forEach(args.showPointsData, function(dataset, index){
      //console.log('args.showPointsData', dataset.length, index);
      svg.selectAll("circle"+index)
       .data(dataset)
       .enter()
       .append("circle")
       .attr("cx", function(d) {
         return args.scales.X(d.date);
       })
       .attr("cy", function(d) {
         return args.scales.Y(d.value);
       })
       .attr("r", 1)
       .attr('class', 'mg-line mg-line'+(index+1)+' mg-line'+(index+1)+'-color mg-points-'+(index+1))
       //.style("stroke-width", 2)
       .style("fill", "none");
       //.style("stroke", "red")//#05b378
       //.attr('stroke', '#db4437');
    });
  }
};

MG.add_hook('line.after_init', function(chart) {
    showPoints(chart);
});
