# Sneakers Ecommerce Website

Welcome to the **Sneakers Ecommerce Website** project! This is a fully functional ecommerce platform built using the Django web framework. The platform allows users to browse, search, and purchase sneakers, while also providing administrators with tools to manage the product catalog, user accounts, and orders.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Project Status](#project-status)

---

## Features

### User Features
- Browse a catalog of sneakers with images, descriptions, and prices.
- User registration and login system.
- Add sneakers to a shopping cart and proceed to checkout.
- Secure online payment integration using SSLCommerz Sandbox for transaction processing.
- View order history and order status.

### Admin Features
- Admin dashboard to manage products, categories, and orders.
- Add, edit, or remove products from the catalog.
- Track and update order statuses.

---

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript (Bootstrap for styling)
- **Backend**: Django (Python)
- **Database**: SQLite (default)
- **Payment Gateway**: SSLCOMMERZ Sandbox

---

## Installation

### Prerequisites
1. Python 3.8+
2. Virtual environment tool (venv or virtualenv).
3. SSLCOMMERZ Sandbox Payment System Registration.

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/sneakers-ecommerce.git
   cd sneakers-ecommerce
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Website:**
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Usage

### Development
1. Run the Django server locally:
   ```bash
   python manage.py runserver
   ```
2. Modify templates, static files, or models to customize the project.
3. Use the Django admin panel for quick management of data: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

### Deployment
This project includes Docker support for deployment. Follow these steps:
1. Build and run Docker containers:
   ```bash
   docker-compose up --build
   ```
2. Access the application on your server's public IP or domain.

---

## Project Structure
_Note:_ _Will be updated soon._

---

## Project status
- [ ] This is a complete project.
- [x] This project is on hold.
- [ ] This is an incomplete project.

# Let's go! Have some coding! 🙂
