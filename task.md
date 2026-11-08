# Technical Specification: Blog API

## 1. Project Overview

A REST API for a blog platform with user authentication, blog posts, and comments. The project follows the same architecture and technology stack as the reference e-commerce project (Products & Reviews), but with a different domain.

---

## 2. Tech Stack

| Component        | Technology                    |
|-----------------|-------------------------------|
| Framework       | FastAPI                       |
| Database        | SQLite (async via aiosqlite)  |
| ORM             | SQLAlchemy 2.0 (async)        |
| Migrations      | Alembic                       |
| Auth            | JWT (PyJWT) + bcrypt          |
| Validation      | Pydantic v2                   |

---

## 3. Domain Model

### 3.1 User
- `id` — primary key
- `username` — unique, required, indexed
- `hashed_password` — required
- `created_at` — timestamp

### 3.2 Post
- `id` — primary key
- `title` — string, required, max 255
- `content` — text, optional
- `author_id` — FK → users.id, required, CASCADE on delete
- `is_published` — boolean, default false
- `created_at` — timestamp

**Relations:** One User has many Posts. One Post belongs to one User.

### 3.3 Comment
- `id` — primary key
- `post_id` — FK → posts.id, required, CASCADE on delete
- `author` — string, required, max 255
- `text` — text, required
- `created_at` — timestamp

**Relations:** One Post has many Comments. One Comment belongs to one Post.

---

## 4. API Endpoints

### 4.1 Auth (`/auth`)

| Method | Path       | Auth | Description                    |
|--------|------------|------|--------------------------------|
| POST   | `/register`| No   | Register new user              |
| POST   | `/login`   | No   | Login, returns JWT token       |

**Request bodies:**
- Register/Login: `{ "username": string, "password": string }`

**Response (auth):**
- `{ "access_token": string, "user_id": int }`

### 4.2 Posts (`/posts`)

| Method | Path          | Auth | Description           |
|--------|---------------|------|-----------------------|
| GET    | ``            | Yes  | List all posts        |
| POST   | ``            | Yes  | Create post           |
| GET    | `/{post_id}`  | Yes  | Get post by id        |
| PATCH  | `/{post_id}`  | Yes  | Update post           |
| DELETE | `/{post_id}`  | Yes  | Delete post           |

**Create/Update payload:**
- Create: `{ "title": string, "content"?: string, "is_published"?: boolean }`
- Update: same fields, all optional

### 4.3 Comments (`/comments`)

| Method | Path            | Auth | Description              |
|--------|-----------------|------|--------------------------|
| GET    | ``              | Yes  | List all comments        |
| POST   | ``              | Yes  | Create comment           |
| GET    | `/{comment_id}` | Yes  | Get comment by id        |
| PATCH  | `/{comment_id}` | Yes  | Update comment           |
| DELETE | `/{comment_id}` | Yes  | Delete comment           |

**Create/Update payload:**
- Create: `{ "post_id": int, "author": string, "text": string }`
- Update: same fields, all optional

**Auth:** All post and comment endpoints require `Authorization: Bearer <token>`.

---

## 5. Project Structure

```
project/
├── main.py
├── alembic.ini
├── .env
├── migrations/
│   ├── env.py
│   └── versions/
├── src/
│   ├── core/
│   │   ├── auth.py          # hash_password, verify_password, create_access_token, decode_access_token, get_current_user
│   │   ├── database.py      # async engine, session, get_session
│   │   ├── settings.py      # Pydantic Settings (DATABASE_URL, SECRET_KEY, JWT_ALGORITHM)
│   │   ├── utils.py         # response() wrapper for exceptions
│   │   └── exceptions.py    # DoesNotExists, UniqueConstraint
│   ├── models/
│   │   ├── schemas/         # SQLAlchemy models (User, Post, Comment)
│   │   └── dto/             # Pydantic schemas (Create, Update, Response)
│   ├── views/
│   │   ├── routing/         # FastAPI routers (auth, posts, comments)
│   │   ├── services/        # business logic (AuthService, PostService, CommentService)
│   │   └── interfaces/      # abstract interfaces (AuthInterface, CRUDInterface)
│   └── dependencies.py      # get_session, get_auth_service, get_post_service, get_comment_service
```

---

## 6. Implementation Requirements

### 6.1 General
- Use **English** for all identifiers, messages, and comments
- Follow async/await everywhere for DB operations
- Use type hints
- Route prefixes: `/auth`, `/posts`, `/comments`
- Path parameters: lowercase (e.g. `{post_id}`, `{comment_id}`)

### 6.2 Auth
- JWT with `sub` (user id), `exp`, `iat` claims
- Algorithm: HS256
- Password hashing: bcrypt
- Protected routes: require `Authorization: Bearer <token>`

### 6.3 Database
- Base model with `id`, `created_at`
- Table names: plural (users, posts, comments)
- Alembic: `target_metadata` from base model, autogenerate migrations

### 6.4 Layers
- **Routing:** define endpoints, use `Depends` for services and session
- **Services:** implement interfaces, call ORM, raise custom exceptions
- **Interfaces:** abstract methods for list, create, retrieve, update, delete
- **DTOs:** Pydantic models for request/response validation

### 6.5 Error Handling
- 401: invalid/expired token, user not found
- 404: resource not found (post, comment, user credentials)
- 400: unique constraint violation (e.g. username exists)
- 500: unhandled exceptions (with safe detail message)

---

## 7. Validation

- `username`: non-empty string
- `password`: non-empty string
- `title`: non-empty, max 255
- `post_id`, `comment_id`: positive integer
- `is_published`: boolean
- `author`, `text`: non-empty where required

---

## 8. Testing (Manual, via curl)

1. Register user
2. Login and get token
3. Create post
4. List posts
5. Get post by id
6. Create comment for post
7. List comments
8. Update/delete post and comment
9. Verify 401 without token
10. Verify 404 for wrong credentials

---

## 9. Differences from Reference Project

| Reference (E-commerce) | This project (Blog)      |
|------------------------|--------------------------|
| Product                | Post                     |
| Review                 | Comment                  |
| product_id in Review   | post_id in Comment       |
| rating in Review       | —                        |
| price, description     | title, content, is_published |
| —                      | author_id in Post (FK to User) |

---

## 10. Optional Extensions

- Filter posts by `is_published`
- Filter comments by `post_id`
- Ensure only post author can edit/delete their post
- Add pagination for list endpoints
