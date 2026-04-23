import Card from '../common/Card';

export default function StaffPerformance({ recommendations }) {
  return (
    <Card title="My Performance" subtitle="Personal execution plan">
      <ol className="list ordered">
        {recommendations.map((r, idx) => (
          <li key={idx}>{r}</li>
        ))}
      </ol>
    </Card>
  );
}
