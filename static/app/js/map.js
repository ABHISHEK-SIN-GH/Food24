var myLatLng = { lat: 0.0, lng: 0.0 };
var mapOptions = {
  center: myLatLng,
  zoom: 1,
  mapTypeId: google.maps.MapTypeId.ROADMAP,
};

// Hide result box
document.getElementById("output").style.display = "none";

// Create/Init map
var map = new google.maps.Map(
  document.getElementById("google-map"),
  mapOptions
);

// Create a DirectionsService object to use the route method and get a result for our request
var directionsService = new google.maps.DirectionsService();


// Define calcRoute function
function calcRoute() {
  console.log("Map is live")

  //create request
  var request = {
    origin: document.getElementById("location-1").value,
    destination: document.getElementById("location-2").value,
    travelMode: google.maps.TravelMode.DRIVING,
    unitSystem: google.maps.UnitSystem.METRIC,
  };
 
  // Routing
  directionsService.route(request, function (result, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      //Get distance and time
      var dis = result.routes[0].legs[0].distance.text 
      // console.log(dis);
      document.getElementById("output").style.display = "block";
      document.getElementById("output").value = result.routes[0].legs[0].distance.text;
      //display route
      // directionsDisplay.setDirections(result);
      const output = result.routes[0].legs[0].distance.text;
      var id = $('#diff').attr("pid").toString();
      console.log(id);
      dis = output;
      var dist = dis.replace(',', '');
      var justTheNumber = parseInt(dist.match(/\d+/g));
      console.log(justTheNumber);
      $.ajax({ type:"GET", url:"/shipping", data:{prod_id:id,distance:justTheNumber}, 
      success:function(data){
         console.log(data);
         document.getElementById("shippp").innerText = data.shipping + ".0"
         document.getElementById("total").innerText = data.totalAmt
      }
      })
      return; 
    } 
    else {
      //delete route from map
      directionsDisplay.setDirections({ routes: [] });
      //center map in London
      map.setCenter(myLatLng);
      //Show error message
      alert("Can't find road! Please try again!");
      clearRoute();
      console.log("hello")
    }
  });
}


// Create autocomplete objects for all inputs

var options = {
  types: ["(cities)"],
};

var input1 = document.getElementById("location-1");
var autocomplete1 = new google.maps.places.Autocomplete(input1, options);

var input2 = document.getElementById("location-2");
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);


