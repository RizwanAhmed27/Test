import { useState } from 'react';
import AppShell from './components/layout/AppShell';
import ChatPanel from './components/chat/ChatPanel';
import SummaryCards from './components/dashboard/SummaryCards';
import KPIWidgets from './components/dashboard/KPIWidgets';
import AnomalyAlerts from './components/dashboard/AnomalyAlerts';
import AdminOverview from './components/dashboard/AdminOverview';
import StaffPerformance from './components/dashboard/StaffPerformance';
import { useSeyallaData } from './hooks/useSeyallaData';

export default function App() {
  const [role, setRole] = useState('admin');
  const data = useSeyallaData(role);

  return (
    <AppShell role={role} onRoleChange={setRole}>
      {data.error && <div className="error-banner">{data.error}</div>}
      {data.loading && <div className="loading">Loading data…</div>}

      <div className="layout-grid">
        <section className="main-column">
          <SummaryCards summary={data.summary} />
          <KPIWidgets salesKpi={data.salesKpi} commissionKpi={data.commissionKpi} />
          <AnomalyAlerts anomalies={data.anomalies} />
          {role === 'admin' ? (
            <AdminOverview recommendations={data.recommendations} />
          ) : (
            <StaffPerformance recommendations={data.recommendations} />
          )}
        </section>

        <aside className="side-column">
          <ChatPanel onAsk={data.askChat} />
        </aside>
      </div>
    </AppShell>
  );
}
