export interface InvoiceItem {
  id?: number;
  description: string;
  quantity: number;
  unit_price: number;
  amount: number;
}

export interface Invoice {
  id?: number;
  invoice_number: string;
  invoice_date: string;
  due_date: string;

  client_name: string;
  client_email?: string;
  client_address?: string;
  client_phone?: string;

  company_name?: string;
  company_address?: string;
  company_email?: string;
  company_phone?: string;

  subtotal: number;
  tax_rate: number;
  tax_amount: number;
  discount: number;
  total: number;

  notes?: string;
  terms?: string;
  status: 'draft' | 'sent' | 'paid' | 'cancelled';

  items: InvoiceItem[];

  created_at?: string;
  updated_at?: string;
}

export interface InvoiceFormData {
  invoice_number: string;
  invoice_date: string;
  due_date: string;

  client_name: string;
  client_email: string;
  client_address: string;
  client_phone: string;

  company_name: string;
  company_address: string;
  company_email: string;
  company_phone: string;

  tax_rate: number;
  discount: number;
  notes: string;
  terms: string;
  status: 'draft' | 'sent' | 'paid' | 'cancelled';

  items: InvoiceItem[];
}
