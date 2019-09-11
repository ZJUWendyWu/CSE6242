var dataset = [ 5, 10, 15, 20, 25 ];
var width = 600;
var height = 400;
var barPadding = 2;
var svg = d3.select("body").append("svg")
            .attr("width", width)
            .attr("height", height);
var draw = function(d) {
    var yScale = d3.scaleLinear()
                   .domain([0, d3.max(d, function(d) {return d.running_total})])
                   .range([0, height]);
    var xScale = d3.scaleLinear()
                   .domain([d3.min(d, function(d) {return d.year}), d3.max(d, function(d) {return d.year})])
                   .range([0, width]);
    // draw bars
    svg.selectAll("rect")
       .data(d)
       .enter()
       .append("rect")
       .attr("x", function(d, i) {
            return xScale(d.year);
        })
        .attr("y", function(d) {
            return height - yScale(d.running_total);  //Height minus data value
        })
       .attr("width", width / dataset.length - barPadding)
       .attr("height", function(d) {
            return yScale(d.running_total);
        })
        .attr("fill", "teal");

    // add tittle tag
    // svg.selectAll("text")
    //    .append("text")
    //    .text("Lego Sets by Year from Rebrickable")
    //    .attr("x", )
    //    .attr("y",)
    //    .attr("font-family", "sans-serif")
    //    .attr("font-size", "18px")
    
    // add X and Y axis
}
var dataset;
var rowConverter = function(d) {
    return {
        year: d.year, // may need time parsing/ formatting 
        running_total: +d.running_total
    };
};

d3.dsv(",", "q3.csv", rowConverter).then(function(data) {
    dataset = data;    //Once loaded, copy to dataset.
    //dataset.sort(function(a, b) {return a.year - b.year;});
    console.log(dataset);
    //draw(dataset);
});