// set initial latitude, longitude and zoom level
lat = 30.2672;
lng = -97.7431;
zoomLevel = 13;
//apiURL = 'http://ec2-52-20-232-151.compute-1.amazonaws.com:8080/v1/'
apiURL = 'http://localhost:8080/v1/'
// setup a marker group

var HouseIcon = L.Icon.extend({
    options:{
        iconSize:     [24, 24], // size of the icon
        iconAnchor:   [12, 12], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -26] // point from which the popup should open relative to the iconAnchor
    }
});
var HouseIconBig = L.Icon.extend({
    options:{
        iconSize:     [32, 32], // size of the icon
        iconAnchor:   [16, 16], // point of the icon which will correspond to marker's location
        popupAnchor:  [0, -26] // point from which the popup should open relative to the iconAnchor
    }
});

var redIcon = new HouseIcon({iconUrl: 'images/redIcon.png'}),
    orangeIcon = new HouseIcon({iconUrl: 'images/orangeIcon.png'}),
    greenIcon = new HouseIcon({iconUrl: 'images/greenIcon.png'});

var redIconBig = new HouseIconBig({iconUrl: 'images/redIcon.png'}),
    orangeIconBig = new HouseIconBig({iconUrl: 'images/orangeIcon.png'}),
    greenIconBig = new HouseIconBig({iconUrl: 'images/greenIcon.png'});

// function to set the sizes of div's
function initContent() {
    // get document width and height
    docWidth = $(window).width();
    docHeight = $(window).height();

    // add and size nav div
    $("body").append("<div id='nav'></div>");
    $("#nav").width(docWidth).height(docHeight/17);
    $("#nav").append("<div id='logo'></div>");
    $("#logo").width(docHeight/5).height(docHeight/20);

    // add and size map div
    $("body").append("<div id='mapid'></div>");
    $("#mapid").width(docWidth*0.98).height(docHeight*0.9);
    $("#mapid").css("marginLeft", docWidth*0.01);

    // add filter
    $("#nav").append("<div id='searchMenu'></div>");
    $("#searchMenu").width(docHeight*4/5).height(docHeight/20);

    // add finance filter
    $("#searchMenu").append("<div id='finance'><h4>Cash</h4></div>");
    $("#finance").append("<label id='financeSwitch'></label>")
    $("#finance").height(docHeight/20);
    $("#finance").append("<h4>Finance</h4>");
    $("#financeSwitch").append("<input type='checkbox' id='financeSlider'>");
    $("#financeSwitch").append("<span class='slider round'></span>");
    $("#financeSlider").change(function (e) {
        refreshMarkers();
    });

    // add max price filter
    $("#searchMenu").append("<div id='maxPrice'></div>");
    $("#maxPrice").height(docHeight/20);
    $("#maxPrice").append("<input type='number' id='priceButton' name='price' min='1000' max='10000000' placeholder='Any Price'>");
    $("#priceButton").on("keydown", event => {
        if (event.which == 13) {
            $("#priceButton").blur();
            refreshMarkers();
        }
    });
    $("#priceButton").focusout(function() {
        refreshMarkers();
    });

    // add max price filter
    $("#searchMenu").append("<div id='downPayment'></div>");
    $("#downPayment").height(docHeight/20);
    $("#downPayment").append("<input type='number' id='cashButton' name='cash' min='0' max='10000000' placeholder='Down Payment'>");
    $("#downPayment").on("keydown", event => {
        if (event.which == 13) {
            $("#downPayment").blur();
            refreshMarkers();
        }
    });
    $("#downPayment").focusout(function() {
        refreshMarkers();
    });
}

function resizeContent() {
    // size nav div
    $("#nav").width(docWidth).height(docHeight/17);
    $("#logo").width(docHeight/5).height(docHeight/20);
    // size map div
    $("#mapid").width(docWidth*0.98).height(docHeight*0.9);
    $("#mapid").css("marginLeft", docWidth*0.01);
}

function initMap() {
    // create map element
    map = L.map('mapid').setView([lat, lng], zoomLevel);

    // add tiles to map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);

    // show the scale bar on the lower left corner
    L.control.scale().addTo(map);

    // add layer for markers
    markerGroup = L.layerGroup().addTo(map);
}

