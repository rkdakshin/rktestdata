# Getting Started with Invoice Generator

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git

## Initial Setup

### 1. Clone and Navigate
```bash
cd invoice-generator
```

### 2. Database Setup
```bash
# Install PostgreSQL and create database
createdb invoice_db
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend Setup
```bash
cd frontend
npm install
```

### 5. Environment Configuration

Create `backend/.env`:
```
DATABASE_URL=postgresql://localhost/invoice_db
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

Create `frontend/.env`:
```
VITE_API_URL=http://localhost:5000
```

### 6. Run Development Servers

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### 7. Access Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Next Steps

1. Review the codebase structure
2. Check out example invoices in `/examples`
3. Read API documentation in `/PRPs`
4. Customize invoice templates as needed
