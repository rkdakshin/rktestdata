import React from 'react';
import { Invoice } from '../types/invoice.types';

interface InvoicePreviewProps {
  invoice: Invoice;
}

export const InvoicePreview: React.FC<InvoicePreviewProps> = ({ invoice }) => {
  return (
    <div className="max-w-4xl mx-auto bg-white p-8 shadow-lg rounded-lg">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">INVOICE</h1>
      </div>

      {/* Company and Client Info */}
      <div className="grid grid-cols-2 gap-8 mb-8">
        <div>
          <h2 className="text-sm font-semibold text-gray-600 mb-2">FROM:</h2>
          <p className="font-semibold text-gray-800">{invoice.company_name || 'Your Company'}</p>
          <p className="text-gray-600 text-sm whitespace-pre-line">{invoice.company_address}</p>
          <p className="text-gray-600 text-sm">{invoice.company_email}</p>
          <p className="text-gray-600 text-sm">{invoice.company_phone}</p>
        </div>
        <div>
          <h2 className="text-sm font-semibold text-gray-600 mb-2">TO:</h2>
          <p className="font-semibold text-gray-800">{invoice.client_name}</p>
          <p className="text-gray-600 text-sm whitespace-pre-line">{invoice.client_address}</p>
          <p className="text-gray-600 text-sm">{invoice.client_email}</p>
          <p className="text-gray-600 text-sm">{invoice.client_phone}</p>
        </div>
      </div>

      {/* Invoice Details */}
      <div className="grid grid-cols-2 gap-4 mb-8 bg-gray-50 p-4 rounded">
        <div>
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Invoice Number:</span> {invoice.invoice_number}
          </p>
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Status:</span>{' '}
            <span className="uppercase font-medium">{invoice.status}</span>
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Date:</span> {invoice.invoice_date}
          </p>
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Due Date:</span> {invoice.due_date}
          </p>
        </div>
      </div>

      {/* Line Items Table */}
      <div className="mb-8">
        <table className="w-full">
          <thead className="bg-gray-700 text-white">
            <tr>
              <th className="text-left p-3">Description</th>
              <th className="text-center p-3">Quantity</th>
              <th className="text-center p-3">Unit Price</th>
              <th className="text-right p-3">Amount</th>
            </tr>
          </thead>
          <tbody className="bg-gray-50">
            {invoice.items.map((item, index) => (
              <tr key={index} className="border-b border-gray-200">
                <td className="p-3">{item.description}</td>
                <td className="text-center p-3">{item.quantity}</td>
                <td className="text-center p-3">${item.unit_price.toFixed(2)}</td>
                <td className="text-right p-3">${item.amount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Totals */}
      <div className="flex justify-end mb-8">
        <div className="w-64 space-y-2">
          <div className="flex justify-between text-gray-700">
            <span>Subtotal:</span>
            <span>${invoice.subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-gray-700">
            <span>Tax ({invoice.tax_rate}%):</span>
            <span>${invoice.tax_amount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-gray-700">
            <span>Discount:</span>
            <span>${invoice.discount.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-xl font-bold text-gray-900 pt-2 border-t-2 border-gray-800">
            <span>Total:</span>
            <span>${invoice.total.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Notes and Terms */}
      {invoice.notes && (
        <div className="mb-4">
          <h3 className="font-semibold text-gray-800 mb-2">Notes:</h3>
          <p className="text-gray-600 text-sm whitespace-pre-line">{invoice.notes}</p>
        </div>
      )}

      {invoice.terms && (
        <div>
          <h3 className="font-semibold text-gray-800 mb-2">Terms:</h3>
          <p className="text-gray-600 text-sm whitespace-pre-line">{invoice.terms}</p>
        </div>
      )}
    </div>
  );
};
