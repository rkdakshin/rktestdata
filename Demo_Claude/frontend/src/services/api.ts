import axios from 'axios';
import { Invoice, InvoiceFormData } from '../types/invoice.types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const invoiceApi = {
  // Get all invoices
  getAll: async (): Promise<Invoice[]> => {
    const response = await api.get('/api/invoices');
    return response.data.invoices;
  },

  // Get single invoice
  getById: async (id: number): Promise<Invoice> => {
    const response = await api.get(`/api/invoices/${id}`);
    return response.data.invoice;
  },

  // Create new invoice
  create: async (data: InvoiceFormData): Promise<Invoice> => {
    const response = await api.post('/api/invoices', data);
    return response.data.invoice;
  },

  // Update invoice
  update: async (id: number, data: Partial<InvoiceFormData>): Promise<Invoice> => {
    const response = await api.put(`/api/invoices/${id}`, data);
    return response.data.invoice;
  },

  // Delete invoice
  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/invoices/${id}`);
  },

  // Download PDF
  downloadPDF: async (id: number, invoiceNumber: string): Promise<void> => {
    const response = await api.get(`/api/invoices/${id}/pdf`, {
      responseType: 'blob',
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `invoice_${invoiceNumber}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};

export default api;
