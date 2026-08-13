# 📦 Warehouse Management System (Django REST Framework)

A progressive REST API backend system designed for automating warehouse inventory tracking and stock management. Built with a focus on data security, granular access control, advanced query filtering, and relational database integrity.

---
## 🚀 Key Features

* **Full Inventory CRUD:** Complete management of products and categories via REST API endpoints.
* **Custom Business Logic (`reduce_stock`):** Specialized endpoint for real-time item stock deduction and validation.
* **Smart Search & Filtering:** Filter products by category, perform full-text searches by title/SKU, and dynamically sort by price.
* **Role-Based Security:** Granular access permissions that restrict data modification features exclusively to authorized admin users.

## 🛠️ Tech Stack

* **Backend:** Python 3.11, Django 5.x, Django REST Framework (DRF)
* **Database:** PostgreSQL (relational database for strict data integrity)
* **Tools:** `django-filter` (for dynamic API filtering)

## 📋 API Map

| Method | URL | Description | Access |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/products/` | Retrieve product list with search/filtering | Public (Guest) |
| **POST** | `/api/products/` | Create a new product entry | Admin only |
| **POST** | `/api/products/{id}/reduce_stock/` | Custom stock deduction endpoint | Admin only |
| **DELETE** | `/api/products/{id}/` | Remove product from database | Admin only |
| **GET** | `/api/categories/` | Retrieve list of available categories | Public (Guest) |

### 🔍 API Query Examples:
* **Search by title / SKU:** `/api/products/?search=laptop`
* **Sort by price:** `/api/products/?ordering=price`
* **Filter by category ID:** `/api/products/?category=1`

---

## 🏛️ Architectural Decisions & Engineering Context

* **Data Layer (PostgreSQL):** Unlike file-based databases, a production-grade relational database ensures ACID transactions, strict typing, and reliable foreign key relationships between categories and items.
* **Granular Access Control:** Uses DRF's `IsAuthenticatedOrReadOnly` permission logic. Authentication layer (`SessionAuthentication` / `BasicAuthentication`) is clean-cut and independent from business logic.
* **Business Logic Separation:** Custom operations (e.g., `reduce_stock`) are encapsulated inside ViewSet methods via the `@action` decorator, maintaining a clean **Thin Controller / Fat Model** structure.
* **Data Integrity:** Strict input data validation is enforced via Serializers to protect the database layer against malformed requests.

## **🚀 Getting Started**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AlinaFetisova/Warehouse_postgresql.git
   cd Warehouse_postgresql
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
