import Card from '../common/Card';

export default function AnomalyAlerts({ anomalies }) {
  return (
    <Card title="Anomaly Alerts" subtitle="Unusual sales/attendance patterns">
      {anomalies.length === 0 ? (
        <p className="muted">No anomalies detected.</p>
      ) : (
        <ul className="alerts">
          {anomalies.map((item, idx) => (
            <li key={`${item.entity_id}-${idx}`} className={`alert ${item.severity}`}>
              <strong>{item.entity_id}</strong>: {item.reason}
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
