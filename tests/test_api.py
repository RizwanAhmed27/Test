from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json()['status'] == 'ok'


def test_chat_commission_lookup_staff():
    payload = {
        'context': {'requester_id': 'staff_anna', 'requester_role': 'staff'},
        'message': 'How much commission did I earn today?'
    }
    res = client.post('/chat', json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body['intent'] == 'commission_lookup'
    assert 'commission' in body['answer'].lower()


def test_analytics_target_gap_requires_staff_id():
    payload = {
        'context': {'requester_id': 'mgr_s1', 'requester_role': 'admin'},
        'metric': 'target_gap',
        'time_range': 'weekly'
    }
    res = client.post('/analytics', json=payload)
    assert res.status_code == 400


def test_summary_staff_cannot_access_other_staff():
    payload = {
        'context': {'requester_id': 'staff_anna', 'requester_role': 'staff'},
        'time_range': 'daily',
        'staff_id': 'staff_liam'
    }
    res = client.post('/summary', json=payload)
    assert res.status_code == 403


def test_manager_cannot_access_other_store():
    payload = {
        'context': {'requester_id': 'mgr_s1', 'requester_role': 'admin'},
        'time_range': 'weekly',
        'store_id': 's2'
    }
    res = client.post('/summary', json=payload)
    assert res.status_code == 403


def test_target_gap_rejects_non_weekly():
    payload = {
        'context': {'requester_id': 'mgr_s1', 'requester_role': 'admin'},
        'metric': 'target_gap',
        'time_range': 'daily',
        'staff_id': 'staff_anna'
    }
    res = client.post('/analytics', json=payload)
    assert res.status_code == 400
