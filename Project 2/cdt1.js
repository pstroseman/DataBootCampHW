////Load "cdt.csv"

d3.csv("cdt.csv")
    .then(data => {
    console.log('=== SUCCESS ===');
    console.log(data);
    

//Convert "date strings" to dates using timeParse
//Convert "number strings" to numbers
    
    var tp = d3.timeParse('%m/%d/%Y');
    data.forEach (function (d) {
        d.Date = tp (d.Date);
        Object.keys(d).forEach (k => {
            if(["Date","Organization","District","Name of Collaborative","Name of Initiative"].includes(k)) {
                //console.log(`skipping ${k}`)
                return; 
            }
            console.log(k);
            d[k] = +d[k];
        })     
    })


//Summarize data: Mean calucations for Collective Vision variables
            
    var commUnderstanding = d3.mean(data, function(d) { return d["We have a common understanding of the challenges and barriers that are impacted the academic performances as well as the college and career success of students within our region"]; });
        
    var collVision = d3.mean(data, function(d) { return d["We have developed a collective vision that focuses our work and is designed to impact equity, access, and student achievement"]; });
        
    var defStudentOutcomes = d3.mean(data, function(d) { return d["We have defined student outcomes that are aligned to our collective vision"]; });
        
    var devPolicies = d3.mean(data, function(d) { return d["We have developed and instituted policies and procedures that allow us to monitor student outcomes"]; });
    
    var devStrategicPlan = d3.mean(data, function(d) { return d["We have developed (and routinely refine) a strategic plan that informs efforts to refine, sustain, and further develop our collective vision"]; });
        
    console.log(devStrategicPlan);
    console.log(devPolicies);
    console.log(defStudentOutcomes);
    console.log(collVision);
    console.log(commUnderstanding);


//NEST DATA//
    
    //Nest data by Name of Collaborarive

        var dataByCollaborativeName = d3.nest()
            .key(function(d) { return d["Name of Collaborative"]; })
            .rollup(function(v) {  
                return {
                  "Common understanding of challenges and barriers impacting students are defined":d3.mean(v, function(d) {
                    return d["We have a common understanding of the challenges and barriers that are impacted the academic performances as well as the college and career success of students within our region"];
                  }),
                  "Collective vision focuses on equity, access, and student achievement": d3.mean(v, function(d) {
                    return d["We have developed a collective vision that focuses our work and is designed to impact equity, access, and student achievement"];
                  }),
                    "Student outcomes are aligned to collective vision": d3.mean(v, function(d) {
                    return d["We have defined student outcomes that are aligned to our collective vision"];
                  }),
                    "Policies that allow us to monitor student outcomes have been developed": d3.mean(v, function(d) {
                    return d["We have developed and instituted policies and procedures that allow us to monitor student outcomes"];
                  }),
                    "A stragegic plan used to refine, sustain and develop our collective vision has been created": d3.mean(v, function(d) {
                    return d["We have developed (and routinely refine) a strategic plan that informs efforts to refine, sustain, and further develop our collective vision"];
                  })
                }; 
            })
            .entries(data);

        console.log(dataByCollaborativeName);
        console.table(dataByCollaborativeName.sort(function(a,b) { return b.values - a.values }));


    //FILTER
    var crimsonKey = 'Crimson';
    var filteredResult1 = dataByCollaborativeName.filter(obj => {
        console.log(obj.key);
       if (obj.key === crimsonKey) {
           return true;
       } 
    
      return false;
    });
    
    var onDropdownSelect = function() {

        var filterKey = d3.event.target.value;

        var filteredResult = dataByCollaborativeName.filter(obj => {
           if (obj.key === filterKey) {
               return true;
           } 

          return false;
        });
        
        createBarChart(filteredResult[0].value);
        console.log('filtered result is:');
        console.log(filteredResult[0].value);
    };
    
    d3.select('.dropdown1').on('change', onDropdownSelect);

//DEVELOP HORIZONTAL BAR CHART
    
    var createBarChart = function(data) {
    //Develop horizontal bar chart
    // set the dimensions and margins of the graph
  

    var svg = d3.select("svg"),
    margin = {top: 50, 
              right: 20, 
              bottom: 30, 
              left: 700},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
        
        
    svg.html('');
  
    var tooltip = d3.select("body").append("div").attr("class", "toolTip");
  
    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleBand().range([height, 0]);

    var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  

  
  	//data.sort(function(a, b) { return a.value - b.value; });
  
    //console.log(Object.keys(data));
  	x.domain([0, 6]);
    y.domain(Object.keys(data)).padding(0.1);

    g.append("g")
        .attr("class", "x axis")
       	.attr("transform", "translate(0," + height + ")")
      	.call(d3.axisBottom(x).ticks(5).tickFormat(function(d) { return parseInt(d); }).tickSizeInner([-height]));

    g.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(y));

    // { question_1: 3.3, question_2: 3.4 ... }
    g.selectAll(".bar")
        .data(Object.values(data))
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("height", y.bandwidth())
        .attr("y", function(d, i) {
          console.log('calculating y...');
          console.log(i);
          console.log(Object.keys(data)[i]);
          return y(Object.keys(data)[i]);
         })
        .attr("width", function(d) { return x(d); })
        .text(function(d) { return d; })
        .on("mousemove", function(d){
            tooltip
              .style("left", d3.event.pageX - 50 + "px")
              .style("top", d3.event.pageY - 70 + "px")
              .style("display", "inline-block")
              .html("<body>" + d + "</body>");
        })
    		  .on("mouseout", function(d){ tooltip.style("display", "none");});
        
    g.selectAll('.label')
        .data(Object.values(data))
        .enter().append("text")
        .attr("class", "label")
        .attr("x", 0)
        .attr("height", y.bandwidth())
        .attr("y", function(d, i) {
          console.log('calculating y...');
          console.log(i);
          console.log(Object.keys(data)[i]);
          return y(Object.keys(data)[i]);
         })
        .attr("width", function(d) { return x(d); })
        .text(function(d) { return d; })
    };
    
    createBarChart(filteredResult1[0].value);
    
//Catch errors and give error codes in the conole
})
    .catch(err => {
    console.log('=== ERROR ===');
    console.log(err);
})

