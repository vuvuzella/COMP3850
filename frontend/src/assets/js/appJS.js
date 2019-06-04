var pathCoordinates = [ { lat:-22.921178, lng: 151.702009 } ];

function setPath(points) {
  console.log(points);
  pathCoordinates = points;
  initMap();
}

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,
    center: { lat: -32.921178, lng: 151.702009 },
    mapTypeId: 'terrain'
  });

  var path = new google.maps.Polyline({
    path: pathCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
  });

  path.setMap(map);
  var location = pathCoordinates[0];
  map.setCenter(location);
}


