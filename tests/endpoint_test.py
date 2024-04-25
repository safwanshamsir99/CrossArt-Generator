from fastapi.testclient import TestClient
from app.endpoint import app

client = TestClient(app)

def test_root():
    response = client.get("/crossart/")
    assert response.status_code == 200, "Response 404, failed"
    assert response.json() == {"status": "ok", "type": "crosstabsgen"}, "No response"

def test_crosstabs_gen():
    '''
    TODO: TEST ENDPOINT CROSSTABS
    '''
    ...