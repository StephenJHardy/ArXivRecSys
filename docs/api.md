# API Documentation

## Authentication

### Register User
```
POST /api/users/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword"
}
```

### Login
```
POST /api/users/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
}
```

## Papers

### Get Daily Papers
```
GET /api/papers?skip=0&limit=100
Authorization: Bearer <token>
```

Response:
```json
[
    {
        "id": 1,
        "arxiv_id": "2401.12345",
        "title": "Example Paper Title",
        "abstract": "This is the paper abstract...",
        "authors": "Author One, Author Two",
        "categories": "cs.AI cs.LG",
        "published_date": "2024-01-15T10:30:00",
        "score": 4.5
    }
]
```

### Get Paper by ID
```
GET /api/papers/{paper_id}
Authorization: Bearer <token>
```

### Rate Paper
```
POST /api/papers/{paper_id}/rate
Authorization: Bearer <token>
Content-Type: application/json

{
    "rating": 5
}
```

## User Operations

### Get Current User
```
GET /api/users/me
Authorization: Bearer <token>
```

### Get User Ratings
```
GET /api/users/me/ratings
Authorization: Bearer <token>
```

Response:
```json
[
    {
        "id": 1,
        "paper_id": 123,
        "rating": 5,
        "created_at": "2024-01-15T10:30:00"
    }
]
```

## Error Responses

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
    "detail": "Paper not found"
}
```

### 400 Bad Request
```json
{
    "detail": "Email already registered"
}
```

## Rate Limiting

- API requests are limited to 100 requests per minute per user
- Authentication attempts are limited to 5 per minute per IP

## Data Formats

### Paper Object
```json
{
    "id": "integer",
    "arxiv_id": "string",
    "title": "string",
    "abstract": "string",
    "authors": "string",
    "categories": "string",
    "published_date": "datetime",
    "score": "float"
}
```

### Rating Object
```json
{
    "id": "integer",
    "paper_id": "integer",
    "rating": "integer (0-5)",
    "created_at": "datetime"
}
```

### User Object
```json
{
    "id": "integer",
    "email": "string",
    "created_at": "datetime"
}
``` 