import { useCallback, useEffect, useMemo, useState } from 'react';
import { SeyallaApi } from '../api/client';

const defaultUsers = {
  admin: { requester_id: 'admin_root', requester_role: 'admin', store_id: 's1' },
  staff: { requester_id: 'staff_anna', requester_role: 'staff', store_id: 's1' },
};

export function useSeyallaData(role) {
  const context = useMemo(() => defaultUsers[role], [role]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [summary, setSummary] = useState(null);
  const [salesKpi, setSalesKpi] = useState(null);
  const [commissionKpi, setCommissionKpi] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const [summaryRes, salesRes, commissionRes, anomaliesRes, recRes] = await Promise.all([
        SeyallaApi.summary({ context, time_range: 'daily', staff_id: role === 'staff' ? context.requester_id : null, store_id: role === 'admin' ? context.store_id : null }),
        SeyallaApi.analytics({ context, metric: 'sales', time_range: 'weekly', store_id: context.store_id }),
        SeyallaApi.analytics({ context, metric: 'commission', time_range: 'weekly', staff_id: role === 'staff' ? context.requester_id : null, store_id: role === 'admin' ? context.store_id : null }),
        SeyallaApi.anomalies({ context, store_id: context.store_id }),
        SeyallaApi.recommendations({ context, goal: role === 'admin' ? 'recover_store_target' : 'increase_commission', staff_id: role === 'staff' ? context.requester_id : null, store_id: context.store_id }),
      ]);

      setSummary(summaryRes);
      setSalesKpi(salesRes);
      setCommissionKpi(commissionRes);
      setAnomalies(anomaliesRes.items || []);
      setRecommendations(recRes.recommendations || []);
    } catch (e) {
      setError(e.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  }, [context, role]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const askChat = useCallback(
    (message) => SeyallaApi.chat({ context, message }),
    [context],
  );

  return {
    context,
    loading,
    error,
    summary,
    salesKpi,
    commissionKpi,
    anomalies,
    recommendations,
    askChat,
    refresh: loadDashboard,
  };
}
