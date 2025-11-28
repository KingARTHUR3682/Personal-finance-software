# Haak Personal Finance Software (HaakPFS)

**HaakPFS** is a full-stack personal finance and bookkeeping application designed to help users track expenses, manage income, and organize financial records. Developed as a Final Year Project, it leverages a modern web architecture to provide secure, cloud-based financial management.

## 🚀 Live Demo & Deployment

* **Frontend**: Hosted on [Cloudflare](https://pages.cloudflare.com/)
* **Backend**: Containerized and hosted on [Google Cloud Platform](https://cloud.google.com/)
* **Database**: Managed PostgreSQL on [Supabase](https://supabase.com/)
* **Storage**: Media/Receipts stored via [Google Cloud Storage](https://cloud.google.com/storage)

## ✨ Features

* **Transaction Tracking**: Log both **Income** and **Expenses** with detailed descriptions and amounts.
* **Smart Categorization**: Organize finances with hierarchical categories (Parent & Subcategories) and custom icons.
* **Receipt Management**: Upload and store digital copies of receipts directly with transaction records.
* **User Authentication**: Secure registration and login using JWT (JSON Web Tokens).
* **Profile Management**: Manage user details and settings.
* **Security**: Includes password reset functionality via email and secure session handling.
* **Dashboard**: Visual overview of your financial status.

## 🛠 Tech Stack

### Frontend
* **Framework**: [Vue.js 3](https://vuejs.org/) (Script Setup)
* **Build Tool**: [Vite](https://vitejs.dev/)
* **State Management**: [Pinia](https://pinia.vuejs.org/)
* **HTTP Client**: Axios
* **Routing**: Vue Router

### Backend
* **Framework**: [Django 5.2](https://www.djangoproject.com/)
* **API**: Django REST Framework (DRF)
* **Authentication**: SimpleJWT
* **Database Interface**: `dj-database-url` with `psycopg2`
* **Storage**: `django-storages` with Google Cloud Storage
* **Server**: Gunicorn

## ⚙️ Local Development Setup

Follow these steps to run the project locally.

### Prerequisites
* Node.js (v20+ recommended)
* Python (v3.10+)
* PostgreSQL (or SQLite for local testing)

### 1. Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd personal-finance-software/backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the `backend/` root directory. Add the following variables (based on `settings.py`):
    ```ini
    # Django Settings
    SECRET_KEY=your_secret_key_here
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Database (Supabase or Local Postgres)
    DATABASE_URL=postgres://user:password@host:port/dbname

    # Google Cloud Storage (For Receipt Uploads)
    GS_BUCKET_NAME=your_bucket_name
    GS_PROJECT_ID=your_project_id
    # Ensure your Google credentials JSON is set up if running locally

    # Email Settings (For Password Reset)
    EMAIL_HOST_PASSWORD=your_app_password
    FRONTEND_URL=http://localhost:5173
    ```

5.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend/app
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the Vite Development Server:**
    ```bash
    npm run dev
    ```

4.  Access the app at `http://localhost:5173`.

## 🐳 Docker Support

The backend includes a `Dockerfile` for containerization. To build and run the backend container:

```bash
cd backend
docker build -t haak-backend .
docker run -p 8080:8080 --env-file .env haak-backend
