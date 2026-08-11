import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

export default function CustomStatusDropdown({ value, onChange }) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef(null);

  const options = [
    { id: 'PUBLISHED', label: 'Published Tenders' },
    { id: 'FINISHED', label: 'Finished Tenders' },
    { id: 'ALL', label: 'All Bids & Tenders' }
  ];

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedOption = options.find(o => o.id === value) || options[1];

  return (
    <div ref={containerRef} style={{ position: 'relative', width: '100%' }}>
      {/* Select Box */}
      <div
        onClick={() => setOpen(!open)}
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: '#0d1527',
          border: '1px solid #1e293b',
          borderRadius: '8px',
          padding: '10px 14px',
          color: '#fff',
          cursor: 'pointer',
          fontSize: '0.92rem',
          fontWeight: 600
        }}
      >
        <span>{selectedOption.label}</span>
        <ChevronDown style={{ width: '18px', height: '18px', color: '#94a3b8' }} />
      </div>

      {/* Screenshot 4: Custom Popup Menu */}
      {open && (
        <div
          style={{
            position: 'absolute',
            top: 'calc(100% + 4px)',
            left: 0,
            right: 0,
            zIndex: 999,
            background: '#151d30',
            border: '1px solid #334155',
            borderRadius: '8px',
            boxShadow: '0 10px 25px rgba(0,0,0,0.7)',
            overflow: 'hidden'
          }}
        >
          {options.map((opt) => {
            const isSelected = opt.id === value;
            return (
              <div
                key={opt.id}
                onClick={() => {
                  onChange(opt.id);
                  setOpen(false);
                }}
                style={{
                  padding: '12px 16px',
                  fontSize: '0.9rem',
                  fontWeight: isSelected ? 700 : 500,
                  background: isSelected ? '#1d4ed8' : 'transparent',
                  color: isSelected ? '#ffffff' : '#e2e8f0',
                  cursor: 'pointer',
                  transition: 'background 0.15s ease'
                }}
              >
                {opt.label}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
