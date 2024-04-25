from pydantic import BaseModel
import pandas as pd
from typing import List, Dict

class DataframeSchema(BaseModel):
    '''
    df: dataframe that consists survey responses.
    '''
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ColumnSearchSchema(DataframeSchema):
    '''
    key: keyword to match the column name. 
    '''
    key: str

class DemoSorterSchema(DataframeSchema):
    '''
    demo: column name of the demography to be built on the table.
    '''
    demo: str

class CrosstabSchema(DataframeSchema): 
    '''
    df: pandas DataFrame 
    demos: List of name of the selected demography columns. 
    wise: User selection of the value options. 
    q_ls: List of question column. 
    multi: List of column that contains multiple answer option.
    name_sort: List of column to sort by the name. 
    weight: Name of the selected weight column [str]
    col_seqs:
        Key: Demography column
        Value: Sorted unique value of the key demography column.
    '''
    demos: List[str] 
    wise: str
    q_ls: List[str] 
    multi: List[str] 
    name_sort: List[str] 
    weight: str
    col_seqs: Dict

class ChartSchema(BaseModel):
    '''
    dfs: list of pandas DataFrame 
    sheet_names: list of the sheet names in the crosstabs file.
    '''
    dfs: List[pd.DataFrame]
    sheet_names: List[str]

    class Config:
        arbitrary_types_allowed = True