function simpleBar(data, xval, title, chartID) {
    /*
    Inputs
    data - data to draw in [{'x': x, 'value': y, 'source': source}] format
    dims - dict of dimensions for the chart which should be in the format - 
    {width: 423, height: 160, top: 40, right: 20, bottom: 60, left: 40, 
        hoverOffsetX : (amount to offset hovercard along x axis), hoverOffsetY: (amount to offset hovercard along y axis)}
    title - title of the chart
    chartID - HTML id of the chart in the HTML template
    notes - notes for the chart
    */
   var dims = {width: 843, height: 160, top: 40, right: 20, bottom: 60, left: 40, hoverOffsetX: 0, hoverOffsetY: -200}

    // Set up dimensions
    var width = dims.width - dims.left - dims.right;
    var height = dims.height - dims.top - dims.bottom;

    console.log(chartID);

    // Create SVG element
    var svg = d3.select("#" + chartID)
    .append("svg")
    .attr("width", width + dims.left + dims.right)
    .attr("height", height + dims.top + dims.bottom)
    .append("g")
    .attr("transform", "translate(" + dims.left + "," + dims.top + ")");

    // Add title
    svg.append("text")
        .attr("class", "chart-title")
        .attr("x", 5)
        .attr("y", -dims.top / 1.5) // Adjust the multiplier to change the gap
        .text(title);

    // Create a scale for the x-axis
    var xScale = d3.scaleBand()
        .domain(data.map(function(d) { return d[xval]; }))
        .range([0, width])
        .padding(0.1);
    

    // Create a scale for the y axis 
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d.value; })])
        .nice()
        .range([height, 0]);
    

    var bars = svg.selectAll(".bar-overlay")
        .data(data)
        .enter().append("a")
        .attr("class", "bar-overlay")
        .attr("x", function(d) { return xScale(d[xval]); })
        .attr("y", function(d) { return yScale(d.value); })
        .attr("width", xScale.bandwidth())
        .attr("height", height) 
        .style("bottom", function(d) { return (dims.bottom) + "px"; })
        .style("left", function(d) { return (xScale(d[xval]) + dims.left) + "px"; })
        .on("mouseover", function(event, d) {
            hovercard.style("opacity", "1")
            .text(d[xval] + ": " + d.value)
            .style("left", (event.pageX + dims.hoverOffsetX) + "px") // Adjust the left position
            .style("top", (event.pageY + dims.hoverOffsetY) + "px"); // Adjust the top position

        })
        .on("mousemove", function(event) { // Update hovercard position on mousemove
            hovercard.style("left", (event.pageX + dims.hoverOffsetX) + "px") // Adjust the left position
            .style("top", (event.pageY + dims.hoverOffsetY) + "px"); // Adjust the top position
        })
        .on("mouseout", function() {
            hovercard.style("opacity", 1e-6);
        });

        // Add hovercard
    var hovercard = d3.select(chartID).append("div")
        .attr("class", "hovercard")
        .style("opacity", 1e-6); // Initially hide hovercard
    
    // Actual bars
    bars.append("rect")
        .attr("class", "income-bar")
        .attr("x", function(d) { return xScale(d[xval]); })
        .attr("y", function(d) { return yScale(d.value); })
        .attr("width", xScale.bandwidth())
        .attr("height", function(d) { return height - yScale(d.value); });
    
    // Add year labels
    bars.append("text")
        .attr("class", "x-label")
        .attr("x", function(d) { return xScale(d[xval]) + xScale.bandwidth() / 1.5; })
        .attr("y", height + dims.bottom / 3)
        .attr("dy", "0.35em")
        .text(function(d) { return d[xval]; });

    // Add value labels
    data.map(function(d) { 
        console.log(xScale(d[xval]));
        console.log(yScale(d.value));
    })

    
    
    
    // bars.append("text")
    //     .attr("class", "col-label")
    //     .attr("x", function(d) { return xScale(d.x) + xScale.bandwidth() / 1.5; })
    //     .attr("y", function(d) { return yScale(d.value) - 5; })
    //     .attr("dy", "0.25em")
    //     .text(function(d) { return d.value; });
    
};

