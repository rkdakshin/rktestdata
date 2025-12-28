# Invoice Generator MicroSaaS

A modern invoice generator built with React TypeScript and Python Flask.

## Tech Stack

### Frontend
- React + TypeScript (Vite)
- Tailwind CSS
- React Hook Form
- Axios

### Backend
- Flask (Python)
- PostgreSQL
- SQLAlchemy
- ReportLab (PDF Generation)

## Project Structure

```
invoice-generator/
├── .claude/              # Claude configuration
├── agents/               # AI agents for automation
├── skills/               # Reusable components/utilities
├── examples/             # Sample invoices and templates
├── backend/              # Flask API
├── frontend/             # React + TypeScript
├── database/             # Database migrations
└── PRPs/                 # Documentation
```

## Features

- Create and manage invoices
- Professional PDF generation
- Live invoice preview
- Responsive design
- PostgreSQL database storage

## Getting Started

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create `.env` files in both backend and frontend directories. See `.env.example` for required variables.

## License

MIT
