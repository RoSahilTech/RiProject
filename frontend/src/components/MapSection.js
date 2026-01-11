import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for Leaflet default icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const WARD_COORDINATES = {
  'Karol Bagh': [28.6514, 77.1907],
  'Connaught Place': [28.6315, 77.2167],
  'Dwarka Sector 21': [28.5822, 77.0500],
  'Rohini Sector 8': [28.7495, 77.0565],
  'Lajpat Nagar': [28.5677, 77.2433],
  'Paharganj': [28.6453, 77.2128],
  'Vasant Kunj': [28.5245, 77.1492],
  'Mayur Vihar Phase 1': [28.6083, 77.2908],
  'Model Town': [28.6892, 77.2124],
  'Okhla Phase 1': [28.5355, 77.2656],
  'Paschim Vihar': [28.6734, 77.1478],
  'Janakpuri': [28.5918, 77.0892],
  'New Delhi': [28.6284, 77.2189],
  'Saket': [28.5576, 77.1789],
  'Shalimar Bagh': [28.7098, 77.1025],
  'Vasant Vihar': [28.4867, 77.1324],
  'Civil Lines': [28.6623, 77.2298],
  'Hauz Khas': [28.5434, 77.2056],
  'Patparganj': [28.5789, 77.2712],
  'Pitampura': [28.6987, 77.1687]
};

function MapSection({ selectedWard, wardData, predictions }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);

  useEffect(() => {
    if (!mapInstanceRef.current && mapRef.current) {
      // Initialize map
      mapInstanceRef.current = L.map(mapRef.current).setView([28.6139, 77.2090], 11);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
      }).addTo(mapInstanceRef.current);

      // Add markers for all wards
      Object.entries(WARD_COORDINATES).forEach(([wardName, coords]) => {
        const riskLevel = wardData[wardName]?.flood_risk_level ?? 0;
        const color = riskLevel === 2 ? '#ef4444' : riskLevel === 1 ? '#f59e0b' : '#10b981';
        
        const icon = L.divIcon({
          html: `<div style="background: ${color}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
          iconSize: [30, 30],
          className: 'custom-div-icon'
        });

        const marker = L.marker(coords, { icon })
          .addTo(mapInstanceRef.current)
          .bindPopup(`
            <div style="padding: 10px; min-width: 200px;">
              <h4 style="font-weight: bold; margin-bottom: 5px;">${wardName}</h4>
              <p style="margin: 5px 0;">Risk: <span style="color: ${color}; font-weight: bold;">
                ${riskLevel === 2 ? 'HIGH' : riskLevel === 1 ? 'MEDIUM' : 'LOW'}
              </span></p>
              ${wardData[wardName]?.max_flood_depth_cm ? 
                `<p style="margin: 5px 0;">Depth: ${wardData[wardName].max_flood_depth_cm.toFixed(1)} cm</p>` : ''}
            </div>
          `);

        markersRef.current.push({ marker, wardName });
      });
    } else if (mapInstanceRef.current) {
      // Update existing markers
      markersRef.current.forEach(({ marker, wardName }) => {
        const riskLevel = wardData[wardName]?.flood_risk_level ?? 0;
        const color = riskLevel === 2 ? '#ef4444' : riskLevel === 1 ? '#f59e0b' : '#10b981';
        
        const icon = L.divIcon({
          html: `<div style="background: ${color}; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></div>`,
          iconSize: [30, 30],
          className: 'custom-div-icon'
        });

        marker.setIcon(icon);
        marker.setPopupContent(`
          <div style="padding: 10px; min-width: 200px;">
            <h4 style="font-weight: bold; margin-bottom: 5px;">${wardName}</h4>
            <p style="margin: 5px 0;">Risk: <span style="color: ${color}; font-weight: bold;">
              ${riskLevel === 2 ? 'HIGH' : riskLevel === 1 ? 'MEDIUM' : 'LOW'}
            </span></p>
            ${wardData[wardName]?.max_flood_depth_cm ? 
              `<p style="margin: 5px 0;">Depth: ${wardData[wardName].max_flood_depth_cm.toFixed(1)} cm</p>` : ''}
          </div>
        `);
      });

      // Center on selected ward
      if (selectedWard && WARD_COORDINATES[selectedWard]) {
        mapInstanceRef.current.setView(WARD_COORDINATES[selectedWard], 13, { animate: true });
      }
    }

    return () => {
      // Cleanup on unmount
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
        markersRef.current = [];
      }
    };
  }, [selectedWard, wardData]);

  return (
    <div className="glass-effect rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800">Ward-Wise Risk Map</h2>
        <div className="flex space-x-2">
          <button 
            onClick={() => {
              if (mapInstanceRef.current) {
                mapInstanceRef.current.setView([28.6139, 77.2090], 11);
              }
            }}
            className="px-3 py-1 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition"
          >
            <i className="fas fa-sync-alt mr-1"></i>Refresh
          </button>
        </div>
      </div>
      <div id="map" ref={mapRef} style={{ height: '500px', width: '100%' }}></div>
      <div className="mt-4 flex items-center justify-center space-x-6">
        <div className="flex items-center">
          <span className="status-indicator bg-red-500 mr-2"></span>
          <span className="text-sm text-gray-600">High Risk</span>
        </div>
        <div className="flex items-center">
          <span className="status-indicator bg-yellow-500 mr-2"></span>
          <span className="text-sm text-gray-600">Medium Risk</span>
        </div>
        <div className="flex items-center">
          <span className="status-indicator bg-green-500 mr-2"></span>
          <span className="text-sm text-gray-600">Low Risk</span>
        </div>
      </div>
    </div>
  );
}

export default MapSection;

