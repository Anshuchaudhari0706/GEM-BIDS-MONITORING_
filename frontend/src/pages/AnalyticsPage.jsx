import React from 'react';
import { useAuth } from '../context/AuthContext';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { BarChart3, TrendingUp, DollarSign, PieChart as PieIcon } from 'lucide-react';

export default function AnalyticsPage() {
  const categoryData = [
    { name: 'IT Hardware', value: 85 },
    { name: 'Manpower', value: 145 },
    { name: 'Facility Mgmt', value: 98 },
    { name: 'Software Dev', value: 62 },
    { name: 'Solar Energy', value: 240 },
    { name: 'Medical Equip', value: 180 }
  ];

  const statusPieData = [
    { name: 'Published Active Bids', value: 65, color: '#38bdf8' },
    { name: 'Finished / Evaluation', value: 35, color: '#c084fc' }
  ];

  return (
    <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <BarChart3 style={{ width: '28px', height: '28px', color: 'var(--primary-cyan)' }} />
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff' }}>GeM Tender Analytics</h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>Real-time intelligence insights into bid values and categories</p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        {/* Value Distribution Bar Chart */}
        <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <TrendingUp style={{ width: '18px', color: 'var(--primary-cyan)' }} />
            Estimated Bid Value by Category (₹ Lakhs)
          </h3>
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer>
              <BarChart data={categoryData}>
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                <Bar dataKey="value" fill="#3b82f6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Status Pie Chart */}
        <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PieIcon style={{ width: '18px', color: 'var(--primary-purple)' }} />
            Published vs Finished Bids Breakdown
          </h3>
          <div style={{ width: '100%', height: '300px' }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie data={statusPieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                  {statusPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
