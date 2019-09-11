var dataset = [ 5, 10, 15, 20, 25 ];
var width = 900;
var height = 400;
var padding = 40;
var innerWidth = width - padding * 2;
var innerHeight = height - padding * 2;
var barPadding = 2;
var svg = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height);

var draw = function(d) {
    console.log("draw");
    var yScale = d3.scaleLinear()
                   .domain([0, d3.max(d, function(d) {return d.running_total})])
                   .range([0, innerHeight]);
    var xScale = d3.scaleTime()
                   .domain(d3.extent(dataset, function(d) {
                    return d.year;
                }))
                   .range([padding, width - padding - innerWidth / d.length]);
    // draw bars
    svg.selectAll("rect")
       .data(d)
       .enter()
       .append("rect")
       .attr("x", function(d, i) {
            return xScale(d.year);
        })
        .attr("y", function(d) {
            return height - yScale(d.running_total) - padding;  //Height minus data value
        })
       .attr("width", innerWidth / d.length - barPadding)
       .attr("height", function(d) {
            return yScale(d.running_total);
        })
        .attr("fill", "teal");
    
    // draw axis
    var xAxis = d3.axisBottom(xScale).ticks(d.length / 4);
    svg.append("g")
       .attr("class", "axis")
       .attr("transform", "translate(0" + "," + (innerHeight + padding) + ")")
       .call(xAxis);
    var yScale = d3.scaleLinear()
       .domain([0, d3.max(d, function(d) {return d.running_total})])
       .range([innerHeight, 0]);
    var yAxis = d3.axisLeft(yScale);
    svg.append("g")
       .attr("class", "axis")
       .attr("transform", "translate("+ padding + "," + padding + ")")
       .call(yAxis);
    
    // add title
    svg.append("text")
       .attr("transform", "translate(" + (width/2) + "," + padding + ")")
       .style("text-anchor", "middle")
       .text("DateLego Sets by Year from Rebrickable");
};

// retrieve data
var dataset;
var parseTime = d3.timeParse("%Y");
var rowConverter = function(d) {
    return {
        year: parseTime(d.year), // may need time parsing/ formatting 
        running_total: +d.running_total
    };
};

d3.dsv(",", "q3.csv", rowConverter).then(function(data) {
    dataset = data;    //Once loaded, copy to dataset.
    dataset.sort(function(a, b) {return a.year < b.year ? 1 : -1;});
    console.log(dataset);
    draw(dataset);
});