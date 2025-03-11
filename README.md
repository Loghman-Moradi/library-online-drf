<div align="center">
    <img src="https://media.giphy.com/media/0eDNZ7gTR8z7CnmwLT/giphy.gif?cid=ecf05e47rtpz60ecy4296mw1tnzdbzaczwx7ktmqtzyiqjw5&ep=v1_gifs_search&rid=giphy.gif&ct=g" alt="Cute Cat" width="400" height="300">
</div>

# :books: E-Library REST API

This project is a RESTful API for an e-library, built using Django REST Framework. It provides endpoints for managing books, authors, user profiles, shopping carts, orders, and more.  Authentication is handled using JWT (JSON Web Tokens).

## :chart: Table of Contents

*   [Introduction](#introduction)
*   [Features](##Features)
*   [Endpoints](#endpoints)
*   [Authentication](#authentication)
*   [Authorization](#authorization)
*   [Models](#models)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Configuration](#configuration)
    *   [Running the API](#running-the-api)
*   [Contributing](#contributing)
*   [License](#license)

## Introduction

The E-Library REST API provides a backend for managing and accessing a digital library. It is designed to be used with a front-end application, allowing users to browse books, manage their profiles, place orders, and more.  The API uses JWT for secure authentication.

## Features

*   **Book Management:**
    *   List all books
    *   Retrieve details of a specific book
*   **Author Management:**
    *   Create, read, update, and delete authors (CRUD operations)
*   **User Authentication:**
    *   Send OTP (One-Time Password) for phone number verification
    *   Verify OTP to authenticate users and receive JWT tokens
    *   Refresh authentication tokens
*   **User Profile Management:**
    *   Retrieve and update user profile information
*   **Shopping Cart:**
    *   View cart items
    *   Add books to the cart
    *   Delete individual cart items
    *   Delete all cart items
*   **Order Management:**
    *   View order history
    *   Create new orders
*   **Coupon Management:**
    *   Apply coupons to orders
*   **Comments & Ratings:**
    *   Add comments to books
    *   Add ratings to books
*   **Admin Panel:**
    *   Django's built-in admin panel for easy data management
*   **PDF & Audio Book Support:**
    *   Books can have associated PDF and audio files.

## 💥 Endpoints

| Method   | Endpoint                            | Description                                    | Permissions                               |
| :------- | :---------------------------------- | :--------------------------------------------- | :---------------------------------------- |
| `GET`    | `/api/books/`                      | List all books                               | `AllowAny`                                |
| `GET`    | `/api/book_detail/<int:pk>/`       | Retrieve details of a specific book          | `AllowAny`                                |
| `POST`   | `/api_account/send-otp/`                   | Send OTP for phone number verification       | `AllowAny`                                |
| `POST`   | `/api_account/verify-otp/`                  | Verify OTP to authenticate user and receive JWT| `AllowAny`                                |
| `POST`   | `/api_account/token-refresh/`              | Refresh authentication token                 | `AllowAny` (using refresh token)         |
| `GET`    | `/api_account/profile/`                    | Retrieve user profile information            | `IsAuthenticated`                         |
| `PUT`    | `/api_account/profile/`                    | Update user profile information              | `IsAuthenticated`                         |
| `GET`    | `/api_cart/cart_page/`                  | View cart items                               | `IsAuthenticated`                         |
| `POST`   | `/api_cart/add_to_cart/<int:book_id>/`   | Add book to the cart                          | `IsAuthenticated`                         |
| `DELETE` | `/api_cart/delete_cart/<int:pk>/`        | Delete a specific cart item                   | `IsAuthenticated`                         |
| `DELETE` | `/api_cart/delete_whole_cartitems/`   | Delete all items from the cart                | `IsAuthenticated`                         |
| `GET`    | `/api_order/view_order/`                 | View order history                             | `IsAuthenticated`                         |
| `POST`   | `/api_order/create_order/`               | Create a new order                             | `IsAuthenticated`                         |
| `POST`   | `/api_order/apply_coupon/`               | Apply a coupon to an order                   | `IsAuthenticated`                         |
| `CRUD`   | `/api/authors/`                    | Create, Read, Update, Delete authors         | `IsAuthenticated`                         |
| `CRUD`   | `/api/comments/`                   | Create, Read, Update, Delete comments        | `IsAuthenticated`                         |
| `CRUD`   | `/api/ratings/`                    | Create, Read, Update, Delete ratings         | `IsAuthenticated`                         |

:exclamation: **Note:**

*   `CRUD` indicates that the endpoint supports Create, Read, Update, and Delete operations.
*   `<int:pk>` in the URL denotes an integer primary key.
*   `<int:book_id>` in the URL denotes an integer book ID.

## :bulb: Authentication

The API uses JWT (JSON Web Tokens) for authentication, provided by the `rest_framework_simplejwt` package.  Here's how authentication works:

1.  **OTP Verification:** Users request an OTP (One-Time Password) by providing their phone number to the `/api_account/send-otp/` endpoint.
2.  **OTP Submission:**  The user then submits the received OTP to the `/api_account/verify-otp/` endpoint.  If the OTP is valid:
    *   A new user account is created if one doesn't exist.
    *   A JWT access token and refresh token are generated.
    *   These tokens are returned in the response.
3.  **JWT Usage:** The access token must be included in the `Authorization` header of subsequent requests that require authentication. The header should be in the format `Bearer <access_token>`.
4.  **Token Refresh:** Access tokens have a limited lifespan.  When an access token expires, a new access token can be obtained by sending the refresh token to the `/api_account/token-refresh/` endpoint.

## :closed_lock_with_key: Authorization

*   `AllowAny`: The endpoint is accessible to anyone, regardless of authentication status.
*   `IsAuthenticated`: The endpoint is only accessible to authenticated users who have a valid JWT access token.


## :rocket: Getting Started

### :red_circle: Prerequisites

*   Python (3.8+)
*   pip
*   Django
*   Django REST Framework
*   `djangorestframework-simplejwt`
*   Any other dependencies listed in `requirements.txt` (if available)

### :red_circle: Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/Loghman-Moradi/library-online-drf.git
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### :red_circle: Configuration

1.  Create a `.env` file in the project root directory.

2.  Set the following environment variables:

    *   `SECRET_KEY`: Django secret key
    *   `DATABASE_URL`: Database connection URL
    *   Any other environment variables required by your project (e.g., for SMS services)

3.  Update the `settings.py` file to read environment variables using a library like `python-dotenv`.

4.  **JWT Configuration:**  Verify that `REST_FRAMEWORK` and `SIMPLE_JWT` settings are correctly configured in your `settings.py` as shown below.  These settings control JWT authentication.

    ```python
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
    }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(weeks=3),
        'REFRESH_TOKEN_LIFETIME': timedelta(weeks=4),
    }
    ```

5.  **Custom User Model:** Confirm that `AUTH_USER_MODEL` is correctly set in `settings.py`:

    ```python
    AUTH_USER_MODEL = 'Account.LibraryUsers'
    ```

### :wrench: Running the API

1.  Apply migrations:

    ```bash
    python manage.py migrate
    ```

2.  Create a superuser (for accessing the admin panel):

    ```bash
    python manage.py createsuperuser
    ```

3.  Run the development server:

    ```bash
    python manage.py runserver
    ```

The API will be accessible at `http://localhost:8000/`.

## :white_check_mark: License

This project is licensed under the MIT License
