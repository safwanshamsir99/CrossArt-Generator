from fastapi import (
    FastAPI, 
    status, 
    APIRouter,
    UploadFile,
    HTTPException
    )
from io import BytesIO
import base64
from typing import List, Dict
from .utils_module.utils import load, demography, col_search, sorter
from .chart_module.chart import load_chart
from .component_module.table import write_table
from .component_module.viz import draw_chart

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
df_crosstabs = {}
@router.post("/read", tags=["Read dataset"])
async def read_data(file: UploadFile = None):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:
        - df: Survey data.

    Return:
        - df: a pandas dataframe
    '''
    read_df = load(df=file.file)
    df_crosstabs["df"] = read_df
    return {"message": "Survey data has been loaded successfully."}

@router.post("/demography", tags=["Auto-select demo"])
async def autoselect_demography():
    '''
    Endpoint to autoselect the demography columns.

    Return:
        - default_demo: list of the column that contains string like 'age', 'gender', 'eth', 'income', 'urban'.
    '''
    df = df_crosstabs.get("df")
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No survey data has been loaded."
        )
    demo_list = demography(df=df)
    return {"demo_list": demo_list}

@router.post("/colsearch", tags=["Column search"])
async def get_search_column(key:str):
    '''
    Endpoint to autoselect column/s with the keyword.

    Request:
        - df: Whole dataframe [pandas dataframe]
        - key: keyword to match [str]

    Return:
        - columns_with_string: list of the column that contains certain keyword.
    '''
    df = df_crosstabs.get("df")
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No survey data has been loaded."
        )
    columns_with_string = col_search(
        df=df,
        key=key
    )
    return {"column with string": columns_with_string}

@router.post("/demo_sorter", tags=["Demography sorter"])
async def get_demo_sorter(demo: str):
    '''
    Endpoint to sort the list of the unique value in the demographic column.

    Request:
        - demo: Column name of the demography you're building the table on [str]

    Return:
        - sorted list of unique values from specific column in the dataframe.
    '''
    df = df_crosstabs.get("df")
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No survey data has been loaded."
        )
    sort_demo = sorter(
        demo=demo,
        df=df
    )
    return {"sort_demography": sort_demo}

@router.post("/crosstabs", tags=["Crosstabs Generator"])
async def generate_crosstabs(
    demos: List[str], 
    wise: str,
    q_ls: List[str],
    multi: List[str], 
    name_sort: List[str], 
    weight: str,
    col_seqs: Dict):
    '''
    Endpoint to generate crosstabs based on the weighted survey file.

    Request:
        - df: pandas DataFrame 
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
        - df_xlsx: conversion result of pandas ExcelWriter that contains crosstabs table into bytes.
    '''
    df = df_crosstabs.get("df")
    if df is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No survey data has been loaded."
        )
    df_xlsx = write_table(
        df=df,
        demos=demos,
        wise=wise,
        q_ls=q_ls,
        multi=multi,
        name_sort=name_sort,
        weight=weight,
        col_seqs=col_seqs
    )
    return {"crosstabs": df_xlsx}


# --------------------------- Chart Generator Endpoint ------------------------------------------
df_charts = {}
sheet_names_list = {}
@router.post("/read_crosstabs", tags=["Read"])
async def read_crosstabs(file: UploadFile = None):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:
        - file: File that contains crosstabs table.
    
    Return:
        - dfs: List of pandas dataframe.
        - sheet_names: List of name of the sheet
    '''
    df_in_memory = BytesIO(file.file.read())
    dfs, sheet_names, _ = load_chart(df_charts=df_in_memory)
    df_charts["dfs"] = dfs
    sheet_names_list["sheet_name"] = sheet_names
    return{
        "message": "Crosstabs data has been loaded successfully."
    }

@router.post("/chart", tags=["Chart Generator"])
async def generate_chart():
    '''
    Endpoint to generate charts based on the crosstabs table.

    Request:
        - dfs: list of pandas DataFrame 
        - sheet_names: list of the sheet names in the crosstabs file. 

    Return:
        - df_charts: crosstabs table that contains clustered column chart in bytes.
    '''
    dfs = df_charts.get("dfs")
    if dfs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No crosstabs data has been loaded."
        )
    sheet_names = sheet_names_list.get("sheet_name")
    if sheet_names is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No crosstabs data has been loaded."
        )
    charts = draw_chart(
        dfs=dfs,
        sheet_names=sheet_names
    )
    encoded_charts = base64.b64encode(charts).decode()
    return {"charts": encoded_charts}

app.include_router(router)