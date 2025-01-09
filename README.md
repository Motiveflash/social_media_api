# Social Media API Documentation

This API provides endpoints to manage user authentication, social interactions, and messaging in a social media application. Built using Django and Django REST Framework, it ensures scalability and ease of integration.

---


## Deployment

- **Description**: Deployment details for the API.
- The API is deployed on Heroku and can be accessed at: [https://tap-chat-api-1cb8bb4f5701.herokuapp.com/](https://tap-chat-api-1cb8bb4f5701.herokuapp.com/)

---

## Authentication

Endpoints to handle user login, logout, and registration.

### 1. Register
- **Description**: Registers a new user.
- **Endpoint**: `/api/users/register/`
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
    "message": "User registered successfully"
  }
  ```
- **Status Codes**:
  - `201 Created`: User registered successfully.
  - `400 Bad Request`: Invalid input.


### 2. Login
- **Description**:Login with either username or email to Authenticates the user and returns the access token.
- **Endpoint**: `/api/users/login/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "refresh": "abcdef1234567890",
    "access": "abcdef1234567890"
  }
  ```
- **Status Codes**:
  - `200 OK`: Successful login.
  - `400 Bad Request`: Invalid credentials.

### 3. Logout
- **Description**: Logs out the authenticated user.
- **Endpoint**: `/api/users/logout/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: `204 No Content`

---

## User Endpoints

Endpoints for managing user profiles.

### 1. Get User Profile
- **Description**: Retrieves the profile of a current user.
- **Endpoint**: `/api/users/profile/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "bio": "Hello, I love coding!",
    "profile_picture": null,
    "follower_count": 0,
    "following_count": 0,
    "followers": [],
    "following": []
  }
  ```
- **Status Codes**:
  - `200 OK`: User retrieved.
  - `404 Not Found`: User does not exist.

### 2. Update User Profile
- **Description**: Updates the profile of the authenticated user.
- **Endpoint**: `/api/users/profile/`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "username": "new_username",
    "bio": "Updated bio text"
  }
  ```
- **Response**:
  ```json
  {
    "username": "new_username",
    "email": "test@example.com",
    "bio": "Updated bio text",
    "profile_picture": null,
    "follower_count": 0,
    "following_count": 0,
    "followers": [],
    "following": []
  }
  ```
- **Status Codes**:
  - `200 OK`: Profile updated.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: User does not exist.

---

## Post Endpoints

Endpoints for creating, retrieving, updating, and deleting posts.
Like and comment on a post

### 1. Lists of Posts
- **Description**: Creates a new post for the authenticated user.
- **Endpoint**: `/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  [
    {
      "id": 1,
      "author": "new_username",
      "content": "This is my first post!",
      "media": "null",
      "like_count": 0,
      "comment_counts": 0,
      "timestamp": "2024-12-27T12:00:00Z",
    }
  ]
  ```
- **Status Codes**:
  - `201 Created`: Post created.
  - `400 Bad Request`: Invalid input.


### 2. Create a Post
- **Description**: Creates a new post for the authenticated user.
- **Endpoint**: `api/posts/create/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "This is my first post!",
    "media": "Optional media link"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "author": "new_username",
    "content": "This is my first post!",
    "media": "null",
    "like_count": 0,
    "comment_counts": 0,
    "timestamp": "2024-12-27T12:00:00Z",
  }
  ```
- **Status Codes**:
  - `201 Created`: Post created.
  - `400 Bad Request`: Invalid input.

### 3. Get a Post
- **Description**: Retrieves the details of a specific post.
- **Endpoint**: `/api/posts/<int:pk>/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "id": 1,
    "author": "new_username",
    "content": "This is my first post",
    "media": null,
    "like_count": 1,
    "comment_counts": 0,
    "timestamp": "2025-01-03T12:05:49.461887Z"
  }
  ```
- **Status Codes**:
  - `200 OK`: Post retrieved.
  - `404 Not Found`: Post does not exist.

### 4. Update a Post
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
    "author": "motive",
    "content": "updated content",
    "media": "https://example.com/new-image.jpg",
    "like_count": 1,
    "comment_counts": 0,
    "timestamp": "2025-01-03T12:05:49.461887Z"
  }
  ```
- **Status Codes**:
  - `200 OK`: Post updated.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 5. Delete a Post
