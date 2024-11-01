import React, { useState, useEffect } from 'react';
import './DemoPopup.css';

const DemoPopup = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Show popup after a short delay for better user experience
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="demo-popup-overlay">
      <div className="demo-popup-container">
        <div className="demo-popup-content">
          <div className="demo-popup-header">
            <div className="demo-popup-icon">
              <i className="fas fa-info-circle"></i>
            </div>
            <h3 className="demo-popup-title">Campus Connect Demo</h3>
          </div>
          
          <div className="demo-popup-body">
            <p className="demo-popup-message">
              This is only for demo purposes. If you are willing to contribute, feel free.
            </p>
            
            <div className="demo-popup-features">
              <div className="demo-feature-item">
                <i className="fas fa-exclamation-triangle demo-feature-icon"></i>
                <span>Limited functionality in demo mode</span>
              </div>
              <div className="demo-feature-item">
                <i className="fas fa-users demo-feature-icon"></i>
                <span>Open for community contributions</span>
              </div>
              <div className="demo-feature-item">
                <i className="fas fa-graduation-cap demo-feature-icon"></i>
                <span>Full version available for schools</span>
              </div>
            </div>
          </div>
          
          <div className="demo-popup-footer">
            <button 
              className="demo-popup-button"
              onClick={handleClose}
            >
              <i className="fas fa-check me-2"></i>
              Got it!
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoPopup;