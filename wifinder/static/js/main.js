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
    green: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
    myRed: 'http://maps.google.com/mapfiles/ms/icons/small_red.png'
};

var icon_nak = {
    gray:   'img/pin_gray.png',
    yellow: 'img/pin_yellow.png',
    purple: 'img/pin_pink.png',
    blue:   'img/pin_turquoise_blue.png',
    green:  'img/pin_light_green.png',
    white:  'img/pin_white.png'
};

var status_mapping = {
    'Nominal': icon_nak.gray,                   //gray
    'S.A Done': icon_nak.yellow,                //yellow
    'A.P.Installation.Done': icon_nak.purple,   //purple
    'B.H.Installation.Done': icon_nak.blue,     //blue
    'On - Air': icon_nak.green,                 //green
    'Switched Off': icon_nak.white,             //white
    'undefined': icons.red
}

var status_color = {
    'Nominal': "#d7dbdd",                       //gray
    'S.A Done': "#fdfec7",                      //yellow
    'A.P.Installation.Done': "#e8daef",         //purple
    'B.H.Installation.Done': "#d1f2eb",         //blue
    'On - Air': "#2ecc71",                      //green
    'Switched Off': "#fdfefe"                   //white
}

;
// var tileUrl = "http://172.26.80.111/osm/{z}/{x}/{y}.png";
var tileUrl = "http://5.160.202.6:2020/osm/{z}/{x}/{y}.png";
var allMarkers = [];
function setMarkers(map) {
    var zoom = map.getZoom();
    var zoom_draw = {
        0: 'country',
        1: 'country',
        2: 'country',
        3: 'country',
        4: 'country',
        5: 'country',
        6: 'country',
        7: 'province',
        8: 'province',
        9: 'province',
        10: 'province',
        11: 'province',
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
                icon: status_mapping[data.status] || icons.red,
            });
            document.markers[zoom_draw[zoom]][index]._marker = marker

        }

        var contents = '<div id="iw-container">' +
                       '<div class="iw-title">NAK Wifinder</div>' +
                       '<div class="iw-content">' +
                       '<p><h5>'+ data.name +'</h5></p>' +
                       '</div>' +
                       '<div class="iw-bottom-gradient"></div>' +
                       '</div>';

        // data._infoWindow = new google.maps.InfoWindow({content: data.name});
        data._infoWindow = new google.maps.InfoWindow({content: contents});
        marker.addListener('click', function () {
            if (openInfo) openInfo.close();

            data._infoWindow.open(map, marker);
            openInfo = data._infoWindow;
            divMapInfo.innerHTML = data.info;

	        // classie.toggle( menuRight, 'cbp-spmenu-open' );
            if( button !== 'showRight' ) {
				classie.toggle( showRight, 'disabled' );
			}
        });

        // Event that closes the Info Window with a click on the map
      google.maps.event.addListener(map, 'click', function() {
        data._infoWindow.close();
      });

       // for prepare style
       google.maps.event.addListener(data._infoWindow, 'domready', function() {

       // ============================================================
       // Reference to the DIV which receives the contents of the infowindow using jQuery
       var iwOuter = $('.gm-style-iw');
       var iwBackground = iwOuter.prev();

       // Remove the background shadow DIV
       iwBackground.children(':nth-child(2)').css({'display' : 'none'});

       // Remove the white background DIV
       iwBackground.children(':nth-child(4)').css({'display' : 'none'});


       // ============================================================
       var iwCloseBtn = iwOuter.next();

        // Apply the desired effect to the close button
        iwCloseBtn.css({
              opacity: '0.6', // by default the close button has an opacity of 0.7
              right: '58px', top: '21px', // button repositioning
              'border-radius': '2px', // circular effect
              'box-shadow': '0 0 5px #c39bd3' // 3D effect to highlight the button
          });

        iwCloseBtn.mouseout(function(){
          $(this).css({opacity: '1'});
        });

        iwCloseBtn.mouseover(function(){
          $(this).css({opacity: '0.6'});
        });
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
            // if (!mapBounds.intersects(tileBounds) || zoom < mapMinZoom || zoom > mapMaxZoom) return null;
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

    $.get('/pois/data.json', function (response, error) {
        document.markers = response;
        setMarkers(map, mapMinZoom);
    });
    setMarkers(map, mapMinZoom);
    map.addListener('zoom_changed', function () {
        setMarkers(map);
    });
}

