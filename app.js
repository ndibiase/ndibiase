// @TODO: YOUR CODE HERE!
// opacity 0.9
// text before circle


// Setting graph size and margins
// ==============================
var svgWidth = 960;
var svgHeight = 500;

var margin = {
    top: 50,
    right: 40,
    bottom: 80,
    left: 50
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;
// var padding = 25;
// var formartPercent = d3.format('.2%');

// Creating an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
// ==============================
var svg = d3
    .select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

// Appending an SVG group
// ==============================
var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);


// Importing Data
// ==============================
d3.csv("data.csv", function (err, allData) {
    if (err) throw err;

    // Parsing data as numbers
    // ==============================
    allData.forEach(function (data) {
        data.smokes = +data.smokes;
        data.age = +data.age;
    });

    // Creating scale functions
    // ==============================
    var xLinearScale = d3.scaleLinear()
        .domain([7, d3.max(allData, d => d.smokes)])
        .range([0, width]);

    var yLinearScale = d3.scaleLinear()
        .domain([25, d3.max(allData, d => d.age)])
        .range([height, 0]);


    // Creating axis functions
    // ==============================
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Appending Axes to the chart
    // ==============================
    chartGroup.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);

    chartGroup.append("g")
        .call(leftAxis);

    
    //  Adding state abbreviation
    // ==============================
    chartGroup.selectAll('text.stateText')
    .data(allData)
    .enter().append('text')
    .text(d => d.abbr)
    .attr('class', 'stateText')
    .attr('x', d => xLinearScale(d.smokes))
    .attr('y', d => yLinearScale(d.age - 0.25));

        
        
    // Creating Circles
    // ==============================
    var circlesGroup = chartGroup.selectAll("circle")
    .data(allData)
    .enter().append("circle")
    .attr('class', 'stateCircle')
    .attr("cx", d => xLinearScale(d.smokes))
    .attr("cy", d => yLinearScale(d.age))
    .attr("r", "15")
    .attr('opacity', '0.4');


    // Initializing tool tip
    // ==============================
    var toolTip = d3.tip()
        .attr("class", "d3-tip")
        .offset([80, -60])
        .html(function (d) {
            return (`<b><i>${d.state}</i></b><br>Smokers: ${d.smokes} %<br>Age: ${d.age} years`);
        });


    // Creating tooltip in the chart
    // ==============================
    chartGroup.call(toolTip);

    // Creating event listeners to display and hide the tooltip
    // ==============================
    circlesGroup.on("mouseover", function (data) {
        toolTip.show(data);    
    })
        // onmouseout event
        .on("mouseout", function (data, index) {
            toolTip.hide(data);   
        });

    // Creating axes labels
    // ==============================
    chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left )
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .attr("class", "axisText")
        .text("Age (Median)"); 

    chartGroup.append("text")
        .attr("transform", `translate(${width / 2}, ${height + margin.top - 10})`)
        .attr("class", "axisText")
        .text("Smokers (%)");



});

