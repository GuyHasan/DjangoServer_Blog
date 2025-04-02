# DjangoServer_Blog

A Django-based backend server for a blog application. This project provides RESTful API endpoints for articles, comments, user authentication, and more. It is configured to work with a PostgreSQL database, includes JWT-based authentication, and uses Django REST Framework for API endpoints.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Environment Setup](#environment-setup)
  - [Environment Variables](#environment-variables)
- [Libraries & Dependencies](#libraries--dependencies)
- [API Routes & Permissions](#api-routes--permissions)
  - [Articles](#articles)
  - [Comments](#comments)
  - [Authentication](#authentication)
- [Expected Request/Response Formats](#expected-requestresponse-formats)
- [Development & Running the Server](#development--running-the-server)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Articles API:** Create, read, update, and delete blog articles.
- **Comments API:** Manage comments on articles, including nested (replying) comments.
- **User Authentication:** JWT-based authentication with token refresh; includes user roles (e.g., admin, editor).
- **CORS Configuration:** Proper CORS settings for frontend integration.
- **Pagination:** API endpoints include pagination for lists of articles and comments.

---

## Prerequisites

- **Python 3.10+**
- **PostgreSQL** (for local database)
- **pip** (Python package installer)
- Recommended: Virtual Environment (venv)

---

## Installation & Setup

### Environment Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/GuyHasan/DjangoServer_Blog.git
   cd DjangoServer_Blog
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Your `requirements.txt` should include packages such as:
   > - Django
   > - djangorestframework
   > - django-cors-headers
   > - psycopg2-binary (for PostgreSQL)
   > - djangorestframework-simplejwt (for JWT authentication)
   > - Other dependencies as needed

### Environment Variables

Create a `.env` file in the root directory (or use your preferred method for managing env variables, e.g., `django-environ` or `python-decouple`).

Example `.env` file:

```
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://<username>:<password>@localhost:5432/<database_name>
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

> **Tip:** If using `django-environ` or `python-decouple`, follow their documentation for loading these values in your `settings.py`.

---

## Libraries & Dependencies

### Main Libraries:
- **Django** – The web framework.
- **Django REST Framework (DRF)** – For building RESTful APIs.
- **django-cors-headers** – To handle Cross-Origin Resource Sharing.
- **psycopg2-binary** – PostgreSQL database adapter.
- **djangorestframework-simplejwt** – JWT authentication support.
- **django-environ / python-decouple** (optional) – For managing environment variables.

### Other Dependencies:
- **Any additional packages** as listed in your `requirements.txt`.

---

## API Routes & Permissions

Below is an overview of the main routes available in your API, along with their permissions and expected request/response formats.

### **Articles**

| Method | URL                         | Permission                  | Description                                      |
|--------|-----------------------------|-----------------------------|--------------------------------------------------|
| GET    | `/api/articles/`            | Public (or IsAuthenticated) | List all articles (paginated)                    |
| GET    | `/api/articles/<id>/`       | Public                      | Retrieve a single article                        |
| POST   | `/api/articles/`            | IsAdminOrEditor             | Create a new article                             |
| PUT    | `/api/articles/<id>/`       | IsAdminOrEditor             | Replace an article completely                    |
| PATCH  | `/api/articles/<id>/`       | IsAdminOrEditor             | Update parts of an article                       |
| DELETE | `/api/articles/<id>/`       | IsAdmin                     | Delete an article                                |

### **Comments**

| Method | URL                                        | Permission         | Description                                        |
|--------|--------------------------------------------|--------------------|----------------------------------------------------|
| GET    | `/api/articles/<article_id>/comments/`     | Public             | List comments for an article (with nested replies) |
| GET    | `/api/comments/<id>/`                       | Public             | Retrieve a single comment                          |
| POST   | `/api/articles/<article_id>/comments/`     | AnyUser            | Create a comment (replying or root comment)        |
| PUT    | `/api/comments/<id>/`                       | IsOwner            | Update a comment completely                        |
| PATCH  | `/api/comments/<id>/`                       | IsOwner            | Partially update a comment                         |
| DELETE | `/api/comments/<id>/`                       | IsAdmin            | Delete a comment                                   |

### **Authentication**

| Method | URL                     | Permission | Description                                           |
|--------|-------------------------|------------|-------------------------------------------------------|
| POST   | `/api/auth/login/`      | Public     | Login and receive JWT tokens (access & refresh)       |
| POST   | `/api/auth/register/`   | Public     | Register a new user                                   |
| POST   | `/api/auth/token/refresh/` | Public  | Refresh access token using the refresh token          |

> **Note:** The JWT payload includes a `user_group` field, which is used on the frontend for permission checks.

---

## Expected Request/Response Formats

### **Articles**
- **POST `/api/articles/`**  
  **Request Body (JSON):**
  ```json
  {
    "title": "My First Article",
    "content": "This is the content of my first article."
  }
  ```
  **Response (201 Created):**
  ```json
  {
    "id": 1,
    "title": "My First Article",
    "content": "This is the content of my first article.",
    "author": 1,
    "publish_date": "2025-03-18T16:41:36.607120Z"
  }
  ```

### **Comments**
- **POST `/api/articles/<article_id>/comments/`**  
  **Request Body (JSON):**
  ```json
  {
    "content": "This is a comment.",
    "reply_to": null  // or an existing comment id for a reply
  }
  ```
  **Response (201 Created):**
  ```json
  {
    "id": 7,
    "author": 1,
    "article": 1,
    "reply_to": null,
    "content": "This is a comment.",
    "publish_date": "2025-03-31T17:09:43.344026Z"
  }
  ```

### **Authentication**
- **POST `/api/auth/login/`**  
  **Request Body (JSON):**
  ```json
  {
    "username": "admin_user",
    "password": "adminpassword"
  }
  ```
  **Response (200 OK):**
  ```json
  {
    "user": {
      "id": 1,
      "username": "admin_user",
      "user_group": "admin"
    },
    "refresh": "refresh_token_here",
    "access": "access_token_here"
  }
  ```

- **POST `/api/auth/token/refresh/`**  
  **Request Body (JSON):**
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```
  **Response (200 OK):**
  ```json
  {
    "access": "new_access_token_here"
  }
  ```

---

## Development & Running the Server

### **Backend (Django)**
1. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   The Django backend will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### **Frontend (React/Vite)**
1. **Install Dependencies:**
   ```bash
   npm install
   ```

2. **Run the Development Server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at [http://localhost:5173](http://localhost:5173).

---

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m "Add some feature"`.
4. Push the branch: `git push origin feature/my-feature`.
5. Open a pull request.

Please adhere to the coding guidelines and ensure tests pass before submitting a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
