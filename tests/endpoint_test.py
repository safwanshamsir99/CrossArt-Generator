from fastapi.testclient import TestClient
from app.endpoint import app
import pytest
from pathlib import Path
import pandas as pd

client = TestClient(app)

API_ROUTER_PREFIX = "crossart"

def get_test_file_path()->Path:
    '''
    Pytest fixture to return path for the test file. 
    '''
    test_file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'
    return test_file_path

def get_test_df_crosstabs()->pd.DataFrame:
    '''
    Extended fixture to read the test file path and 
    return read pandas dataframe
    '''
    test_file = get_test_file_path()
    df_crosstabs = pd.read_csv(test_file)
    return df_crosstabs

df_crosstabs = get_test_df_crosstabs().to_json()

def test_root():
    response = client.get(f"/{API_ROUTER_PREFIX}")
    assert response.status_code == 200, "Response 404, failed"
    assert response.json() == {"status": "ok", "type": "crosstabsgen"}, "No response"

# def test_read_data():
#     '''
#     TODO
#     '''
#     response = client.post(
#         f"/{API_ROUTER_PREFIX}/read", 
#         json={
#             "df": df_crosstabs
#         })
#     assert response.status_code == 200, "Response 404, failed"

# def test_autoselect_demography():
#     '''
#     TODO
#     '''
#     response = client.post(
#         f"/{API_ROUTER_PREFIX}/demography",
#         json={
#             "df": df_crosstabs
#         }
#     )
#     assert response.status_code == 200,"Response 404, failed"
#     assert "demo_list" in response.json()
#     assert isinstance(
#         response["demo_list"], list
#     ), "demo_list is not a list"