- **Description**: Deletes a specific post created by the authenticated user.
- **Endpoint**: `/api/posts/<id>/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**: `204 No Content`
- **Status Codes**:
  - `204 No Content`: Post deleted.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 6. Like a Post
- **Description**: like a specific post.
- **Endpoint**: `/api/posts/like/<int:post_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "user": "current user",
    "post": "post_id",
    "timestamp": "2025-01-04T14:17:02.310651Z"
  }
  ```
- **Status Codes**:
  - `201 Created`: Post liked.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 7. Unlike a Post
- **Description**: Unlike a specific post.
- **Endpoint**: `/api/posts/unlike/<int:post_id>/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "detail": "You have unliked this post."
  }
  ```
- **Status Codes**:
  - `200 OK`: Post liked.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 8. Create Comment
- **Description**: Comment on a specific post.
- **Endpoint**: `/api/posts/<int:post_id>/comment/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "This is a comment"
  }
  ```
- **Response**:
  ```json
  {
    "user": "current user",
    "post": "post_id",
    "content": "This is a comment",
    "timestamp": "2025-01-04T14:51:38.038789Z"
  }
  ```
- **Status Codes**:
  - `201 Created`: Comment Post.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post does not exist.

### 9. Edit Comment
- **Description**: Edit a Comment.
- **Endpoint**: `/api/posts/<int:post_id>/comments/<int:comment_id>/`
- **Method**: `PUT`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "content": "Edit the comment"
  }
  ```
- **Response**:
  ```json
  {
    "user": "current user",
    "post": "post_id",
    "content": "This is the edited comment",
    "timestamp": "2025-01-04T14:51:38.038789Z"
  }
  ```
- **Status Codes**:
  - `200 OK`: Edit Comment Post.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post or comment does not exist.

### 10. Delete Comment
- **Description**: Delete a Comment.
- **Endpoint**: `/api/posts/<int:post_id>/comments/<int:comment_id>/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Status Codes**:
  - `204 No Content`: Edit Comment Post.
  - `403 Forbidden`: Unauthorized access.
  - `404 Not Found`: Post or comment does not exist.

### 11. View Post Comments
- **Description**: Comment on a specific post.
- **Endpoint**: `/api/posts/<int:post_id>/comments/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  [
    {
      "user": "commenter",
      "post": "post_id",
      "content": "This is a comment",
      "timestamp": "2025-01-04T14:51:38.038789Z"
    }
  ]
  ```
- **Status Codes**:
  - `200 OK`: Comment list.
  - `404 Not Found`: Post does not exist.

---

## Follow System Endpoints

Endpoints for managing follow relationships between users.

### 1. Follow a User
- **Description**: Follows a specific user.
- **Endpoint**: `/api/users/follow/<str:username>/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "You are now following testuser."
  }
  ```
- **Status Codes**:
  - `201 Created`: Followed user.
  - `400 Bad Request`: Invalid request.

### 2. Unfollow a User
- **Description**: Unfollows a specific user.
- **Endpoint**: `/api/users/unfollow/<str:username>/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "You have unfollowed testuser."
  }
  ```
- **Status Codes**:
  - `200 OK`: Unfollowed user.

### 3. Number of followers 
- **Description**: Get the follow-count of a specific user.
- **Endpoint**: `api/users/<str:username>/followers-count/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  {
    "username": "random user",
    "followers_count": 1
  }
  ```
- **Status Codes**:
  - `200 OK`: Number of followers.
  - `404 Not Found`: User dose not exist

### 4. Number of following 
- **Description**: Get the following-count of a specific user.
- **Endpoint**: `api/users/<str:username>/followers-count/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  {
    "username": "random user",
    "following_count": 4
  }
  ```
- **Status Codes**:
  - `200 OK`: Number of following.
  - `404 Not Found`: User dose not exist

### 5. Followers list 
- **Description**: Get the followers list of a specific user.
- **Endpoint**: `api/users/<str:username>/followers-list/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  {
    "username": "random user",
    "following": []
  }
  ```
- **Status Codes**:
  - `200 OK`: List of followers.
  - `404 Not Found`: User dose not exist
---

### 5. Following list
- **Description**: Get the following list of a specific user.
- **Endpoint**: `api/users/<str:username>/following-list/`
- **Method**: `GET`
- **Authentication**: Not Required
- **Response**:
  ```json
  {
    "username": "random user",
    "following": ["user1", "user2", "user3", "user4"]
  }
  ```
- **Status Codes**:
  - `200 OK`: List of following.
  - `404 Not Found`: User dose not exist
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
      "author": "followed user",
      "content": "This is my first post",
      "media": null,
      "like_count": 1,
      "comment_counts": 0,
      "timestamp": "2025-01-03T12:05:49.461887Z"
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
    "recipient": "testuser",
    "content": "Hello!",
    "is_read": "false",
    "timestamp": "2024-12-27T12:00:00Z"
  }
  ```
