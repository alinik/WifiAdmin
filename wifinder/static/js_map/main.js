"use strict";
var openInfo;
var lastZoom;
//    var tileUrl="http://localhost:8080/mapbox-studio-osm-bright/{z}/{x}/{y}.png";
// var tileUrl = "/osm/{z}/{x}/{y}.png";
var icons = {
    red: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
    blue: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
    purple: 'http://maps.google.com/mapfiles/ms/icons/purple-dot.png',
    yellow: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png',
    green: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
};
var status_mapping = {
    University: icons.green,
    Hospital:icons.yellow
};
var tileUrl = "http://172.26.80.111/osm/{z}/{x}/{y}.png";
var allMarkers = [];
function setMarkers(map) {
    var zoom = map.getZoom();
    var zoom_draw = {
        0: 'country',
        1: 'country',
        2: 'country',
        3: 'country',
        4: 'country',
        5: 'province',
        6: 'province',
        7: 'province',
        8: 'province',
        9: 'province',
        10: 'detail',
        11: 'detail',
        12: 'detail',
        13: 'detail',
        14: 'detail',
        15: 'detail',
        16: 'detail',
        17: 'detail',
        18: 'detail',
        19: 'detail',
        20: 'detail'
    };
    allMarkers.forEach(function (marker) {
        marker.setMap(null);

    });
    allMarkers = [];
    document.markers[zoom_draw[zoom]].forEach(function (data, index) {
        var marker = data._marker;
        if (!marker) {
            console.log('marker created' + data.name);

            marker = new google.maps.Marker({
                position: {lat: data.coord[0], lng: data.coord[1]},
                title: data.name,
                icon: status_mapping[data.status] || icons.red
            });
            document.markers[zoom_draw[zoom]][index]._marker = marker
        }
        data._infoWindow = new google.maps.InfoWindow({content: data.name});
        marker.addListener('click', function () {
            if (openInfo) openInfo.close();
            data._infoWindow.open(map, marker);
            openInfo = data._infoWindow;
            divMapInfo.innerHTML = data.info;
        });
        marker.setMap(map);
        allMarkers.push(marker);
        // console.log('marker set' + data.name);

    });
    lastZoom = zoom;
}

//noinspection JSUnusedGlobalSymbols
function initialize() {

    var mapBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(25.064079, 44.047249),
        new google.maps.LatLng(39.777222, 63.317459));
    var mapMinZoom = 5;
    var mapMaxZoom = 22;
    var opts = {
        streetViewControl: false,
        // scrollwheel: false,
        tilt: 0,
        mapTypeId: 'tiles',
        mapTypeControl: false,
        zoom: 10,
        center: new google.maps.LatLng(35.7211, 51.3995)
    };
    var imageMapType = new google.maps.ImageMapType({
        getTileUrl: function (coord, zoom) {
            var proj = map.getProjection();
            var z2 = Math.pow(2, zoom);
            var tileXSize = 256 / z2;
            var tileYSize = 256 / z2;
            var tileBounds = new google.maps.LatLngBounds(
                proj.fromPointToLatLng(new google.maps.Point(coord.x * tileXSize, (coord.y + 1) * tileYSize)),
                proj.fromPointToLatLng(new google.maps.Point((coord.x + 1) * tileXSize, coord.y * tileYSize))
            );
            if (!mapBounds.intersects(tileBounds) || zoom < mapMinZoom || zoom > mapMaxZoom) return null;
            return tileUrl.replace('{z}', zoom).replace('{x}', coord.x).replace('{y}', coord.y);
        },
        tileSize: new google.maps.Size(256, 256),
        minZoom: mapMinZoom,
        maxZoom: mapMaxZoom,
        name: 'Tiles'
    });

// // Google only
//        var mapProp = {
//            center: new google.maps.LatLng(35.7211, 51.3995),
//            zoom: 9,
//            mapTypeId: google.maps.MapTypeId.ROADMAP
//        };
//        var map = new google.maps.Map(document.getElementById("map"), mapProp);
// // End Google only
// OSM Map
    var map = new google.maps.Map(document.getElementById("map"), opts);
    map.mapTypes.set('tiles', imageMapType);
// End OSM Map
    map.fitBounds(mapBounds);
    setMarkers(map, mapMinZoom);
    map.addListener('zoom_changed', function () {
        setMarkers(map);
    });
}

