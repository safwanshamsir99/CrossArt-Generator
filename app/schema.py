from pydantic import BaseModel
import pandas as pd
from typing import List, Dict

class DataframeSchema(BaseModel):
    '''
    Pydantic schema for pandas dataframe data type with BaseModel.
    '''
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ColumnSearchSchema(DataframeSchema):
    '''
    Pydantic schema for col_search() endpoint with DataframeSchema.
    '''
    key: str

class DemoSorterSchema(DataframeSchema):
    '''
    Pydantic schema for sorter() endpoint with DataframeSchema.
    '''
    demo: str

class CrosstabSchema(DataframeSchema): 
    '''
    Pydantic schema for crosstabs generator endpoint with DataframeSchema.
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
    Pydantic schema for chart generator endpoint with BaseModel. 
    '''
    dfs: List[pd.DataFrame]
    sheet_names: List[str]

    class Config:
        arbitrary_types_allowed = True