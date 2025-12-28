# API Examples

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Get All Invoices
```bash
GET /api/invoices
```

**Response:**
```json
{
  "invoices": [
    {
      "id": 1,
      "invoice_number": "INV-2024-001",
      "client_name": "Acme Corporation",
      "total": 7277.25,
      "status": "draft"
    }
  ]
}
```

### 2. Get Single Invoice
```bash
GET /api/invoices/1
```

**Response:**
```json
{
  "invoice": {
    "id": 1,
    "invoice_number": "INV-2024-001",
    "invoice_date": "2024-01-15",
    "due_date": "2024-02-15",
    "client_name": "Acme Corporation",
    "items": [...],
    "total": 7277.25
  }
}
```

### 3. Create Invoice
```bash
POST /api/invoices
Content-Type: application/json

{
  "invoice_number": "INV-2024-002",
  "invoice_date": "2024-01-20",
  "due_date": "2024-02-20",
  "client_name": "New Client Inc",
  "tax_rate": 8.5,
  "discount": 0,
  "items": [
    {
      "description": "Service A",
      "quantity": 2,
      "unit_price": 100.00
    }
  ]
}
```

**Response:**
```json
{
  "invoice": {...},
  "message": "Invoice created successfully"
}
```

### 4. Update Invoice
```bash
PUT /api/invoices/1
Content-Type: application/json

{
  "status": "paid"
}
```

**Response:**
```json
{
  "invoice": {...},
  "message": "Invoice updated successfully"
}
```

### 5. Delete Invoice
```bash
DELETE /api/invoices/1
```

**Response:**
```json
{
  "message": "Invoice deleted successfully"
}
```

### 6. Download PDF
```bash
GET /api/invoices/1/pdf
```

**Response:**
Binary PDF file download

## Using cURL

### Create Invoice Example
```bash
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d @examples/sample_invoice.json
```

### Get All Invoices
```bash
curl http://localhost:5000/api/invoices
```

### Download PDF
```bash
curl http://localhost:5000/api/invoices/1/pdf --output invoice.pdf
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: client_name"
}
```

### 404 Not Found
```json
{
  "error": "Invoice not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Database error message"
}
```
