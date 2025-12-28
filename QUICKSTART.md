# Quick Start Guide

Get your Invoice Generator up and running in minutes!

## Prerequisites

Make sure you have these installed:
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git (optional)

## Quick Setup (Windows)

### Option 1: Using Setup Script (Recommended)

1. Run the setup script:
```bash
setup.bat
```

2. Create PostgreSQL database:
```bash
createdb invoice_db
```

3. Configure environment variables:
```bash
# Copy example files
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env

# Edit backend\.env with your database credentials
```

4. Start the application:
```bash
start.bat
```

5. Open browser:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env file with your settings
python app.py
```

#### Frontend Setup (in new terminal)
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

## Quick Setup (Mac/Linux)

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env file
python app.py
```

### Frontend Setup (in new terminal)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Create Your First Invoice

1. Open http://localhost:5173
2. Click "Create New Invoice"
3. Fill in the form:
   - Invoice details (number, dates)
   - Client information
   - Company information
   - Add line items
   - Set tax rate and discount
4. Click "Create Invoice"
5. View your invoice in the list
6. Download PDF by clicking "PDF" button

## Testing the API

### Using curl:
```bash
# Get all invoices
curl http://localhost:5000/api/invoices

# Create invoice from example
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d @examples/sample_invoice.json

# Download PDF
curl http://localhost:5000/api/invoices/1/pdf --output invoice.pdf
```

### Using the frontend:
1. Navigate to http://localhost:5173
2. Use the UI to create, view, edit, and delete invoices

## Project Structure

```
invoice-generator/
├── backend/          # Flask API
│   ├── models/       # Database models
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   └── app.py        # Main application
├── frontend/         # React app
│   └── src/
│       ├── components/  # React components
│       ├── services/    # API client
│       ├── types/       # TypeScript types
│       └── hooks/       # Custom hooks
├── skills/           # Reusable utilities
├── examples/         # Sample data
└── PRPs/            # Documentation

```

## Common Issues

### Database Connection Error
- Make sure PostgreSQL is running
- Check DATABASE_URL in backend/.env
- Create the database: `createdb invoice_db`

### Frontend Can't Connect to Backend
- Verify backend is running on port 5000
- Check VITE_API_URL in frontend/.env
- Check CORS settings in backend/config.py

### Port Already in Use
- Backend: Change PORT in backend/.env
- Frontend: Change port in frontend/vite.config.ts

## Next Steps

- Customize invoice templates in `backend/services/pdf_service.py`
- Add your company logo and branding
- Explore the API documentation in `PRPs/api_examples.md`
- Check out skills for reusable utilities

## Support

For issues or questions:
- Check INITIAL.md for detailed setup
- Review API examples in PRPs/api_examples.md
- Read CLAUDE.md for development with Claude

Happy invoicing!