- **Status Codes**:
  - `201 Created`: Message sent.

### 2. Inbox
- **Description**: Get all recieved messages of the authenticated user.
- **Endpoint**: `/api/posts/messages/inbox/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  [
    {
      "id": 1,
      "sender": "testuser",
      "is_read": "false",
      "timestamp": "2024-12-27T12:00:00Z"
    }
  ]

### 3. Messages Detail 
- **Description**: View the detail of a message
- **Endpoint**: `/api/posts/messages/<int:message_id>/detail/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": 1,
    "sender": "testuser",
    "content": "Hello!",
    "is_read": "true",
    "timestamp": "2024-12-27T12:00:00Z"
  }
  ```
- **Status Codes**:
  - `200 OK`: Inbox.

### 3. Sent Messages 
- **Description**: Get all sent messages of the authenticated user.
- **Endpoint**: `/api/posts/messages/sent/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  [
    {
      "id": 1,
      "recipient": "testuser",
      "content": "Hello!",
      "is_read": "false",
      "timestamp": "2024-12-27T12:00:00Z"
    }
  ]
  ```
- **Status Codes**:
  - `200 OK`: Inbox.

### 3. Delete a Messages 
- **Description**: Get all sent messages of the authenticated user.
- **Endpoint**: `/api/posts/messages/sent/`
- **Method**: `DELETE`
- **Authentication**: Required
- **Status Codes**:
  - `204 No Content`: Deleted Message.

---

## Notifications Endpoints

Endpoints for notifications.

### 1. Get All Notification
- **Description**: Get all notifications of the authenticated user.
- **Endpoint**: `/api/posts/notifications/`
- **Method**: `GIT`
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
  [
    {
      "id": 1,
      "sender": "testuser",
      "post": "nul",
      "notification_type": "direct_message",
      "message": "You have a new message from testuser: Hey this is a message!",
      "is_read": false,
      "timestamp": "2025-01-05T16:45:22.712261Z"
    }
  ]
  ```
- **Status Codes**:
  - `200 OK`: Notifications.

---

### Optional Query Parameters for GET /api/posts/

The `GET /api/posts/` endpoint supports the following optional query parameters for filtering, searching, and ordering posts:

---

#### 1. `author` (optional)
Filters posts by the author's username.

- **Example:** `author=alice`
  - Returns posts authored by the user with the username `alice`.

---

#### 2. `title` (optional)
Filters posts where the title contains the specified string (case-insensitive).

- **Example:** `title=python`
  - Returns posts where the title contains the word `python`.

---

#### 3. `category` (optional)
Filters posts by category (partial match).

- **Example:** `category=tech`
  - Returns posts in the `tech` category or any post that contains `tech` in the category name.

---

#### 4. `published_after` (optional)
Filters posts published within the last `N` days. This parameter must be an integer representing the number of days ago.

- **Example:** `published_after=7`
  - Returns posts that were published in the last 7 days.

---

#### 5. `published_before` (optional)
Filters posts published before `N` days ago. This parameter must be an integer representing the number of days ago.

- **Example:** `published_before=30`
  - Returns posts that were published more than 30 days ago.

---

#### 6. `search` (optional)
Performs a full-text search on both the title and content fields for a specified string (case-insensitive).

- **Example:** `search=python`
  - Returns posts where either the title or content contains the word `python`.

---

#### 7. `ordering` (optional)
Defines the field(s) by which the posts should be ordered. Prefix the field name with `-` to indicate descending order.

- **Example:** `ordering=-timestamp`
  - Orders posts by the `timestamp` field in descending order.
- **Additional Example:** `ordering=-author__username`
  - Orders posts by the author's username in descending order.

---


---

## License

- **Description**: Licensing details.
- This project is licensed under the MIT License.

