import React, { useState, useRef, useEffect } from 'react';
import { Calendar as CalendarIcon, ChevronUp, ChevronDown } from 'lucide-react';

export default function CustomDatePicker({ value, onChange, onClear }) {
  const [open, setOpen] = useState(false);
  const containerRef = useRef(null);

  // Default to August 2026 or parse passed date
  const parsedDate = value ? new Date(value) : new Date(2026, 7, 10);
  const [currentYear, setCurrentYear] = useState(parsedDate.getFullYear() || 2026);
  const [currentMonth, setCurrentMonth] = useState(parsedDate.getMonth() || 7);

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const daysInMonth = (month, year) => new Date(year, month + 1, 0).getDate();
  const firstDayOfWeek = (month, year) => {
    let day = new Date(year, month, 1).getDay();
    return day === 0 ? 6 : day - 1; // Adjust for Monday start (Mo, Tu, We, Th, Fr, Sa, Su)
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear(prev => prev - 1);
    } else {
      setCurrentMonth(prev => prev - 1);
    }
  };

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear(prev => prev + 1);
    } else {
      setCurrentMonth(prev => prev + 1);
    }
  };

  const handleSelectDay = (day) => {
    const monthStr = String(currentMonth + 1).padStart(2, '0');
    const dayStr = String(day).padStart(2, '0');
    const dateFormatted = `${currentYear}-${monthStr}-${dayStr}`;
    onChange(dateFormatted);
    setOpen(false);
  };

  const handleToday = () => {
    const today = new Date();
    const monthStr = String(today.getMonth() + 1).padStart(2, '0');
    const dayStr = String(today.getDate()).padStart(2, '0');
    const dateFormatted = `${today.getFullYear()}-${monthStr}-${dayStr}`;
    setCurrentYear(today.getFullYear());
    setCurrentMonth(today.getMonth());
    onChange(dateFormatted);
    setOpen(false);
  };

  const handleClearClick = () => {
    onClear();
    setOpen(false);
  };

  // Format date display (DD/MM/YYYY)
  const displayFormatted = value
    ? `${String(parsedDate.getDate()).padStart(2, '0')}/${String(parsedDate.getMonth() + 1).padStart(2, '0')}/${parsedDate.getFullYear()}`
    : '10/08/2026';

  const totalDays = daysInMonth(currentMonth, currentYear);
  const startingDay = firstDayOfWeek(currentMonth, currentYear);

  // Previous month trailing days
  const prevMonthTotalDays = daysInMonth(currentMonth === 0 ? 11 : currentMonth - 1, currentMonth === 0 ? currentYear - 1 : currentYear);
  const prevMonthDays = [];
  for (let i = startingDay - 1; i >= 0; i--) {
    prevMonthDays.push(prevMonthTotalDays - i);
  }

  // Days grid
  const daysArray = Array.from({ length: totalDays }, (_, i) => i + 1);
  
  // Next month leading days to complete grid
  const totalCells = prevMonthDays.length + daysArray.length;
  const nextMonthDaysCount = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
  const nextMonthDays = Array.from({ length: nextMonthDaysCount }, (_, i) => i + 1);

  const selectedDay = (parsedDate.getFullYear() === currentYear && parsedDate.getMonth() === currentMonth)
    ? parsedDate.getDate()
    : null;

  return (
    <div ref={containerRef} style={{ position: 'relative', width: '100%' }}>
      {/* Date Input Button */}
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
          fontFamily: 'monospace',
          fontSize: '0.95rem',
          fontWeight: 600
        }}
      >
        <span>{displayFormatted}</span>
        <CalendarIcon style={{ width: '16px', height: '16px', color: 'var(--text-muted)' }} />
      </div>

      {/* Screenshot 3: Custom Popup Calendar Modal */}
      {open && (
        <div
          style={{
            position: 'absolute',
            top: 'calc(100% + 6px)',
            left: 0,
            zIndex: 999,
            width: '260px',
            background: '#ffffff',
            borderRadius: '8px',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.5)',
            padding: '14px',
            color: '#1e293b',
            fontFamily: 'sans-serif'
          }}
        >
          {/* Calendar Month & Year Header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
            <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a', display: 'flex', alignItems: 'center', gap: '4px' }}>
              {monthNames[currentMonth]} {currentYear}
              <ChevronDown style={{ width: '16px', height: '16px' }} />
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <button
                type="button"
                onClick={handlePrevMonth}
                style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '2px', color: '#334155' }}
              >
                <ChevronUp style={{ width: '18px', height: '18px' }} />
              </button>
              <button
                type="button"
                onClick={handleNextMonth}
                style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '2px', color: '#334155' }}
              >
                <ChevronDown style={{ width: '18px', height: '18px' }} />
              </button>
            </div>
          </div>

          {/* Weekday Labels (Mo Tu We Th Fr Sa Su) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', textAlign: 'center', fontSize: '0.82rem', fontWeight: 600, color: '#e11d48', marginBottom: '8px' }}>
            <div>Mo</div>
            <div>Tu</div>
            <div>We</div>
            <div>Th</div>
            <div>Fr</div>
            <div>Sa</div>
            <div>Su</div>
          </div>

          {/* Days Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '2px', textAlign: 'center', fontSize: '0.85rem' }}>
            {prevMonthDays.map((d, idx) => (
              <div key={`prev-${idx}`} style={{ padding: '6px 0', color: '#94a3b8' }}>
                {d}
              </div>
            ))}

            {daysArray.map((day) => {
              const isSelected = selectedDay === day;
              return (
                <div
                  key={day}
                  onClick={() => handleSelectDay(day)}
                  style={{
                    padding: '6px 0',
                    cursor: 'pointer',
                    borderRadius: '4px',
                    fontWeight: isSelected ? 700 : 500,
                    background: isSelected ? '#0070f3' : 'transparent',
                    color: isSelected ? '#ffffff' : '#0f172a',
                    border: isSelected ? '2px solid #000' : 'none'
                  }}
                >
                  {day}
                </div>
              );
            })}

            {nextMonthDays.map((d, idx) => (
              <div key={`next-${idx}`} style={{ padding: '6px 0', color: '#94a3b8' }}>
                {d}
              </div>
            ))}
          </div>

          {/* Bottom Action Links (Clear / Today) */}
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px', paddingTop: '8px', borderTop: '1px solid #f1f5f9', fontSize: '0.85rem', fontWeight: 600 }}>
            <span onClick={handleClearClick} style={{ color: '#0070f3', cursor: 'pointer' }}>Clear</span>
            <span onClick={handleToday} style={{ color: '#0070f3', cursor: 'pointer' }}>Today</span>
          </div>
        </div>
      )}
    </div>
  );
}
