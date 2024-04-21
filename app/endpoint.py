from fastapi import FastAPI, status, APIRouter
from pydantic import BaseModel
from app.component_module.table import write_table
from app.component_module.viz import draw_chart
import pandas as pd

# class Crosstabs(BaseModel):
#     df: pd.DataFrame 
#     demos: list[str] 
#     wise: str
#     q_ls: list[str] 
#     multi: list[str] 
#     name_sort: list[str] 
#     weight: str
#     col_seqs: dict

#     class Config:
#         arbitrary_types_allowed = True

# class Charts(BaseModel):
#     dfs: list[pd.DataFrame]
#     sheet_names: list

#     class Config:
#         arbitrary_types_allowed = True

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

# @router.post("/crosstabs", tags=["crosstabsgen"])
# async def generate_crosstabs(crosstabs: Crosstabs):
#     '''
#     Endpoint to generate crosstabs based on the weighted survey file.

#     Request:
#         - df: pandas DataFrame 
#         - demos: List of name of the selected demography columns. 
#         - wise: User selection of the value options. 
#         - q_ls: List of question column. 
#         - multi: List of column that contains multiple answer option.
#         - name_sort: List of column to sort by the name. 
#         - weight: Name of the selected weight column [str]
#         - col_seqs:
#             - Key: Demography column
#             - Value: Sorted unique value of the key demography column.
    
#     Return:
#         - df_xlsx: conversion result of pandas ExcelWriter that contains crosstabs table into bytes.
#     '''
#     pass # will continue later

app.include_router(router)