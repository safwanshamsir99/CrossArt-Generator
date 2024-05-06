from fastapi.testclient import TestClient
from app.endpoint import app
from pathlib import Path
import pandas as pd
from typing import Dict
import json
from io import StringIO

client = TestClient(app)

# API_ROUTER_PREFIX = "crossart"

survey_file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'
json_file_path = Path.cwd() / 'tests' / 'test_crosstabs.json'

# def csv_to_json(survey_file_path):
#     df = pd.read_csv(survey_file_path)
#     return df.to_json()

# df_json = csv_to_json(survey_file_path) {API_ROUTER_PREFIX}

def test_root():
    response = client.get("/")
    assert response.status_code == 200, "Response 404, failed"
    assert response.json() == {"status": "ok", "type": "crosstabsgen"}, "No response"

# def test_read_data():
#     with survey_file_path.open('rb') as file:
#         response = client.post(
#             f"/{API_ROUTER_PREFIX}/read", 
#             files={
#                 "file": ("test_crosstabs.csv", file, "text/csv")
#             })
#     assert response.status_code == 200, "Response 404, failed"
#     assert "df_reader" in response.json()
#     assert isinstance(
#         response.json()["df_reader"], Dict
#     ), "response.json() is not a dictionary"

# def test_autoselect_demography():
#     response = client.post(
#         f"/{API_ROUTER_PREFIX}/demography",
#         json={"df": json.loads(df_json)}
#         )
#     assert response.status_code == 200,"Response 404, failed"
#     assert "demo_list" in response.json()
#     assert response.json()["demo_list"] == ["Gender","IncomeGroup"], "Expected output is wrong."

# def test_get_search_column():
#     print(pd.DataFrame.from_dict(json.loads(df_json)))
#     response = client.post(
#         f"/{API_ROUTER_PREFIX}/colsearch",
#         json={
#             "df": json.loads(df_json),
#             "key": "LIKERT"
#             }
#     )
#     assert response.status_code == 200, "Response 404, failed"
#     assert "column_with_string" in response.json()
#     assert response.json()["column_with_string"] == ["1. [LIKERT] Opinions"], "Exected output is wrong."

# def test_get_demo_sorter():
#     test_read_data()
#     response = client.post(
#         f"/{API_ROUTER_PREFIX}/demo_sorter",
#         json={"demo": "Gender"} {API_ROUTER_PREFIX}
#     )
#     assert response.status_code == 200, "Response 404, failed"
#     assert "sort_demography" in response.json()
#     assert response.json()["sort_demography"] == ["Male","Female"], "Expected output is wrong."

def test_generate_crosstabs():
    df = pd.read_csv(survey_file_path)
    df_json = df.to_json(orient="records")
    response = client.post(
        "/crosstabs",
        json={
            "df": df_json,
            "demos": ["Gender"],
            "wise": "% of Column Total",
            "q_ls": ["1. [LIKERT] Opinions", "2. What is your dream job field?"],
            "multi": [],
            "name_sort": [],
            "weight": "untrimmed_weight",
            "col_seqs": {"Gender": ["Male", "Female"]}
        }
    )
    assert response.status_code == 200, "Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "crosstabs" in json_data

# def test_read_crosstabs():
#     crosstab_file_path = Path.cwd() / 'tests' / 'test_chartgen.xlsx'
#     with crosstab_file_path.open('rb') as file:
#         response = client.post(
#             f"/{API_ROUTER_PREFIX}/read_crosstabs", 
#             files={
#                 "file": ("test_chartgen.xlsx", file, "text/xlsx")
#             })
#     assert response.status_code == 200, "Response 404, failed"
#     assert response.json() == {"message": "Crosstabs data has been loaded successfully."}

# def test_generate_chart():
#     response = client.post(
#         "/chart",
#         json={
#             "dfs": "",
#             "sheet_names": ""
#         }
#         )
#     assert response.status_code == 200,"Response 404, failed"
#     assert "charts" in response.json()
