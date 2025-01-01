# Social Media API Documentation

This API provides endpoints to manage user authentication, social interactions, and messaging in a social media application. Built using Django and Django REST Framework, it ensures scalability and ease of integration.

## Table of Contents
1. [Authentication](#authentication)
2. [User Endpoints](#user-endpoints)
3. [Post Endpoints](#post-endpoints)
4. [Follow System Endpoints](#follow-system-endpoints)
5. [Feed Endpoints](#feed-endpoints)
6. [Messaging Endpoints](#messaging-endpoints)
7. [Pagination and Sorting](#pagination-and-sorting)
8. [Deployment](#deployment)
9. [License](#license)

---

## Authentication

Endpoints to handle user login, logout, and registration.

### 1. Login
- **Description**: Authenticates a user and returns a token.
- **Endpoint**: `/api/auth/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "token": "abcdef1234567890"
  }
  ```
- **Status Codes**:
  - `200 OK`: Successful login.
  - `400 Bad Request`: Invalid credentials.

### 2. Logout
- **Description**: Logs out the authenticated user.
- **Endpoint**: `/api/auth/logout/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: `204 No Content`

### 3. Register
- **Description**: Registers a new user.
- **Endpoint**: `/api/auth/register/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com"
  }
  ```
- **Status Codes**:
  - `201 Created`: User registered successfully.
  - `400 Bad Request`: Invalid input.

---

## User Endpoints

Endpoints for managing user profiles.

### 1. Get User Profile
- **Description**: Retrieves the profile of a specified user.
- **Endpoint**: `/api/users/<username>/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "bio": "Hello, I love coding!",
    "profile_picture": null
  }
  ```
- **Status Codes**:
  - `200 OK`: User retrieved.
  - `404 Not Found`: User does not exist.

### 2. Update User Profile
- **Description**: Updates the profile of the authenticated user.
- **Endpoint**: `/api/users/<username>/`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "bio": "New bio",
    "profile_picture": "https://example.com/profile.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "bio": "New bio",
    "profile_picture": "https://example.com/profile.jpg"
  }
  ```
- **Status Codes**:
  - `200 OK`: Profile updated.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: User does not exist.

---

## Post Endpoints

Endpoints for creating, retrieving, updating, and deleting posts.

### 1. Create a Post
- **Description**: Creates a new post for the authenticated user.
- **Endpoint**: `/api/posts/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "This is my first post!",
    "media": "https://example.com/image.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "content": "This is my first post!",
    "media": "https://example.com/image.jpg",
    "timestamp": "2024-12-27T12:00:00Z",
    "user": "testuser"
  }
  ```
- **Status Codes**:
  - `201 Created`: Post created.
  - `400 Bad Request`: Invalid input.

### 2. Get a Post
- **Description**: Retrieves the details of a specific post.
- **Endpoint**: `/api/posts/<id>/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": 1,
    "content": "This is my first post!",
    "media": "https://example.com/image.jpg",
    "timestamp": "2024-12-27T12:00:00Z",
    "user": "testuser"
  }
  ```
- **Status Codes**:
  - `200 OK`: Post retrieved.
  - `404 Not Found`: Post does not exist.

### 3. Update a Post
- **Description**: Updates an existing post created by the authenticated user.
- **Endpoint**: `/api/posts/<id>/`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "Updated content!",
    "media": "https://example.com/new-image.jpg"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "content": "Updated content!",
    "media": "https://example.com/new-image.jpg",
    "timestamp": "2024-12-27T12:00:00Z",
    "user": "testuser"
  }
  ```
- **Status Codes**:
  - `200 OK`: Post updated.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 4. Delete a Post
- **Description**: Deletes a specific post created by the authenticated user.
- **Endpoint**: `/api/posts/<id>/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`
- **Status Codes**:
  - `204 No Content`: Post deleted.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

---

## Follow System Endpoints

Endpoints for managing follow relationships between users.

### 1. Follow a User
- **Description**: Follows a specific user.
- **Endpoint**: `/api/users/<username>/follow/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "You are now following testuser."
  }
  ```
- **Status Codes**:
  - `200 OK`: Followed user.
  - `400 Bad Request`: Invalid request.

### 2. Unfollow a User
- **Description**: Unfollows a specific user.
- **Endpoint**: `/api/users/<username>/unfollow/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "You have unfollowed testuser."
  }
  ```
- **Status Codes**:
  - `200 OK`: Unfollowed user.

---

## Feed Endpoints

Endpoints for retrieving posts from followed users.

### 1. View Feed
- **Description**: Retrieves the feed of posts from users the authenticated user follows.
- **Endpoint**: `/api/posts/feed/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  [
    {
      "id": 1,
      "content": "This is my first post!",
      "media": "https://example.com/image.jpg",
      "timestamp": "2024-12-27T12:00:00Z",
      "user": "testuser"
    }
  ]
  ```
- **Status Codes**:
  - `200 OK`: Feed retrieved.

---

## Messaging Endpoints

Endpoints for sending and managing direct messages.

### 1. Send a Message
- **Description**: Sends a direct message to a specified user.
- **Endpoint**: `/api/posts/messages/send/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "recipient": "testuser",
    "content": "Hello!"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "sender": "currentuser",
    "recipient": "testuser",
    "content": "Hello!",
    "timestamp": "2024-12-27T12:00:00Z"
  }
  ```
- **Status Codes**:
  - `201 Created`: Message sent.

---

## Pagination and Sorting

Details on how list endpoints can be paginated and sorted.

- **Description**: Provides controls for data pagination and sorting.
- **Query Parameters**:
  - `?page=<page_number>`: Specify the page number.
  - `?sort=<field>`: Sort by a specific field (e.g., `timestamp`).

---

## Deployment

- **Description**: Deployment details for the API.
- The API is deployed on Heroku and can be accessed at: [https://socialmedia-api.herokuapp.com](https://socialmedia-api.herokuapp.com)

---

## License

- **Description**: Licensing details.
- This project is licensed under the MIT License.

