let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

initMap();

$.ajax({
    url: "./PetWeightVar.json",
    type: "GET",
    dataType: "json",
    success: function(data) {
      alert("SUCCESS!!!");
      $.each(data, function (id, element) {
        alert(element.id);                      
    });
    },
    
    error: function() {
      alert("ERROR!!!");
    }
  });