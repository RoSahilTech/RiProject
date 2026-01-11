import React from 'react';

function Sidebar({ liveUpdates, citizenReports, wardData, selectedWard, onWardClick, onReportClick }) {
  const getRiskClass = (riskLevel) => {
    if (riskLevel === 2) return 'bg-red-50 border-red-500 text-red-800';
    if (riskLevel === 1) return 'bg-yellow-50 border-yellow-500 text-yellow-800';
    return 'bg-green-50 border-green-500 text-green-800';
  };

  const getRiskLabel = (riskLevel) => {
    if (riskLevel === 2) return 'High Risk';
    if (riskLevel === 1) return 'Medium Risk';
    return 'Low Risk';
  };

  const defaultUpdates = [
    {
      ward: 'Karol Bagh',
      message: 'Severe water-logging detected',
      time: '2m ago',
      type: 'alert',
      risk: 2
    },
    {
      ward: 'Dwarka Sector 21',
      message: 'Moderate risk - Drain blockage',
      time: '15m ago',
      type: 'warning',
      risk: 1
    },
    {
      ward: 'Connaught Place',
      message: 'Issue resolved - Pumping complete',
      time: '30m ago',
      type: 'info',
      risk: 0
    }
  ];

  const updates = liveUpdates.length > 0 ? liveUpdates : defaultUpdates;

  const defaultReports = [
    {
      name: 'Anonymous',
      message: 'Heavy water-logging near Metro Station',
      location: 'Rajouri Garden',
      time: '5 min ago'
    },
    {
      name: 'Resident',
      message: 'Drain overflow in main market',
      location: 'Lajpat Nagar',
      time: '12 min ago'
    }
  ];

  const reports = citizenReports.length > 0 ? citizenReports : defaultReports;

  return (
    <div className="space-y-6">
      {/* Live Updates */}
      <div className="glass-effect rounded-xl p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">
          <i className="fas fa-broadcast-tower text-red-500 mr-2"></i>
          Live Updates
        </h3>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {updates.map((update, index) => {
            const riskClass = getRiskClass(update.risk ?? 2);
            return (
              <div
                key={index}
                className={`sidebar-item border-l-4 p-3 rounded cursor-pointer ${riskClass}`}
                onClick={() => onWardClick(update.ward)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold">{update.ward}</p>
                    <p className="text-xs text-gray-600 mt-1">{update.message}</p>
                  </div>
                  <span className="text-xs bg-gray-500 text-white px-2 py-1 rounded">
                    {update.time}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommended Actions */}
      <div className="glass-effect rounded-xl p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">
          <i className="fas fa-tasks text-purple-500 mr-2"></i>
          AI Recommended Actions
        </h3>
        <div className="space-y-3">
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border-l-4 border-purple-500">
            <p className="font-semibold text-purple-800">Immediate: Deploy pumps</p>
            <p className="text-sm text-gray-600 mt-1">
              {selectedWard} - {wardData[selectedWard]?.flood_risk_level === 2 ? 'Critical water levels' : 'Monitoring'}
            </p>
            <button className="mt-2 text-xs bg-purple-600 text-white px-3 py-1 rounded-full hover:bg-purple-700 transition">
              Take Action
            </button>
          </div>
          <div className="bg-gradient-to-r from-blue-50 to-cyan-50 p-4 rounded-lg border-l-4 border-blue-500">
            <p className="font-semibold text-blue-800">Preventive: Clean drains</p>
            <p className="text-sm text-gray-600 mt-1">Multiple wards - Before monsoon</p>
            <button className="mt-2 text-xs bg-blue-600 text-white px-3 py-1 rounded-full hover:bg-blue-700 transition">
              Schedule
            </button>
          </div>
        </div>
      </div>

      {/* Citizen Reports */}
      <div className="glass-effect rounded-xl p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">
          <i className="fas fa-users text-green-500 mr-2"></i>
          Recent Citizen Reports
        </h3>
        <div className="space-y-3">
          {reports.slice(0, 5).map((report, index) => (
            <div key={index} className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-semibold">
                {report.name.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold">{report.name}</p>
                <p className="text-xs text-gray-600">{report.message}</p>
                <p className="text-xs text-gray-400">{report.location} • {report.time}</p>
              </div>
            </div>
          ))}
        </div>
        <button
          onClick={onReportClick}
          className="w-full mt-4 bg-gradient-to-r from-green-500 to-teal-500 text-white py-2 rounded-lg hover:shadow-lg transition"
        >
          <i className="fas fa-plus-circle mr-2"></i>Submit Report
        </button>
      </div>

      {/* Ward Details Card */}
      {wardData[selectedWard] && (
        <div className="glass-effect rounded-xl p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">
            <i className="fas fa-info-circle text-blue-500 mr-2"></i>
            {selectedWard} Details
          </h3>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Flood Risk:</span>
              <span className={`font-bold ${
                wardData[selectedWard].flood_risk_level === 2 ? 'text-red-600' :
                wardData[selectedWard].flood_risk_level === 1 ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {getRiskLabel(wardData[selectedWard].flood_risk_level)}
              </span>
            </div>
            {wardData[selectedWard].max_flood_depth_cm && (
              <div className="flex justify-between">
                <span className="text-gray-600">Max Depth:</span>
                <span className="font-semibold">{wardData[selectedWard].max_flood_depth_cm.toFixed(1)} cm</span>
              </div>
            )}
            {wardData[selectedWard].drain_capacity_score && (
              <div className="flex justify-between">
                <span className="text-gray-600">Drainage Health:</span>
                <span className="font-semibold">{(wardData[selectedWard].drain_capacity_score * 100).toFixed(0)}%</span>
              </div>
            )}
            {wardData[selectedWard].citizen_reports_count !== undefined && (
              <div className="flex justify-between">
                <span className="text-gray-600">Citizen Reports:</span>
                <span className="font-semibold">{wardData[selectedWard].citizen_reports_count}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default Sidebar;

