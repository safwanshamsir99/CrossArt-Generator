from pydantic import BaseModel
from typing import List, Dict

class DataframeSchema(BaseModel):
    '''
    df: JSON string that contains survey response in dictionary.

    Eg: 
        - '{"1. [LIKERT] Opinions":"5)Very Negative","2. What is your dream job field?":"Entrepreneurship","Gender":"Male","IncomeGroup":"B40","untrimmed_weight":0.506694401,"trimmed_weight":1.14631426}'
    '''
    df: str

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
    df: dataframe in JSON string that contains survey response in dictionary.
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
    multi: List[str] = None
    name_sort: List[str] = None
    weight: str
    col_seqs: Dict

class ChartSchema(BaseModel):
    '''
    dfs: list of dataframe in JSON string
    sheet_names: list of the sheet names in the crosstabs file.
    '''
    dfs: List[str]
    sheet_names: List[str]