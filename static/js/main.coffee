(($) ->
  token = localStorage.getItem('token')
  latitude = 47.3824883072708
  longitude = 8.54028777940725
  map = null

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

        # Populate account page
        $('#account-name').val(data.user.name)
        $('#account-email').val(data.user.email)
        load_history()
      error: ->
        token = null
        localStorage.removeItem('token')
    })

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
              content: "<h5>#{ carpark.name }</h5><img src=\"#{ carpark.image }\"><br>Parking spots: #{ carpark.free }/#{ carpark.capacity}<br>Cost: CHF #{ carpark.cost / 100 } / h<br>#{ carpark.address }",
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
        table = $("#history-table")
        tbody = table.find('tbody')
        # Clear content
        tbody.html('')
        $(data.checkins).each((i, checkin) ->
          tbody.append($("<tr><td><img src=\"#{ checkin.carpark.image }\"></td><td>#{ checkin.carpark.name }</td><td>#{ checkin.checkin }</td><td>#{ checkin.checkout }</td><td>#{ checkin.duration } min</td><td>#{ checkin.cost / 100 } CHF</td></tr>"))
        )
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

  if map?
    GMaps.geolocate({
      success: (position) ->
        latitude = position.coords.latitude
        longitude = position.coords.longitude
        map.setCenter(latitude, longitude);
      error: (error) ->
        $('#map-error').modal()
    })

  if token?
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
    $('#registration-form').submit()
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

  $('#account-form').submit(->
    data = {
      token: token
      email: $('#account-email').val()
      name: $('#account-name').val()
    }
    if $('#account-password').val()?
      data.password = $('#account-password').val()
    if $('#account-creditcard').val()?
      data.creditcard = $('#account-creditcard').val()
    $.ajax({
      url: '/users/update',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: (data) ->
        load_user()
    })
    false
  )
) jQuery
