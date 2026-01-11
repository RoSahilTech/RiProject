import React from 'react';

const WARDS = [
  'Abul Fazal Enclave', 'Anand Vihar', 'Ashok Vihar', 'Azadpur',
  'Badli', 'Bawana', 'Bindapur', 'Burari', 'Chandni Chowk',
  'Chhawla', 'Civil Lines', 'Connaught Place', 'Dabri', 'Daryaganj',
  'Dashrath Puri', 'Defence Colony', 'Dilshad Garden', 'Dwarka Sector 10',
  'Dwarka Sector 14', 'Dwarka Sector 21', 'Dwarka Sector 22', 'Dwarka Sector 6',
  'Gandhi Nagar', 'Geeta Colony', 'Govindpuri', 'Greater Kailash Part 1',
  'Green Park', 'Hauz Khas', 'Jama Masjid', 'Janakpuri', 'Jangpura',
  'Jasola', 'Jasola Vihar', 'Kalindi Kunj', 'Kalkaji', 'Kamla Nagar',
  'Kapashera', 'Karkardooma', 'Karol Bagh', 'Kashmere Gate', 'Kingsway Camp',
  'Kirti Nagar', 'Krishna Nagar', 'Lajpat Nagar', 'Laxmi Nagar',
  'Lodhi Colony', 'Mahavir Enclave', 'Mahipalpur', 'Malviya Nagar',
  'Mayur Vihar Phase 1', 'Mehrauli', 'Model Town', 'Moti Nagar',
  'Munirka', 'Najafgarh', 'Nangloi', 'Narela', 'Nehru Place',
  'New Friends Colony', 'Nirman Vihar', 'Okhla Phase 1', 'Old Delhi',
  'Paharganj', 'Palam', 'Paschim Vihar', 'Patel Nagar', 'Patparganj',
  'Pehladpur', 'Pitampura', 'Preet Vihar', 'Rajendra Place',
  'Rajouri Garden', 'Rithala', 'Rohini Sector 15', 'Rohini Sector 16',
  'Rohini Sector 22', 'Rohini Sector 24', 'Rohini Sector 3',
  'Rohini Sector 5', 'Rohini Sector 8', 'Sadar Bazaar',
  'Safdarjung Enclave', 'Saket', 'Sarita Vihar', 'Seelampur',
  'Shahdara', 'Shaheen Bagh', 'Shalimar Bagh', 'Sultanpur',
  'Tagore Garden', 'Timarpur', 'Tis Hazari', 'Tuglakabad',
  'Uttam Nagar', 'Vasant Kunj', 'Vasant Vihar', 'Vikaspuri',
  'Vivek Vihar', 'Wazirabad', 'Yamuna Vihar'
];

function ControlPanel({ selectedWard, setSelectedWard, demoMode, setDemoMode, controls, setControls, onPredict }) {
  return (
    <div className="glass-effect rounded-xl p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800">
          <i className="fas fa-sliders-h mr-2 text-purple-500"></i>
          Prediction Controls
        </h2>
        <div className="flex items-center space-x-4">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={demoMode}
              onChange={(e) => setDemoMode(e.target.checked)}
              className="mr-2 w-5 h-5"
            />
            <span className="font-semibold text-gray-700">
              <i className="fas fa-play-circle mr-1"></i>Demo Mode (Live Simulation)
            </span>
          </label>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Ward Selection
          </label>
          <select
            value={selectedWard}
            onChange={(e) => setSelectedWard(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            disabled={demoMode}
          >
            {WARDS.map(ward => (
              <option key={ward} value={ward}>{ward}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Rain (1h): {controls.rain1h.toFixed(1)} mm
          </label>
          <input
            type="range"
            min="0"
            max="50"
            step="0.1"
            value={controls.rain1h}
            onChange={(e) => setControls({...controls, rain1h: parseFloat(e.target.value)})}
            className="w-full"
            disabled={demoMode}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Rain (3h): {controls.rain3h.toFixed(1)} mm
          </label>
          <input
            type="range"
            min="0"
            max="150"
            step="0.1"
            value={controls.rain3h}
            onChange={(e) => setControls({...controls, rain3h: parseFloat(e.target.value)})}
            className="w-full"
            disabled={demoMode}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Rain (24h): {controls.rain24h.toFixed(1)} mm
          </label>
          <input
            type="range"
            min="0"
            max="200"
            step="0.1"
            value={controls.rain24h}
            onChange={(e) => setControls({...controls, rain24h: parseFloat(e.target.value)})}
            className="w-full"
            disabled={demoMode}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Forecast (3h): {controls.rainForecast3h.toFixed(1)} mm
          </label>
          <input
            type="range"
            min="0"
            max="100"
            step="0.1"
            value={controls.rainForecast3h}
            onChange={(e) => setControls({...controls, rainForecast3h: parseFloat(e.target.value)})}
            className="w-full"
            disabled={demoMode}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Yamuna Level: {controls.yamunaLevel.toFixed(1)} m
          </label>
          <input
            type="range"
            min="202"
            max="206"
            step="0.1"
            value={controls.yamunaLevel}
            onChange={(e) => setControls({...controls, yamunaLevel: parseFloat(e.target.value)})}
            className="w-full"
            disabled={demoMode}
          />
        </div>
      </div>

      <button
        onClick={onPredict}
        disabled={demoMode}
        className={`w-full md:w-auto px-6 py-3 rounded-lg font-semibold transition ${
          demoMode 
            ? 'bg-gray-400 text-gray-600 cursor-not-allowed' 
            : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:shadow-lg'
        }`}
      >
        <i className="fas fa-brain mr-2"></i>
        {demoMode ? 'Auto-Predicting in Demo Mode...' : 'Run AI Prediction'}
      </button>
    </div>
  );
}

export default ControlPanel;

