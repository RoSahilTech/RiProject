import React, { useState } from 'react';

function ReportModal({ onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    location: '',
    severity: 'medium',
    description: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const report = {
      name: 'You',
      message: formData.description,
      location: formData.location,
      time: 'Just now',
      severity: formData.severity
    };
    onSubmit(report);
    setFormData({ location: '', severity: 'medium', description: '' });
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content bg-white rounded-xl p-6 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold">Report Water-Logging Issue</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <i className="fas fa-times text-xl"></i>
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input
              type="text"
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Enter ward or area name"
              value={formData.location}
              onChange={(e) => setFormData({...formData, location: e.target.value})}
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Severity</label>
            <select
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              value={formData.severity}
              onChange={(e) => setFormData({...formData, severity: e.target.value})}
              required
            >
              <option value="low">Low - Minor accumulation</option>
              <option value="medium">Medium - Traffic affected</option>
              <option value="high">High - Major flooding</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea
              className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              rows="3"
              placeholder="Describe the issue..."
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              required
            ></textarea>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">Upload Image (Optional)</label>
            <input type="file" accept="image/*" className="w-full text-sm" />
          </div>
          <button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-2 rounded-lg hover:shadow-lg transition"
          >
            Submit Report
          </button>
        </form>
      </div>
    </div>
  );
}

export default ReportModal;

