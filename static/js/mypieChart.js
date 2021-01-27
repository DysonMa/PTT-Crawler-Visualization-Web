
var w = 600
var h = 400
var p = 100
var bar_w = 50
var bar_p = 15

// console.log(boardName)

svg();
bind(data);
render();
bind_pie_data(data);
render_pie(data);

//繪圖區
function svg() {
    d3.select("#barChart")
        .append("svg")
        .attr({
            width: w,
            height: h,
        })
    
    d3.select("#pieChart")
        .append("svg")
        .attr({
            width: w,
            height: h,
        })
}

//綁定資料
function bind(data) {
    //rect
    var selection = d3.select("#barChart>svg")
        .selectAll("rect")
        .data(data);

    selection.enter().append("rect");
    selection.exit().remove();


    //text
    var selection_text = d3.select("#barChart>svg")
        .selectAll("text")
        .data(data);

    selection_text.enter().append("text");
    selection_text.exit().remove();
}

//渲染
function render() {
    //rect
    d3.selectAll("rect")
        .transition()
        .attr({
            x: (d, i) => {
                return p + bar_p + (bar_w + bar_p) * i;
            },
            y: (d, i) => {
                return h - p - d;
            },
            width: bar_w,
            height: (d) => {
                return d
            },
            fill: (d)=>{
                if (d>100){
                    return "lightgreen";
                }
                else{
                    return "red";
                }
            },
            "id": (d, i)=>{
                return boardName[i];
            }
        })
      

    //text
    d3.selectAll("text")
    // .transition()
        .attr({
            x: (d, i) => {
                return p + bar_p + (bar_w + bar_p) * i + bar_w / 2 - 8;
            },
            y: (d, i) => {
                return h - p - d - 5;
            },
            "font-size": 15
        })
        .text((d) => {
            return d
        })

    // axis
    var xScale = d3.scale.linear()
        .domain([0, data.length-1])
        .rangeRound([0, w-2*p])

    var yScale = d3.scale.linear()
        .domain([d3.min(data), d3.max(data)])
        .range([h-p, 0])

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(7)
        .tickFormat((d)=>{
            return boardName[d];
        })
    
    var yAxis = d3.svg.axis()
        .scale(yScale)
        .orient("left")
        .ticks(7)
        .tickFormat((d)=>{
            return d+"個";
        })

    d3.select("#barChart>svg")
        .append("g")
        .classed("axis", true)
        // .transition()
        .attr("transform", "translate("+(p)+"," + (h - p) + ")")
        .call(xAxis);

    d3.select("#barChart>svg")
        .append("g")
        .classed("axis", true)
        // .transition()
        .attr("transform", "translate("+(p)+", 0)")
        .call(yAxis);

    // bind(boardName)
    // d3.select("#barChart>svg")
    //     .append("text")
    //     .attr({
    //         // "text-anchor": "middle",
    //         "font-size": 15,
    //         x: (d, i)=>{
    //             return p + bar_p + (bar_w + bar_p) * i + bar_w / 2 - 8;
    //         },
    //         y: (d, i)=>{
    //             return h - p - data[i] - 5;
    //         }
    //     })
    //     .text((d)=>{
    //         return d;
    //     })
    
}

function bind_pie_data(data){
    // 圓餅圖
    var pie = d3.layout.pie().value((d)=>{
        return d
    })

    var selection = d3.select("#pieChart>svg")
                        .selectAll("g.arc")
                        .data(pie(data));

    var g_arc = selection.enter().append("g").attr("class","arc");
    g_arc.append("path");
    g_arc.append("text");
    selection.exit().remove();
}

function render_pie(data){
    var outerR = 200;
    var innerR = 100;
    var arc = d3.svg.arc()
                .outerRadius(outerR)
                .innerRadius(innerR); 

    var fScale = d3.scale.category20();

    d3.selectAll("g.arc")
        // .transition()
        .attr("transform", "translate("+w/2+","+h/2+")")
        .select("path")
        .attr("d", arc)
        .style("fill", function(d,i) { return fScale(i); });
    
    d3.selectAll("g.arc")
        .select("text")
        .transition()
        .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })  //arc.centroid 計算並回傳此元素中心位置(重心)
        .attr({
            "text-anchor":"middle",
            // dy: 20,   //y的移動距離
            // dx: 20    //x的移動距離
        })
        .text(function(d, i){
            return boardName[i];    
        })

    // d3.selectAll('#pieChart g.arc path').on("mouseover", (d, i)=>{
    //     var posX = arc.centroid(d)[0]
    //     console.log(posX)
    //     var posY = arc.centroid(d)[1]
    //     console.log(posY)

    //     var tooltip = d3.select("#tooltip")
    //                     .style({
    //                         "left": (+posX)+"px",
    //                         "top": (+posY)+"px"
    //                     })

    //     tooltip.html(boardName[i]+"<br>"+d);
    //     tooltip.classed("hidden", false);

    //     // d3.select(this).attr({
    //     //     "stroke-width": 5
    //     // });
    // })
    // .on("mouseout", (d)=>{
    //     d3.select("#tooltip").classed("hidden", true);
    //     // d3.select(this).attr({
    //     //     "stroke-width": 1
    //     // })
    // })
}

