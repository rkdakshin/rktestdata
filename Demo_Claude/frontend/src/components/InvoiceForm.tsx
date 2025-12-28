import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { InvoiceFormData, InvoiceItem } from '../types/invoice.types';
import { invoiceApi } from '../services/api';

interface InvoiceFormProps {
  onSuccess?: () => void;
  initialData?: InvoiceFormData;
  invoiceId?: number;
}

export const InvoiceForm: React.FC<InvoiceFormProps> = ({ onSuccess, initialData, invoiceId }) => {
  const { register, handleSubmit, watch, setValue } = useForm<InvoiceFormData>({
    defaultValues: initialData || {
      invoice_number: `INV-${Date.now()}`,
      invoice_date: new Date().toISOString().split('T')[0],
      due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      client_name: '',
      client_email: '',
      client_address: '',
      client_phone: '',
      company_name: 'Your Company',
      company_address: '',
      company_email: '',
      company_phone: '',
      tax_rate: 0,
      discount: 0,
      notes: '',
      terms: 'Payment due within 30 days',
      status: 'draft',
      items: [{ description: '', quantity: 1, unit_price: 0, amount: 0 }],
    },
  });

  const [items, setItems] = useState<InvoiceItem[]>(
    initialData?.items || [{ description: '', quantity: 1, unit_price: 0, amount: 0 }]
  );
  const [loading, setLoading] = useState(false);

  const calculateItemAmount = (quantity: number, unitPrice: number) => {
    return quantity * unitPrice;
  };

  const updateItem = (index: number, field: keyof InvoiceItem, value: string | number) => {
    const newItems = [...items];
    newItems[index] = { ...newItems[index], [field]: value };

    if (field === 'quantity' || field === 'unit_price') {
      newItems[index].amount = calculateItemAmount(
        Number(newItems[index].quantity),
        Number(newItems[index].unit_price)
      );
    }

    setItems(newItems);
    setValue('items', newItems);
  };

  const addItem = () => {
    setItems([...items, { description: '', quantity: 1, unit_price: 0, amount: 0 }]);
  };

  const removeItem = (index: number) => {
    if (items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
      setValue('items', newItems);
    }
  };

  const onSubmit = async (data: InvoiceFormData) => {
    try {
      setLoading(true);
      data.items = items;

      if (invoiceId) {
        await invoiceApi.update(invoiceId, data);
      } else {
        await invoiceApi.create(data);
      }

      if (onSuccess) {
        onSuccess();
      }

      alert(invoiceId ? 'Invoice updated successfully!' : 'Invoice created successfully!');
    } catch (error) {
      console.error('Error saving invoice:', error);
      alert('Failed to save invoice. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const subtotal = items.reduce((sum, item) => sum + item.amount, 0);
  const taxRate = watch('tax_rate') || 0;
  const discount = watch('discount') || 0;
  const taxAmount = (subtotal * taxRate) / 100;
  const total = subtotal + taxAmount - discount;

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold text-gray-800">
        {invoiceId ? 'Edit Invoice' : 'Create New Invoice'}
      </h2>

      {/* Invoice Details */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Invoice Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Invoice Number</label>
            <input
              {...register('invoice_number', { required: true })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Invoice Date</label>
            <input
              type="date"
              {...register('invoice_date', { required: true })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Due Date</label>
            <input
              type="date"
              {...register('due_date', { required: true })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
        </div>
      </div>

      {/* Client Details */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Client Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Client Name</label>
            <input
              {...register('client_name', { required: true })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Client Email</label>
            <input
              type="email"
              {...register('client_email')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Client Phone</label>
            <input
              {...register('client_phone')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Client Address</label>
            <textarea
              {...register('client_address')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              rows={2}
            />
          </div>
        </div>
      </div>

      {/* Company Details */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Company Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Company Name</label>
            <input
              {...register('company_name')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Company Email</label>
            <input
              type="email"
              {...register('company_email')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Company Phone</label>
            <input
              {...register('company_phone')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Company Address</label>
            <textarea
              {...register('company_address')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              rows={2}
            />
          </div>
        </div>
      </div>

      {/* Line Items */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Line Items</h3>
        <div className="space-y-4">
          {items.map((item, index) => (
            <div key={index} className="grid grid-cols-12 gap-2 items-end">
              <div className="col-span-5">
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <input
                  value={item.description}
                  onChange={(e) => updateItem(index, 'description', e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                  placeholder="Item description"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Quantity</label>
                <input
                  type="number"
                  value={item.quantity}
                  onChange={(e) => updateItem(index, 'quantity', parseFloat(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                  min="0"
                  step="0.01"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Unit Price</label>
                <input
                  type="number"
                  value={item.unit_price}
                  onChange={(e) => updateItem(index, 'unit_price', parseFloat(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
                  min="0"
                  step="0.01"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Amount</label>
                <input
                  type="number"
                  value={item.amount.toFixed(2)}
                  readOnly
                  className="mt-1 block w-full rounded-md border-gray-300 bg-gray-50 shadow-sm p-2 border"
                />
              </div>
              <div className="col-span-1">
                <button
                  type="button"
                  onClick={() => removeItem(index)}
                  className="w-full bg-red-500 text-white p-2 rounded-md hover:bg-red-600"
                  disabled={items.length === 1}
                >
                  X
                </button>
              </div>
            </div>
          ))}
        </div>
        <button
          type="button"
          onClick={addItem}
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
        >
          Add Item
        </button>
      </div>

      {/* Totals */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Totals</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tax Rate (%)</label>
            <input
              type="number"
              {...register('tax_rate')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Discount ($)</label>
            <input
              type="number"
              {...register('discount')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              min="0"
              step="0.01"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <select
              {...register('status')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            >
              <option value="draft">Draft</option>
              <option value="sent">Sent</option>
              <option value="paid">Paid</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>
        <div className="mt-4 text-right space-y-2">
          <p className="text-gray-700">Subtotal: ${subtotal.toFixed(2)}</p>
          <p className="text-gray-700">Tax ({taxRate}%): ${taxAmount.toFixed(2)}</p>
          <p className="text-gray-700">Discount: ${discount.toFixed(2)}</p>
          <p className="text-xl font-bold text-gray-900">Total: ${total.toFixed(2)}</p>
        </div>
      </div>

      {/* Additional Info */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Additional Information</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Notes</label>
            <textarea
              {...register('notes')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              rows={3}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Terms</label>
            <textarea
              {...register('terms')}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
              rows={3}
            />
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className="bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 disabled:bg-gray-400"
        >
          {loading ? 'Saving...' : invoiceId ? 'Update Invoice' : 'Create Invoice'}
        </button>
      </div>
    </form>
  );
};
