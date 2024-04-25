from fastapi import FastAPI, status, APIRouter
from app.utils_module.utils import load, demography, col_search, sorter
from app.chart_module.chart import load_chart
from app.component_module.table import write_table
from app.component_module.viz import draw_chart
from app.schema import (
    DataframeSchema,
    ColumnSearchSchema,
    DemoSorterSchema,
    CrosstabSchema,
    ChartSchema
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
async def read_data(dataframe: DataframeSchema):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:
        - df: Whole dataframe [streamlit dataframe]

    Return:
        - df: a pandas dataframe
    '''
    read_df = load(df=dataframe.df)
    return {"df_reader": read_df}

@router.post("/demography", tags=["Auto-select demo"])
async def autoselect_demography(demo: DataframeSchema):
    '''
    Endpoint to autoselect the demography columns.
    '''
    demo_list = demography(df=demo.df)
    return {"demo_list": demo_list}

@router.post("/colsearch", tags=["Column search"])
async def get_search_column(search_column: ColumnSearchSchema):
    '''
    Endpoint to autoselect column/s with the keyword.

    Request:
        - df: Whole dataframe [pandas dataframe]
        - key: keyword to match [str]

    Return:
        - columns_with_string: list of the column that contains certain keyword.
    '''
    columns_with_string = col_search(
        df=search_column.df,
        key=search_column.key
    )
    return {"column with string": columns_with_string}

@router.post("/demo_sorter", tags=["Demography sorter"])
async def get_demo_sorter(demo_sorter:DemoSorterSchema):
    '''
    Endpoint to sort the list of the unique value in the demographic column.

    Request:
        - demo: Column name of the demography you're building the table on [str]
        - df: Whole dataframe [pandas dataframe]

    Return:
        - sorted list of unique values from specific column in the dataframe.
    '''
    sort_demo = sorter(
        demo=demo_sorter.demo,
        df=demo_sorter.df
    )
    return {"sort_demography": sort_demo}

@router.post("/crosstabs", tags=["Crosstabs Generator"])
async def generate_crosstabs(crosstabs: CrosstabSchema):
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
    df_xlsx = write_table(
        df=crosstabs.df,
        demos=crosstabs.demos,
        wise=crosstabs.wise,
        q_ls=crosstabs.q_ls,
        multi=crosstabs.multi,
        name_sort=crosstabs.name_sort,
        weight=crosstabs.weight,
        col_seqs=crosstabs.col_seqs
    )
    return {"crosstabs": df_xlsx}


# --------------------------- Chart Generator Endpoint ------------------------------------------
@router.post("/read_crosstabs", tags=["Read"])
async def read_crosstabs(crosstabreader: DataframeSchema):
    '''
    Endpoint to read and load the streamlit dataframe into pandas dataframe.

    Request:
        - df_charts: Whole dataframe [streamlit dataframe]
    
    Return:
        - dfs: List of pandas dataframe.
        - sheet_names: List of name of the sheet
        - df_chartsname: Name of the uploaded file
    '''
    dfs, sheet_names, df_chartsname = load_chart(df_charts=crosstabreader.df)
    return{
        "df_list": dfs,
        "sheet_names": sheet_names,
        "file_name": df_chartsname
    }

@router.post("/chart", tags=["Chart Generator"])
async def generate_chart(chart: ChartSchema):
    '''
    Endpoint to generate charts based on the crosstabs table.

    Request:
        - dfs: list of pandas DataFrame 
        - sheet_names: listof the sheet names in the crosstabs file. 

    Return:
        - df_charts: crosstabs table that contains clustered column chart in bytes.
    '''
    df_charts = draw_chart(
        dfs=chart.dfs,
        sheet_names=chart.sheet_names
    )
    return {"charts": df_charts}

app.include_router(router)