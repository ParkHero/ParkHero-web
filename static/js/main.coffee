(($) ->
  token = localStorage.getItem('token')
  latitude = 47.3824883072708
  longitude = 8.54028777940725

  load_user = ->
    $.ajax({
      url: '/users/details',
      type: 'GET',
      data: {
        token: token
      },
      contentType: 'application/json',
      success: (data) ->
        $("#navbar-login").hide()
        $("#navbar-user").show()
        $("#navbar-user").removeClass('hidden')
        $(".content").hide()
        $("#content-history").show()
      error: ->
        token = null
        localStorage.removeItem('token')
    })

  map = null

  load_carparks = ->
    $(map.markers).each((i, marker) ->
      marker.setMap(null)
    )
    center = map.getCenter()
    $.ajax({
      url: '/carparks',
      type: 'GET',
      data: {
        token: token,
        longitude: center.lng(),
        latitude: center.lat()
      }
      success: (data) ->
        $(data.carparks).each((i, carpark) ->
          map.addMarker({
            lng: carpark.longitude,
            lat: carpark.latitude,
            title: carpark.name,
            infoWindow: {
              content: '<h5>' + carpark.name + '</h5>' + carpark.free,
            }
          })
        )
      error: (r) ->
        console.log(r)
        console.log(r.responseJSON.error)
    })

  register = ->
    $.ajax({
      url: '/users/register',
      type: 'POST',
      data: JSON.stringify({
        email: $('#registration-email').val()
        password: $('#registration-password').val()
        name: $('#registration-name').val()
        creditcard: $('#registration-creditcard').val()
      }),
      contentType: 'application/json',
      success: (data) ->
        token = data.user.token
        localStorage.setItem('token', token)
        load_user()
        $('#registration').modal('hide')
      error: (data) ->
        $('#login-error-text').html(data.responseJSON.error)
        $('#login-error').modal()
    })
    false

  load_history = ->
    $.ajax({
      url: '/users/checkins',
      type: 'GET',
      data: {
        token: token
      },
      contentType: 'application/json',
      success: (data) ->
        console.log(data)
      error: ->
        token = null
        localStorage.removeItem('token')
    })

  init_map = ->
    $(".content").hide()
    $("#content-map").show()
    map = new GMaps({
      div: '#map',
      lat: latitude,
      lng: longitude,
      dragend: load_carparks
    })

    load_carparks()

  GMaps.geolocate({
    success: (position) ->
      latitude = position.coords.latitude
      longitude = position.coords.longitude
      map.setCenter(latitude, longitude);
    error: (error) ->
      $('#map-error').modal()
  })

  if token != null
    load_user()

  $("#login-form").submit ->
    $.ajax({
      url: '/users/login',
      type: 'POST',
      data: JSON.stringify({
        email: $("#login-email").val()
        password: $("#login-password").val()
      }),
      contentType: 'application/json',
      success: (data) ->
        token = data.user.token
        localStorage.setItem('token', token)
        load_user()
    })
    false

  $('#registration-form').submit(->
    register()
  )
  $('#registration-submit').click(->
    register()
  )

  $('#navbar-register').click(->
    $('#registration').modal()
  )

  $(".content").hide()
  $("#content-intro").show()

  $("#navbar-account").click ->
    $(".content").hide()
    $("#content-account").show()
    false

  $("#navbar-history").click ->
    $(".content").hide()
    $("#content-history").show()
    load_history()
    false

  $("#navbar-map").click ->
    init_map()
    false

  $('#search-form').submit ->
    init_map()
    GMaps.geocode({
      address: $('#search-address').val(),
      callback: (results, status) ->
        if status == 'OK'
          latlng = results[0].geometry.location;
          latitude = latlng.lat()
          longitude = latlng.lng()
          map.setCenter(latlng.lat(), latlng.lng());
          load_carparks()
    });
    false
) jQuery
