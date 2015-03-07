(($) ->
  load_user = (token) ->
    $.ajax({
      url: '/users/details',
      type: 'GET',
      data: {
        token: token
      },
      ontentType: 'application/json',
      success: (data) ->
        $("#navbar-login").hide()
        $("#navbar-user").show()
        $("#navbar-user").removeClass('hidden')
        $(".content").hide()
        $("#content-history").show()
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
        localStorage.setItem('token', data.user.token)
        load_user(data.user.token)
      error: (data) ->
        $('#login-error-text').html(data.responseJSON.error)
        $('#login-error').modal()
    })
    false

  token = localStorage.getItem('token')
  if token != null
    load_user(token)

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
        localStorage.setItem('token', data.user.token)
        load_user(data.user.token)
        $('#registration').modal('hide')
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
    false

  $("#navbar-map").click ->
    $(".content").hide()
    $("#content-map").show()
    map = new GMaps({
      div: '#map',
      lat: 47.3824883072708,
      lng: 8.54028777940725,
      dragend: load_carparks
    })

    GMaps.geolocate({
      success: (position) ->
        map.setCenter(position.coords.latitude, position.coords.longitude);
      error: (error) ->
        $('#map-error').modal()
    })
    load_carparks()
    false
) jQuery
