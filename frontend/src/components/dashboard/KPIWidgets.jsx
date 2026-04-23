import Card from '../common/Card';

export default function KPIWidgets({ salesKpi, commissionKpi }) {
  return (
    <div className="grid cards-2">
      <Card title="Weekly Sales KPI">
        <p className="metric">{(salesKpi?.values?.sales_total ?? 0).toFixed(2)}</p>
      </Card>
      <Card title="Weekly Commission KPI">
        <p className="metric">{(commissionKpi?.values?.commission_total ?? 0).toFixed(2)}</p>
      </Card>
    </div>
  );
}
