import React, { useState } from 'react';
import { InvoiceForm } from './components/InvoiceForm';
import { InvoiceList } from './components/InvoiceList';
import { InvoicePreview } from './components/InvoicePreview';
import { useInvoices } from './hooks/useInvoice';
import { Invoice } from './types/invoice.types';

type View = 'list' | 'create' | 'edit' | 'preview';

function App() {
  const { invoices, loading, error, refetch } = useInvoices();
  const [currentView, setCurrentView] = useState<View>('list');
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);

  const handleCreateNew = () => {
    setSelectedInvoice(null);
    setCurrentView('create');
  };

  const handleEdit = (invoice: Invoice) => {
    setSelectedInvoice(invoice);
    setCurrentView('edit');
  };

  const handleView = (invoice: Invoice) => {
    setSelectedInvoice(invoice);
    setCurrentView('preview');
  };

  const handleFormSuccess = () => {
    refetch();
    setCurrentView('list');
    setSelectedInvoice(null);
  };

  const handleBackToList = () => {
    setCurrentView('list');
    setSelectedInvoice(null);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">Invoice Generator</h1>
            <div className="space-x-4">
              <button
                onClick={handleBackToList}
                className={`px-4 py-2 rounded-md ${
                  currentView === 'list'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                All Invoices
              </button>
              <button
                onClick={handleCreateNew}
                className={`px-4 py-2 rounded-md ${
                  currentView === 'create'
                    ? 'bg-green-600 text-white'
                    : 'bg-green-500 text-white hover:bg-green-600'
                }`}
              >
                Create New Invoice
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading && currentView === 'list' ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">Loading invoices...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        ) : (
          <>
            {currentView === 'list' && (
              <InvoiceList
                invoices={invoices}
                onEdit={handleEdit}
                onView={handleView}
                onRefresh={refetch}
              />
            )}

            {currentView === 'create' && (
              <InvoiceForm onSuccess={handleFormSuccess} />
            )}

            {currentView === 'edit' && selectedInvoice && (
              <InvoiceForm
                onSuccess={handleFormSuccess}
                initialData={selectedInvoice}
                invoiceId={selectedInvoice.id}
              />
            )}

            {currentView === 'preview' && selectedInvoice && (
              <div className="space-y-4">
                <button
                  onClick={handleBackToList}
                  className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
                >
                  Back to List
                </button>
                <InvoicePreview invoice={selectedInvoice} />
              </div>
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-gray-500 text-sm">
            Invoice Generator - Built with React TypeScript & Flask
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