// create modal
function createModal(property) {
    modal = $("<div id='modal'></div>");
    modal.dialog({
        draggable: false,
        width: docWidth*0.9,
        height: docHeight*0.9,
        close: function(event, ui) {$(this).dialog('destroy').remove();}
    });
    modalWidth = modal.width();
    modalHeight = modal.height();

    $("#modal").append("<div id='modalDisplay'></div>");
    $("#modalDisplay").append("<div id='propImage'></div>");
    $("#modalDisplay").append("<div id='propDetails'></div>");
    $("#modalDisplay").append("<div id='propAnalysis'></div>");
    $("#modalDisplay").append("<div id='propChart'></div>");
    $("#propImage").outerWidth(modalWidth*0.5,true).outerHeight(modalHeight*0.5,true);
    $("#propDetails").outerWidth(modalWidth*0.5,true).outerHeight(modalHeight*0.5,true);
    $("#propAnalysis").outerWidth(modalWidth*0.5,true).outerHeight(modalHeight*0.5,true);
    $("#propChart").outerWidth(modalWidth*0.5,true).outerHeight(modalHeight*0.5,true);
    
    imgMargin = ((modalWidth*0.5)/(modalHeight*0.5)-1.33)*modalHeight*0.5;
    if (imgMargin>0) {
        $("#propImage").css("margin-left", imgMargin/2);
        $("#propImage").css("margin-right", imgMargin/2);
        $("#propImage").width((modalWidth*0.5)-(imgMargin));
    }

    // add images
    imgPosition = $("#propImage").position();
    $("#propImage").append("<button id='prevImage'>&#10094;</button>");
    $("#propImage").append("<img id='showImage'></img>");
    $("#propImage").append("<button id='nextImage'>&#10095;</button>");
    $("#propImage").append("<div id='imgTracker'></div>");
    $("#imgTracker").append("<label id='imgNum'>0 of 0</label>");

    // add details
    $("#propDetails").append("<div id='propPrice'></div>");
    $("#propDetails").append("<div id='propAddress'></div>");
    $("#propDetails").append("<div id='propBedBath'></div>");
    //$("#propDetails").append("<div id='propBath'></div>");
    $("#propDetails").append("<div id='propArea'></div>");
    $("#propDetails").append("<div id='propYear'></div>");
    $("#propDetails").append("<div id='propRemarks'></div>");

    // add analysis
    $("#propAnalysis").append("<div id='propIncome'></div>");
    $("#propAnalysis").append("<div id='propReturn'></div>");
    //$("#propAnalysis").append("<div id='propReturnMort'></div>");
    $("#propAnalysis").append("<div id='propCapRate'></div>");
    $("#propAnalysis").append("<hr id='line'></hr>")
    $("#propAnalysis").append("<div id='propRent'></div>");
    $("#propAnalysis").append("<div id='propTaxes'></div>");
    $("#propAnalysis").append("<div id='propMortgage'></div>");
    $("#propAnalysis").append("<div id='propInsurance'></div>");
    $("#propAnalysis").append("<div id='propRepair'></div>");
    $("#propAnalysis").append("<div id='propHomeowners'></div>");
    $("#propAnalysis").append("<hr id='line'></hr>")
    $("#propAnalysis").append("<div id='analysisButtons'></div>");
    $("#analysisButtons").height(docHeight/30);
    // add interest rate selector
    $("#analysisButtons").append("<div id='divInterest'><h4>Interest</h4></div>");
    $("#analysisButtons").append("<div id='interestRate'></div>");
    $("#interestRate").append("<input type='number' id='interestButton' name='interest' min='0' max='20' placeholder='4%'>");
    $("#interestRate").on("keydown", event => {
        if (event.which == 13) {
            $("#interestButton").blur();
            if($("#interestButton").val()==''){$("#interestButton").val(4);}
            getPropertyAnalysis(property.propertyId);
        }
    });
    $("#interestRate").focusout(function() {
        if($("#interestButton").val()==''){$("#interestButton").val(4);}
        getPropertyAnalysis(property.propertyId);
    });
    $("#interestButton").val(4);
    if($("#financeSlider")[0].checked == false) {
        $("#divInterest").css("opacity",0);
        $("#interestButton").css("opacity",0);
    }
    $("#analysisButtons").append("<div><h4>Term</h4></div>");
    // add mortgage term selector
    $("#analysisButtons").append("<div id='mortTerm'></div>");
    $("#mortTerm").append("<input type='number' id='termButton' name='term' min='5' max='30' placeholder='30 years'>");
    $("#mortTerm").on("keydown", event => {
        if (event.which == 13) {
            $("#termButton").blur();
            if($("#termButton").val()==""){$("#termButton").val(30);}
            getPropertyAnalysis(property.propertyId);
        }
    });
    $("#mortTerm").focusout(function() {
        getPropertyAnalysis(property.propertyId);
    });
    $("#termButton").val(30);


    // populate property details
    getPropertyDetails(property.propertyId).then(data => {
        var imgSel = 0;
        if (data.PhotosCount == 0) {
            $("#imgNum").text("0 of 0");
            $("#showImage").attr("src", "../images/NoImage.png")
        }
        else {
            $("#imgNum").text("1 of "+data.PhotosCount);
            $("#showImage").attr("src", data.Media[imgSel].MediaURL)
            $("#prevImage").click(function (e) {
                if (imgSel != 0 && data.PhotosCount != 0) {imgSel -= 1;} else {imgSel = data.PhotosCount-1;}
                $("#showImage").attr("src", data.Media[imgSel].MediaURL);
                $("#imgNum").text((imgSel+1)+" of "+data.PhotosCount);

            });
            $("#nextImage").click(function (e) {
                if (imgSel != (data.PhotosCount-1) && data.PhotosCount != 0) {imgSel += 1;} else {imgSel = 0;}
                $("#showImage").attr("src", data.Media[imgSel].MediaURL);
                $("#imgNum").text((imgSel+1)+" of "+data.PhotosCount);
            });
        }

        // set details
        $("#propPrice").text(new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:0,maximumFractionDigits:0}).format(data.ListPrice));
        $("#propAddress").text(data.UnparsedAddress);
        $("#propBedBath").text(data.BedroomsTotal+' beds    '+data.BathroomsTotalDecimal+' baths');
        $("#propArea").text(data.LivingArea+' sq ft');
        $("#propYear").text('Built in: '+data.YearBuilt);
        $("#propRemarks").text(data.PublicRemarks);
    });

    getPropertyAnalysis(property.propertyId);
}

