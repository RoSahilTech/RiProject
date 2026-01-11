import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Header from './components/Header';
import StatsCards from './components/StatsCards';
import MapSection from './components/MapSection';
import Sidebar from './components/Sidebar';
import PredictionsChart from './components/PredictionsChart';
import ControlPanel from './components/ControlPanel';
import ReportModal from './components/ReportModal';
import './App.css';

// Use relative path for proxy, or direct URL if proxy fails
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [selectedWard, setSelectedWard] = useState('Karol Bagh');
  const [demoMode, setDemoMode] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [wardData, setWardData] = useState({});
  const [stats, setStats] = useState({
    totalWards: 30,
    highRisk: 8,
    mediumRisk: 10,
    lowRisk: 12
  });
  const [controls, setControls] = useState({
    rain1h: 15.5,
    rain3h: 42.3,
    rain24h: 85.2,
    rainForecast3h: 38.5,
    yamunaLevel: 203.5
  });
  const [liveUpdates, setLiveUpdates] = useState([]);
  const [showReportModal, setShowReportModal] = useState(false);
  const [citizenReports, setCitizenReports] = useState([]);
  const intervalRef = useRef(null);

  const updateDashboardData = (data) => {
    if (data.ward_data) {
      setWardData(data.ward_data);
    }
    if (data.stats) {
      setStats(data.stats);
    }
    if (data.predictions) {
      setPredictions(data.predictions);
    }
    if (data.live_updates) {
      setLiveUpdates(data.live_updates);
    }
  };

  const setFallbackData = () => {
    // Generate fallback data for multiple wards
    const fallbackWards = ['Karol Bagh', 'Paharganj', 'Lajpat Nagar', 'Dwarka Sector 21', 
                          'Connaught Place', 'Rohini Sector 8', 'Vasant Kunj'];
    const fallbackWardData = {};
    
    fallbackWards.forEach((ward, index) => {
      const riskLevel = index % 3; // Cycle through risk levels
      fallbackWardData[ward] = {
        flood_risk_level: riskLevel,
        risk_label: ['Safe', 'Warning', 'Danger'][riskLevel],
        max_flood_depth_cm: riskLevel === 2 ? 45.2 : riskLevel === 1 ? 25.5 : 5.2,
        drain_capacity_score: 0.65 + (riskLevel * 0.1),
        citizen_reports_count: riskLevel === 2 ? 12 : riskLevel === 1 ? 5 : 1
      };
    });
    
    setWardData(fallbackWardData);
    setStats({
      totalWards: 100,
      highRisk: Math.floor(fallbackWards.length / 3),
      mediumRisk: Math.floor(fallbackWards.length / 3),
      lowRisk: Math.ceil(fallbackWards.length / 3)
    });
  };

  const fetchInitialData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/demo`, { timeout: 3000 });
      if (response.data) {
        updateDashboardData(response.data);
      }
    } catch (error) {
      console.warn('Backend not available, using fallback data:', error.message);
      setFallbackData();
    }
  };

  const fetchDemoData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/demo`, { timeout: 3000 });
      if (response.data) {
        updateDashboardData(response.data);
      }
    } catch (error) {
      // Silently fail in demo mode - will use cached/fallback data
      console.warn('Demo data fetch failed (backend may be offline)');
    }
  };

  useEffect(() => {
    fetchInitialData();
    
    // Set up demo mode polling
    if (demoMode) {
      intervalRef.current = setInterval(() => {
        fetchDemoData();
      }, 3000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [demoMode]);

  const handlePredict = async () => {
    try {
      const response = await axios.post(`${API_BASE}/predict`, {
        ward_name: selectedWard,
        rain_1h_mm: controls.rain1h,
        rain_3h_mm: controls.rain3h,
        rain_24h_mm: controls.rain24h,
        rain_forecast_3h_mm: controls.rainForecast3h,
        yamuna_level_m: controls.yamunaLevel
      }, { timeout: 5000 });
      
      if (response.data) {
        setPredictions(response.data);
        setWardData(prev => ({
          ...prev,
          [selectedWard]: response.data
        }));
      }
    } catch (error) {
      console.warn('Backend prediction unavailable, using fallback logic:', error.message);
      // Fallback prediction using simple rule-based logic
      const riskLevel = controls.rain24h > 80 || controls.yamunaLevel > 204 ? 2 : 
                       controls.rain24h > 50 ? 1 : 0;
      const prediction = {
        flood_risk_level: riskLevel,
        risk_label: ['Safe', 'Warning', 'Danger'][riskLevel],
        max_flood_depth_cm: Math.min(controls.rain24h * 0.6, 100),
        drain_capacity_score: 0.7,
        confidence: 0.75,
        citizen_reports_count: riskLevel > 0 ? Math.floor(controls.rain24h / 10) : 0
      };
      setPredictions(prediction);
      setWardData(prev => ({
        ...prev,
        [selectedWard]: prediction
      }));
      // Show notification that fallback was used
      if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
        console.info('💡 Tip: Start the backend server with: cd backend && python app.py');
      }
    }
  };

  const handleReportSubmit = (reportData) => {
    setCitizenReports(prev => [reportData, ...prev].slice(0, 10));
    setShowReportModal(false);
    // In real system, this would send to backend
    console.log('Report submitted:', reportData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onReportClick={() => setShowReportModal(true)}
        notificationCount={liveUpdates.filter(u => u.type === 'alert').length}
      />
      
      <div className="container mx-auto px-4 py-6">
        <StatsCards stats={stats} />
        
        <ControlPanel
          selectedWard={selectedWard}
          setSelectedWard={setSelectedWard}
          demoMode={demoMode}
          setDemoMode={setDemoMode}
          controls={controls}
          setControls={setControls}
          onPredict={handlePredict}
        />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2">
            <MapSection 
              selectedWard={selectedWard}
              wardData={wardData}
              predictions={predictions}
            />
            
            <PredictionsChart predictions={predictions} />
          </div>

          <Sidebar
            liveUpdates={liveUpdates}
            citizenReports={citizenReports}
            wardData={wardData}
            selectedWard={selectedWard}
            onWardClick={setSelectedWard}
            onReportClick={() => setShowReportModal(true)}
          />
        </div>
      </div>

      {showReportModal && (
        <ReportModal
          onClose={() => setShowReportModal(false)}
          onSubmit={handleReportSubmit}
        />
      )}
    </div>
  );
}

export default App;

