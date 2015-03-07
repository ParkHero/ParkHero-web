# ParkHero-web

## API

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
    success: true,
    user: {
        id: 124,
        token: 'uuid-aasdf',
        email: 'sam@ple.email',
        name: 'Sample Name'
    }
}
```
OR
```json
{
    success: false,
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
    success: true,
    user: {
        id: 'uuid-...',
        token: 'uuid-aasdf',
        email: 'sam@ple.email',
        name: 'Sample Name'
    }
}
```
OR
```json
{
    success: false,
    error: 'Error message'
}
```

### GET /carparks/list

#### Request:
```json
{
    longitude: 1.24567,
    latitude: 7.654321
}
```
 
#### Response:
```json
{
    success: true,
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

### POST /carparks/{carpark_UUID}/checkin

#### Request:
```json
{
    user_id: 'uuid-...',
    token: 'uuid-...',
}
```
 
#### Response:
```json
{
    success: true,
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

### POST /carparks/{carpark_UUID}/checkout

#### Request:
```json
{
    user_id: 'uuid-...',
    token: 'uuid-...',
}
```
 
#### Response:
```json
{
    success: true,
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