function addMarker(property) {
    if (property.score > 7) {
        var marker = L.marker([property.latitude, property.longitude], {propertyId: property.id, score: property.score, icon: greenIcon, riseOnHover:true}).addTo(map);
        marker.bindPopup("$"+(property.price/1000)+"k", {closeButton:false});
        marker.on('mouseover', function(e) {this.setIcon(greenIconBig);
                                            this.openPopup();});
        marker.on('mouseout', function(e) {this.setIcon(greenIcon);
                                        this.closePopup();});
        marker.on('click', function(e) {createModal(this.options);});
        marker.addTo(markerGroup);
    } else if (property.score > 6) {
        var marker = L.marker([property.latitude, property.longitude], {propertyId: property.id, score: property.score, icon: orangeIcon, riseOnHover:true}).addTo(map);
        marker.bindPopup("$"+(property.price/1000)+"k", {closeButton:false});
        marker.on('mouseover', function(e) {this.setIcon(orangeIconBig);
                                            this.openPopup();});
        marker.on('mouseout', function(e) {this.setIcon(orangeIcon);
                                        this.closePopup();});
        marker.on('click', function(e) {createModal(this.options);});
        marker.addTo(markerGroup);
    } else {
        var marker = L.marker([property.latitude, property.longitude], {propertyId: property.id, score: property.score, icon: redIcon, riseOnHover:true}).addTo(map);
        marker.bindPopup("$"+(property.price/1000)+"k", {closeButton:false});
        marker.on('mouseover', function(e) {this.setIcon(redIconBig);
                                            this.openPopup();});
        marker.on('mouseout', function(e) {this.setIcon(redIcon);
                                        this.closePopup();});
        marker.on('click', function(e) {createModal(this.options);});
        marker.addTo(markerGroup);
    }
}

async function getProperties() {
    var maxPrice = $("#priceButton").val();
    var cashDown = $("#cashButton").val();
    var params = {};
    params.finance = $("#financeSlider")[0].checked;
    if (maxPrice != "") {params.maxPrice = maxPrice;}
    if (cashDown != "") {params.cashDown = cashDown;}
    var response = [];
    var url = new URL(apiURL + 'properties'), params
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        //body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        response = data;
    });
    return response;
}

