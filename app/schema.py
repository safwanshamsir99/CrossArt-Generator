from pydantic import BaseModel
import pandas as pd
from typing import List, Dict

class DataframeSchema(BaseModel):
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ColumnSearch(DataframeSchema):
    key: str

class DemoSorter(DataframeSchema):
    demo: str

class CrosstabSchema(DataframeSchema): 
    demos: List[str] 
    wise: str
    q_ls: List[str] 
    multi: List[str] 
    name_sort: List[str] 
    weight: str
    col_seqs: Dict

class ChartSchema(BaseModel):
    dfs: List[pd.DataFrame]
    sheet_names: List[str]

    class Config:
        arbitrary_types_allowed = True