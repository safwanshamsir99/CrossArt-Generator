from fastapi.testclient import TestClient
from app.endpoint import app
from pathlib import Path
import pandas as pd
import json

client = TestClient(app)

API_ROUTER_PREFIX = "crossart"

survey_file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'
crosstab_file_path = Path.cwd() / 'tests' / 'test_chartgen.xlsx'

def test_root():
    response = client.get(f"/{API_ROUTER_PREFIX}")
    assert response.status_code == 200, "Response 404, failed"
    assert response.json() == {"status": "ok", "type": "crosstabsgen"}, "No response"

# --------------------------- Crosstab Generator Endpoint ------------------------------------------
def test_read_data():
    with open(survey_file_path, 'rb') as f:
        response = client.post(
            f"/{API_ROUTER_PREFIX}/read", 
            files={
                "file": f
            })
    assert response.status_code == 200, "Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "df_reader" in json_data
    df = pd.DataFrame(json_data["df_reader"])
    return df

def test_autoselect_demography():
    df = test_read_data()
    df_json = df.to_json(orient="records")
    response = client.post(
        f"/{API_ROUTER_PREFIX}/demography",
        json={
            "df": df_json
        }
    )
    assert response.status_code == 200,"Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "demo_list" in json_data
    assert json_data["demo_list"] == ["Gender","IncomeGroup"], "Expected output is wrong."

def test_get_search_column():
    df = test_read_data()
    df_json = df.to_json(orient="records")
    response = client.post(
        f"/{API_ROUTER_PREFIX}/colsearch",
        json={
            "df": df_json,
            "key": "LIKERT"
            }
    )
    assert response.status_code == 200, "Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "column_with_string" in json_data
    assert json_data["column_with_string"] == ["1. [LIKERT] Opinions"], "Expected output is wrong."

def test_get_demo_sorter():
    df = test_read_data()
    df_json = df.to_json(orient="records")
    response = client.post(
        f"/{API_ROUTER_PREFIX}/demo_sorter",
        json={
            "demo": "Gender",
            "df": df_json
            }
    )
    assert response.status_code == 200, "Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "sort_demography" in json_data
    assert json_data["sort_demography"] == ["Male","Female"], "Expected output is wrong."

def test_generate_crosstabs():
    df = test_read_data()
    df_json = df.to_json(orient="records")
    response = client.post(
        f"/{API_ROUTER_PREFIX}/crosstabs",
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

# --------------------------- Chart Generator Endpoint ------------------------------------------
def test_read_crosstabs():
    with open(crosstab_file_path, "rb") as f:
        response = client.post(
            f"/{API_ROUTER_PREFIX}/read_crosstabs", 
            files={
                "file": f
            }
        )
    assert response.status_code == 200, "Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "df_list" in json_data
    assert "sheet_names" in json_data
    dfs = [pd.read_json(df) for df in json_data["df_list"]]
    sheet_names = json_data["sheet_names"]
    return dfs, sheet_names

def test_generate_chart():
    dfs, sheet_names = test_read_crosstabs()
    dfs_json = [df.to_json(orient="records") for df in dfs]
    response = client.post(
        f"/{API_ROUTER_PREFIX}/chart",
        json={
            "dfs": dfs_json,
            "sheet_names": sheet_names
        })
    assert response.status_code == 200,"Response 404, failed"
    json_data = json.loads(json.dumps(response.json()))
    assert "charts" in json_data
