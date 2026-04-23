import Card from '../common/Card';

export default function AdminOverview({ recommendations }) {
  return (
    <Card title="Admin Overview" subtitle="Store-level actions for managers/admins">
      <ul className="list">
        {recommendations.map((r, idx) => (
          <li key={idx}>{r}</li>
        ))}
      </ul>
    </Card>
  );
}
