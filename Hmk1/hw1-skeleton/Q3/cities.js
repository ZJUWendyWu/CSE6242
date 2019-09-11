import { 
  select, 
  csv, 
  scaleLinear, 
  max, //find max in an array for domain
  scaleBand, 
  axisLeft, 
  axisBottom, //put axis at bottom
  format //number formatting for axes
} from 'd3';

const svg = select("svg");  
svg.style("background-color", "pink");

//Establish panel params, h&w defined as attributes in index.html
const height = parseFloat( svg.attr('height') ); 
const width = +svg.attr('width'); //extract as a float 

//Function to produce a bar per row DOM elements
const makeBar = data => {
  const xValue = d => d.Population; //function access for reuse
  const yValue = d => d.City; //function access for reuse
  const margin = {left: 200, right: 20, top: 40, bottom: 120};
	const innerWidth = width - margin.left - margin.right;
	const innerHeight = height - margin.top - margin.bottom;
  const titleMargin = 10 //distance of the title from the top
  
  const xScale = scaleLinear() //scale the bars as horizontal bar chart
  	.domain( [0, max(data, xValue)]) //find min and max
		.range( [0, innerWidth] ) //max width of bar is the screen - margins
  //console.log(xScale.range());
        
  const yScale = scaleBand() //seperate for each country
  	.domain(data.map(yValue))
  	.range( [0, innerHeight] )
	  .padding(0.1) //set a space between bars
	//console.log(yScale.range());

  const barGroup = svg.append('g') //create group to position all bars
  	.attr('transform', `translate( ${margin.left}, ${margin.top})`)

	//Function to format x Axis 
  const xAxisTickFormat = number => format('.3s')(number)
  	.replace('G', 'B'); //replace G with billion
  
  const xAxis = axisBottom(xScale)
  	.tickFormat(xAxisTickFormat) // 3significant digits
  	.tickSize(-innerHeight) //draw ticks through the bars  
  
  //create group element for left axis (y)
  //NB selectAll selects more than one attribute from DOM
  const yAxisGroup = barGroup.append('g').call( axisLeft(yScale) )  
	//Remove the domain path and ticks at the left side
  yAxisGroup.selectAll('.domain, .tick line').remove()
	
  //Add y axis label
	yAxisGroup.append('text')
  	.attr('class', 'yAxisLabel') //set a class for ref in styles
   	.attr("transform", "rotate(-90)") //rotate 90 degrees
  	.attr('y', -170) //Shift down trial and error
  	.attr('x', -150) //Shift down trial and error
    .text(`City (metro)`)	 
    
	//create group element for bottom axis (x)
  const xAxisGroup = barGroup.append('g').call( xAxis )  
  	.attr('transform', `translate( 0, ${innerHeight})`) //move bottom axis down

  //Rotate axis labels DOESNT ENABLE AXIS TITLE
//		.selectAll("text")	  //Rotate labels on x Axis
//        .style("text-anchor", "end")
//        .attr("dx", "-.8em")
//        .attr("dy", ".15em")
//  			.attr("transform", function (d) {
//	        return "rotate(-30)";
//        });
  
  //Remove the domain path: personal preference
	//xAxisGroup.selectAll('.domain').remove()
  
  //Add x axis label
	xAxisGroup.append('text')
  	.attr('class', 'xAxisLabel') //set a class for ref in styles
  	.attr('y', innerHeight/4) //Shift down
  	.attr('x', innerWidth/2.5) //Centre
    .text(`Population in metro`)	 
  
	barGroup.selectAll('rect').data(data) //none initially but required to make data join
  	.enter().append('rect') //creates rectangle per row of data
  		.attr('width', d => xScale(xValue(d))) //can inspect DOM and see rect with different widths
			.attr('y', d => yScale(yValue(d)))
    	.attr('height', yScale.bandwidth()) //computed width of single bar

	//Insert a title for the bar chart
  barGroup.append('text')
  	.attr('class', 'titleLabel') //set a class for ref in styles
    .attr('y', -titleMargin) //Shift down
//  	.attr('font-size', '3em')
  	.attr('fill', '#635F5D')
  	.text(`World's 10 most populous cities`) //must use string literals with '
};
 
csv('worldData.csv').then(data => { //takes headings as keys
	data.forEach(rowElement => {
  	rowElement.Population = +rowElement.Population*1000 //convert to float
  });
  makeBar(data); 
});