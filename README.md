# ParkHero-web

## Example for local_settings.py

```python
DEBUG = True
SECRET_KEY = 'SEKRET!!!!!!!'
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host/database'
```

## API

### General
 * Response code for successfull requests should always be 200
 * If response code is not 200, json response contains a field 'error' with the error message

### POST /users/register

#### Request:
```json
{
    email: 'sam@ple.email',
    password: 'samplepwd',
    name: 'Sample Name',
    creditcard: '1234',
}
```
 
#### Response:
```json
{
    user: {
        id: 124,
        token: 'uuid-aasdf',
        email: 'sam@ple.email',
        name: 'Sample Name'
    }
}
```
OR ON ERROR
```json
{
    error: 'Error message'
}
```

### POST /users/login

#### Request:
```json
{
    email: 'sam@ple.email',
    password: 'samplepwd',
}
```
 
#### Response:
```json
{
    user: {
        id: 'uuid-...',
        token: 'uuid-aasdf',
        email: 'sam@ple.email',
        name: 'Sample Name'
    }
}
```
OR ON ERROR
```json
{
    error: 'Error message'
}
```

### GET /carparks/list

#### Request:
```json
{
    token: 'uuid-...',
    longitude: 1.24567,
    latitude: 7.654321
}
```
 
#### Response:
```json
{
    carparks: [
        {
            id: 'uuid-...',
            name: 'foo',
            type: 1,
            image: 'http://test/',
            longitude: 1.234567,
            latitude: 7.654321,
            distance: 1234,
            capacity: 100,
            free: 12,
            cost: 1.23,
            todo: true
        }
    ]
}
```
OR ON ERROR
```json
{
    error: 'Error message'
}
```

### POST /carparks/{carpark_UUID}/checkin

#### Request:
```json
{
    token: 'uuid-...',
}
```
 
#### Response:
```json
{
    carpark: {
        id: 'uuid-...',
        name: 'foo',
        type: 1,
        image: 'http://test/',
        longitude: 1.234567,
        latitude: 7.654321,
        distance: 1234,
        capacity: 100,
        free: 12,
        cost: 1.23,
        todo: true
    },
    spot: {
        todo: true
    }
}
```
OR ON ERROR
```json
{
    error: 'Error message'
}
```

### POST /carparks/{carpark_UUID}/checkout

#### Request:
```json
{
    token: 'uuid-...',
}
```
 
#### Response:
```json
{
    carpark: {
        id: 'uuid-...',
        name: 'foo',
        type: 1,
        image: 'http://test/',
        longitude: 1.234567,
        latitude: 7.654321,
        distance: 1234,
        capacity: 100,
        free: 12,
        cost: 1.23,
        todo: true
    }
    duration: 65,
    cost: 123
}
```
OR ON ERROR
```json
{
    error: 'Error message'
}
```