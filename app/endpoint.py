from fastapi import (
    FastAPI, 
    status, 
    APIRouter,
    UploadFile,
    File
    )
from io import StringIO
import base64
from fastapi.encoders import jsonable_encoder
import os
import shutil
import pandas as pd
from .utils_module.utils import load, demography, col_search, sorter
from .chart_module.chart import load_chart
from .component_module.table import write_table
from .component_module.viz import draw_chart
from .schema import (
    CrosstabSchema, 
    ChartSchema, 
    DataframeSchema,
    ColumnSearchSchema,
    DemoSorterSchema
    )

description = """
This is a crosstabs generator API from crosstabs-generator-v3.
"""

app = FastAPI(
    title="crosstabs generator",
    description=description,
    license_info={
        "name": "MIT",
        "identifier": "MIT"
    }
)

router = APIRouter(prefix="/crossart")

@router.get("/", status_code=status.HTTP_200_OK, tags=["test"])
def root():
    return {"status": "ok",
            "type": "crosstabsgen"}

# --------------------------- Crosstab Generator Endpoint ------------------------------------------
@router.post("/read", tags=["Read dataset"])
async def read_data(file: UploadFile = File(...)):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:

        - file: Filepath or buffer(Streamlit dataframe/SpooledTemporaryFile)

    Return:

        - df: a pandas dataframe
    '''
    os.makedirs('temp', exist_ok=True)
    path =  f"temp/{file.filename}"
    with open(path, 'w+b') as f:
        shutil.copyfileobj(file.file, f)
    read_df = load(df=path)
    data = {
        "df_reader": jsonable_encoder(
            read_df,
            custom_encoder={
                bytes: lambda value: base64.b64encode(value).decode("utf-8")
            }
        )
    }
    os.remove(path)
    shutil.rmtree('temp')
    return data

@router.post("/demography", tags=["Auto-select demo"])
async def autoselect_demography(demo: DataframeSchema):
    '''
    Endpoint to autoselect the demography columns.

    Request:

        - df: Whole dataframe in JSON string format.

    Return:

        - default_demo: list of the column that contains string like 'age', 'gender', 'eth', 'income', 'urban'.
    '''
    df_json = pd.read_json(StringIO(demo.df), orient="records")
    demo_list = demography(df=df_json)
    data = {
        "demo_list": demo_list
        }
    return data

@router.post("/colsearch", tags=["Column search"])
async def get_search_column(search_col: ColumnSearchSchema):
    '''
    Endpoint to autoselect column/s with the keyword.

    Request:

        - df: Whole dataframe in JSON string format.
        - key: keyword to match [str]

    Return:

        - columns_with_string: list of the column that contains certain keyword.
    '''
    df_json = pd.read_json(StringIO(search_col.df), orient="records")
    columns_with_string = col_search(
        df=df_json,
        key=search_col.key
    )
    data = {
        "column_with_string": columns_with_string
        }
    return data

@router.post("/demo_sorter", tags=["Demography sorter"])
async def get_demo_sorter(demo_sorter: DemoSorterSchema):
    '''
    Endpoint to sort the list of the unique value in the demographic column.

    Request:

        - demo: Column name of the demography you're building the table on [str]
        - df: Whole dataframe in JSON string format.

    Return:

        - sorted list of unique values from specific column in the dataframe.
    '''
    df_json = pd.read_json(StringIO(demo_sorter.df), orient="records")
    sort_demo = sorter(
        demo=demo_sorter.demo,
        df=df_json
    )
    data = {
        "sort_demography": sort_demo
    }
    return data

@router.post("/crosstabs", tags=["Crosstabs Generator"])
async def generate_crosstabs(crosstabs: CrosstabSchema):
    '''
    Endpoint to generate crosstabs based on the weighted survey file.

    Request:

        - df: Whole dataframe in JSON string format.
        - demos: List of name of the selected demography columns. 
        - wise: User selection of the value options. 
        - q_ls: List of question column. 
        - multi: List of column that contains multiple answer option.
        - name_sort: List of column to sort by the name. 
        - weight: Name of the selected weight column [str]
        - col_seqs:
            - Key: Demography column
            - Value: Sorted unique value of the key demography column.
    
    Return:
    
        - data: df_xlsx in encoded bytes.
    '''
    df_json = pd.read_json(StringIO(crosstabs.df), orient="records")
    df_xlsx = write_table(
        df=df_json,
        demos=crosstabs.demos,
        wise=crosstabs.wise,
        q_ls=crosstabs.q_ls,
        multi=crosstabs.multi,
        name_sort=crosstabs.name_sort,
        weight=crosstabs.weight,
        col_seqs=crosstabs.col_seqs
    )
    data = {
        "crosstabs": jsonable_encoder(
            df_xlsx,
            custom_encoder={
                bytes: lambda value: base64.b64encode(value).decode("utf-8")
            }
        )
    }
    return data

# --------------------------- Chart Generator Endpoint ------------------------------------------
@router.post("/read_crosstabs", tags=["Read"])
async def read_crosstabs(file: UploadFile = File(...)):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:

        - df_charts: Filepath or buffer(Streamlit dataframe/SpooledTemporaryFile)
    
    Return:

        - dfs: List of pandas dataframe.
        - sheet_names: List of name of the sheet 
    '''
    os.makedirs('temp', exist_ok=True)
    path =  f"temp/{file.filename}"
    with open(path, 'w+b') as f:
        shutil.copyfileobj(file.file, f)
    dfs, sheet_names, _ = load_chart(df_charts=path)
    data = {
        "df_list": [df.to_json(orient="records") for df in dfs],
        "sheet_names": sheet_names,
    }
    os.remove(path)
    shutil.rmtree('temp')
    return data

@router.post("/chart", tags=["Chart Generator"])
async def generate_chart(chart: ChartSchema):
    '''
    Endpoint to generate charts based on the crosstabs table.

    Request:

        - dfs: list of pandas DataFrame in JSON string format -> List[str]
        - sheet_names: list of the sheet names in the crosstabs file. 

    Return:

        - data: charts in encoded bytes.
    '''
    dfs = [pd.read_json(StringIO(df), orient='records') for df in chart.dfs]
    charts = draw_chart(
        dfs=dfs,
        sheet_names=chart.sheet_names
    )
    data = {
        "charts": jsonable_encoder(
            charts,
            custom_encoder={
                bytes: lambda value: base64.b64encode(value).decode("utf-8")
            }
        )
    }
    return data

app.include_router(router)