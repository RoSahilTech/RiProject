import React from 'react';

function StatsCards({ stats }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div className="glass-effect rounded-xl p-4 action-card">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm">Total Wards</p>
            <p className="text-2xl font-bold">{stats.totalWards || 30}</p>
          </div>
          <i className="fas fa-map-marked-alt text-3xl text-blue-500"></i>
        </div>
      </div>
      <div className="glass-effect rounded-xl p-4 action-card risk-high">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-white/80 text-sm">High Risk</p>
            <p className="text-2xl font-bold">{stats.highRisk || 0}</p>
          </div>
          <i className="fas fa-exclamation-triangle text-3xl animate-pulse-slow"></i>
        </div>
      </div>
      <div className="glass-effect rounded-xl p-4 action-card risk-medium">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-700 text-sm">Medium Risk</p>
            <p className="text-2xl font-bold">{stats.mediumRisk || 0}</p>
          </div>
          <i className="fas fa-exclamation-circle text-3xl"></i>
        </div>
      </div>
      <div className="glass-effect rounded-xl p-4 action-card risk-low">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-white/80 text-sm">Low Risk</p>
            <p className="text-2xl font-bold">{stats.lowRisk || 0}</p>
          </div>
          <i className="fas fa-check-circle text-3xl"></i>
        </div>
      </div>
    </div>
  );
}

export default StatsCards;

