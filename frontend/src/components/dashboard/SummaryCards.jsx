import Card from '../common/Card';

export default function SummaryCards({ summary }) {
  if (!summary) return null;

  const metrics = summary.metrics || {};
  const items = [
    { label: 'Sales', value: metrics.sales_total ?? 0 },
    { label: 'Commission', value: metrics.commission_total ?? 0 },
    { label: 'Range', value: metrics.time_range || '-' },
  ];

  return (
    <div className="grid cards-3">
      {items.map((item) => (
        <Card key={item.label} title={item.label}>
          <p className="metric">{typeof item.value === 'number' ? item.value.toFixed(2) : item.value}</p>
        </Card>
      ))}
      <Card title="Narrative" className="span-3">
        <p>{summary.narrative}</p>
      </Card>
    </div>
  );
}