function getPropertiesByZip() {

}

async function getPropertyDetails(propertyID) {
    var response = [];
    propUrl = "https://api.bridgedataoutput.com/api/v2/abor_ref/listings/"+propertyID+"?access_token=6f825db2f561cf99a0fbbf3b2f19ad8b";
    await fetch(propUrl, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        response = data.bundle;
    });
    return response;
}

async function getPropertyAnalysis(propertyID) {
    var params = {};
    params.finance = $("#financeSlider")[0].checked;
    if ($("#cashButton").val() != "") {params.cashDown = $("#cashButton").val();}
    params.interestRate = $("#interestButton").val();
    params.term = $("#termButton").val();
    var url = new URL(apiURL + 'properties/analysis/'+propertyID), params;
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
    await fetch(url, {
        method: 'GET', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json'
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        //body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        data = data[0];
        $("#propIncome").text("Income: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.income));
        $("#propRent").text("Rent: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.rent));
        $("#propTaxes").text("Taxes: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.taxes));
        $("#propMortgage").text("Mortgage Payment: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.mortgage));
        $("#propInsurance").text("Insurance Payment: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.insurance));
        $("#propRepair").text("Repair Costs: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.repair));
        $("#propHomeowners").text("Homeowners Association: "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.homeowners));
        $("#propReturn").text("ROI (Year 1): "+new Intl.NumberFormat('en-US',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.returnCash[0]+data.returnMortgage[0]));
        //$("#propReturnMort").text("ROI Finance (Year 1): "+new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.returnMortgage));
        $("#propCapRate").text("Cap Rate: "+new Intl.NumberFormat('en-US',{style:'percent',minimumFractionDigits:2,maximumFractionDigits:2}).format(data.capRate));
    
        var roiSum = data.returnCash.map(function (num, idx) {
            return (num + data.returnMortgage[idx])*100;
        });
        
        d3.selectAll("svg").remove();
        // create chart
        var chartMargin = {top: 10, right: 30, bottom: 40, left: 50};
        var chartWidth = modalWidth*0.5 - chartMargin.left - chartMargin.right;
        var chartHeight = modalHeight*0.5 - chartMargin.top - chartMargin.bottom;
        var svg = d3.select("#propChart")
            .append("svg")
                .attr("width", chartWidth+chartMargin.left+chartMargin.right)
                .attr("height", chartHeight+chartMargin.top+chartMargin.bottom)
            .append("g")
                .attr("transform", "translate("+chartMargin.left+","+chartMargin.top+")");
        // Add X axis
        xScale = d3.scaleLinear()
            .range([0, chartWidth])
            .domain([0, $("#termButton").val()]);
        svg.append("g")
            .attr("transform", "translate(0," + chartHeight + ")")
            .call(d3.axisBottom(xScale));
        // Add Y axis
        yScale = d3.scaleLinear()
            .range([chartHeight, 0])
            .domain([0, d3.max(roiSum, function(d) { return d; })]);
        svg.append("g")
            .call(d3.axisLeft(yScale));

        svg.append("path")
            .datum(roiSum)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
              .x(function(d, i) { return xScale(i);})
              .y(function(d, i) { return yScale(d); })
            );
        
        // add labels
        svg.append("text")             
            .attr("transform", "translate(" + (chartWidth/2) + " ," + 
                                (chartHeight + chartMargin.top + 20) + ")")
            .style("text-anchor", "middle")
            .text("years");

        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - chartMargin.left)
            .attr("x",0 - (chartHeight / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("ROI (%)");  
    });
}

function refreshMarkers() {
    //remove markers
    markerGroup.clearLayers();
    // get properties
    getProperties().then(properties => {
        // add markers
        //selArray = Array.from({length: 500}, d3.randomUniform(properties.length));
        $.each(properties, function (key, property) {
            if (property.status=="Active") {
                addMarker(property);
            }
        });
    });
}

$(document).ready(function() {
    // set size
    initContent();
    $(window).resize(function(){
        // get document width and height
        docWidth = $(window).width();
        docHeight = $(window).height();
        resizeContent();
    });

    // initialize map
    initMap();

    // get properties and add markers
    refreshMarkers();
});
