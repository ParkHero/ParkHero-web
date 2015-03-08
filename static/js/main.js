// Generated by CoffeeScript 1.8.0
(function() {
  (function($) {
    var load_carparks, load_user, map, register, token;
    load_user = function(token) {
      return $.ajax({
        url: '/users/details',
        type: 'GET',
        data: {
          token: token
        },
        ontentType: 'application/json',
        success: function(data) {
          $("#navbar-login").hide();
          $("#navbar-user").show();
          $("#navbar-user").removeClass('hidden');
          $(".content").hide();
          return $("#content-history").show();
        }
      });
    };
    map = null;
    load_carparks = function() {
      var center;
      $(map.markers).each(function(i, marker) {
        return marker.setMap(null);
      });
      center = map.getCenter();
      return $.ajax({
        url: '/carparks',
        type: 'GET',
        data: {
          token: token,
          longitude: center.lng(),
          latitude: center.lat()
        },
        success: function(data) {
          return $(data.carparks).each(function(i, carpark) {
            return map.addMarker({
              lng: carpark.longitude,
              lat: carpark.latitude,
              title: carpark.name,
              infoWindow: {
                content: '<h5>' + carpark.name + '</h5>' + carpark.free
              }
            });
          });
        },
        error: function(r) {
          console.log(r);
          return console.log(r.responseJSON.error);
        }
      });
    };
    register = function() {
      $.ajax({
        url: '/users/register',
        type: 'POST',
        data: JSON.stringify({
          email: $('#registration-email').val(),
          password: $('#registration-password').val(),
          name: $('#registration-name').val(),
          creditcard: $('#registration-creditcard').val()
        }),
        contentType: 'application/json',
        success: function(data) {
          localStorage.setItem('token', data.user.token);
          return load_user(data.user.token);
        },
        error: function(data) {
          $('#login-error-text').html(data.responseJSON.error);
          return $('#login-error').modal();
        }
      });
      return false;
    };
    token = localStorage.getItem('token');
    if (token !== null) {
      load_user(token);
    }
    $("#login-form").submit(function() {
      $.ajax({
        url: '/users/login',
        type: 'POST',
        data: JSON.stringify({
          email: $("#login-email").val(),
          password: $("#login-password").val()
        }),
        contentType: 'application/json',
        success: function(data) {
          localStorage.setItem('token', data.user.token);
          load_user(data.user.token);
          return $('#registration').modal('hide');
        }
      });
      return false;
    });
    $('#registration-form').submit(function() {
      return register();
    });
    $('#registration-submit').click(function() {
      return register();
    });
    $('#navbar-register').click(function() {
      return $('#registration').modal();
    });
    $(".content").hide();
    $("#content-intro").show();
    $("#navbar-account").click(function() {
      $(".content").hide();
      $("#content-account").show();
      return false;
    });
    $("#navbar-history").click(function() {
      $(".content").hide();
      $("#content-history").show();
      return false;
    });
    return $("#navbar-map").click(function() {
      $(".content").hide();
      $("#content-map").show();
      map = new GMaps({
        div: '#map',
        lat: 47.3824883072708,
        lng: 8.54028777940725,
        dragend: load_carparks
      });
      GMaps.geolocate({
        success: function(position) {
          return map.setCenter(position.coords.latitude, position.coords.longitude);
        },
        error: function(error) {
          return $('#map-error').modal();
        }
      });
      load_carparks();
      return false;
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=main.js.map