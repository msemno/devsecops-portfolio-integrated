from fastapi.testclient import TestClient

from service.main import app

client = TestClient(app)

def test_health():
    r=client.get('/healthz'); assert r.status_code == 200 and r.json() == {'status':'ok'}

def test_basic_security_headers():
    r=client.get('/healthz')
    assert r.headers['x-content-type-options']=='nosniff'
    assert r.headers['cache-control']=='no-store'
    assert r.headers['x-frame-options']=='DENY'

def test_build_metadata_omits_secrets(monkeypatch):
    monkeypatch.setenv('APP_REVISION','test-revision')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY','FAKE_DO_NOT_USE')
    r=client.get('/v1/build')
    assert r.json()['revision']=='test-revision'
    assert 'FAKE_DO_NOT_USE' not in r.text

def test_unexposed_docs():
    assert client.get('/docs').status_code==404
