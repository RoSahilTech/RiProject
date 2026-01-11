import React from 'react';

function Header({ onReportClick, notificationCount }) {
  return (
    <header className="glass-effect shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <i className="fas fa-water text-3xl text-blue-600"></i>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Jal-Drishti Dashboard
              </h1>
              <p className="text-sm text-gray-600">AI-Powered Water-Logging Risk Management System</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative notification-badge">
              <i className="fas fa-bell text-xl text-gray-600 cursor-pointer"></i>
              {notificationCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-2">
                  {notificationCount}
                </span>
              )}
            </div>
            <button 
              onClick={onReportClick}
              className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:shadow-lg transition"
            >
              <i className="fas fa-plus mr-2"></i>Report Issue
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

