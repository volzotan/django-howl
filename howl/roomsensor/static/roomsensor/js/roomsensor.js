
function prepare_and_draw(sensorname, datapoints, compression_factor) {
  $(".graph-container-" + sensorname).removeClass("stats");
  $(".graph-container-" + sensorname).addClass("busy");

  var rawdata;
  var context = cubism.context()
                      .step(compression_factor * 6e4) // Distance between data points in milliseconds // 6e4 = 1min
                      .size(datapoints)     // Number of data points (actually 1440 / 2 = 720, but our content width is 700px)
                      .stop();       // Fetching from a static data source; don't update values


  $.getJSON("/roomsensor/" + sensorname + "/rawdata/" + datapoints + "/" + compression_factor + "/", function(json) {
    rawdata = json.reverse();
    $(".graph-container-" + sensorname).removeClass("busy");
    $(".graph-container-" + sensorname).removeClass("stats");
    
    if (settings["ruler"] == true) {
      d3.select(".graph-container").append("div") // Add a vertical rule
      .attr("class", "rule")              // to the graph
      .call(context.rule());
    }

    if (settings["timeline"] == true) {
      d3.select(".graphs-" + sensorname) // Select the div on which we want to act           
      .selectAll(".axis")                // This is a standard D3 mechanism to
      .data(["top"])                     // bind data to a graph. In this case
      .enter()                           // we're binding the axes "top" and "bottom".
      .append("div")                     // Create two divs and 
      .attr("class", function(d) {       // give them the classes
        return d + " axis";              // top axis and bottom axis
      })                                 // respectively 
      .each(function(d) {                // For each of these axes,
        d3.select(this)                  // draw the axes with 4 intervals
          .call(context.axis()           // and place them in their proper places
          .ticks(8).orient(d)); 
      });
    }

    draw_graph(["luminosity", "temperature", "humidity"], sensorname);
  })
  .fail(function() { // json request fails
    $(".graph-container-" + sensorname).removeClass("busy");
    $(".graph-container-" + sensorname).removeClass("stats");
    $(".graph-container-" + sensorname).addClass("failed");
  });

  function create_metric(name) {
    var values = [];
    return context.metric(function(start, stop, step, callback) {
      start = +start, stop = +stop;

      rawdata.forEach(function(d) {
        values.push(d[name]); 
      }); 

      callback(null, values);
    }, " ");
  }


  function draw_graph(graph_list, sensorname) {
    graph_list.forEach(function(graph) {
      d3.select(".graphs-" + sensorname).call(function(div) {
        div.datum(create_metric(graph));

        div.append("div")
           .attr("class", "horizon")
           .insert("div", ".bottom")
           .call(context.horizon()
        // .format(d3.format("+,.2p"))          // Format the values to floating point percentage
           .height(settings[graph]["height"])                        // graph height (default 30px)
           .colors(settings[graph]["colors"])   // two colors -> 1 band graph (1 color positive, 1 color negative)
           .extent(settings[graph]["extent"])); 
      });

    });
  }

}
