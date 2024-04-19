from app.component_module.table import write_table
from pathlib import Path
import pandas as pd
import pytest
from app.chart_module.chart import load_chart
from app.component_module.viz import draw_chart
from app.utils_module.utils import (
    load, 
    demography,
    col_search,
    sorter
)

# --------------------------- Crosstabs Generator ------------------------------------------
'''
NOTE: 
    1. Base script: crosstabs.py (in crosstabs_module folder)
    2. Middle script: processor.py (in utils_module folder)
    3. Top script: table.py (in component_module folder)

Only top script will be gone through unit testing process.
Reasons: 
    1. Functions in middle script will call the functions in base script.
    2. Functions in top script will call the functions in middle script.

This is also known as integration unit testing. 
'''
def test_weighted_file_exist():
    '''
    Test to check whether the test_crosstabs.csv file is exist.
    '''
    file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'

    assert file_path.exists() == True, "test_crosstabs.csv does not exist"

def test_write_table():
    '''
    Test to check the write_table() function is working
    by returning pandas Excelwriter in bytes.
    '''
    file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'

    df = pd.read_csv(file_path)
    demos = ['Gender', 'IncomeGroup']
    wise = 'Both'
    q_ls = [
        '1. [LIKERT] Opinions',
        '2. What is your dream job field?'
    ]
    multi = []
    name_sort = ['1. [LIKERT] Opinions']
    weight = 'untrimmed_weight'
    col_seqs = {
        'Gender': ['Male', 'Female'],
        'IncomeGroup': ['B40', 'M40', 'T20']
        }
    
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

    assert isinstance(
        df_xlsx, bytes
        ), "Output is not in bytes"

# --------------------------- Chart Generator ------------------------------------------
'''
NOTE: 
    1. Helper script: chart.py (in chart_module folder)
    2. Top script: viz.py (in component_module folder)

Only top script will be gone through unit testing process.
Reason: 
    1. Functions in top script will call the functions in helper script.

This is also known as integration unit testing. 
'''
def test_crosstabs_file_exist():
    '''
    Test to check whether the test_chartgen.xlsx file is exist.
    '''
    file_path = Path.cwd() / 'tests' / 'test_chartgen.xlsx'

    assert file_path.exists() == True, "test_chartgen.xlsx does not exist"

def test_draw_chart():
    '''
    Test to check whether the draw_chart() function is working
    by returning xlsxwriter charts in bytes.
    '''
    file_path = Path.cwd() / 'tests' / 'test_chartgen.xlsx'

    dfs, sheet_names, _ = load_chart(df_charts=file_path)
    df_charts = draw_chart(dfs=dfs, sheet_names=sheet_names)

    assert isinstance(
        df_charts, bytes
        ), "Output is not in bytes"

# --------------------------- Utils Function ------------------------------------------
@pytest.fixture
def get_test_file_path()->Path:
    '''
    Pytest fixture to return path for the test file. 
    '''
    test_file_path = Path.cwd() / 'tests' / 'test_crosstabs.csv'
    return test_file_path

@pytest.fixture
def get_test_df_crosstabs(get_test_file_path: Path)->pd.DataFrame:
    '''
    Extended fixture to read the test file path and 
    return read pandas dataframe
    '''
    df_crosstabs = pd.read_csv(get_test_file_path)
    return df_crosstabs

def test_load(get_test_file_path: Path):
    '''
    Test the load feature into pandas dataframe.
    '''
    df = load(get_test_file_path)
    assert isinstance(
        df, pd.DataFrame
        ), "Output is not pandas dataframe"

def test_demography(get_test_df_crosstabs:pd.DataFrame):
    '''
    Test the demography auto-detection method based on certain demography keyword.
    '''
    demo_list = demography(get_test_df_crosstabs)
    assert isinstance(
        demo_list, list
    ), "Output is not a list"

def test_col_search(get_test_df_crosstabs:pd.DataFrame):
    '''
    Test the column auto-detection search based on any keyword.
    Extended fixture to return list of searched column based on keyword.
    '''
    col_with_keyword = col_search(df=get_test_df_crosstabs, key='LIKERT')
    assert isinstance(
        col_with_keyword, list
    ), "Output is not a list"
    assert all(
        'LIKERT' in col for col in col_with_keyword
        ), "No keyword 'LIKERT' exists in the list"

def test_sorter(get_test_df_crosstabs:pd.DataFrame):
    '''
    Test the sorter function to sort the selected demography column.
    '''
    sorted_demo_list = sorter(demo='IncomeGroup', df=get_test_df_crosstabs)
    assert isinstance(
        sorted_demo_list, list
    ), "Output is not a list"
    expected_order = ['B40', 'M40', 'T20']
    assert (
        sorted_demo_list == expected_order
        ), "Output is not sorted in the expected order"
    
'''
NOTE: 
    - sort_order() function in the utils.py (in utils_module folder) will not undergo unit testing.
    Reasons:
        - sort_order() function is a helper function when the crosstabs table is being build.
        - It is being utilized in the base script; crosstabs.py (in crosstabs_module folder)
        - Hence, it is hard to do a comparison of the expected output with the actual output
    
    - With that being said, the expected output and actual output can be tested manually only.
    Steps:
        1. Upload the weighted survey responses on the crosstabs generator. 
        2. During the sort order option, select any question column that you want to sort the 
        order based on the name. Usually, it is a likert question column with these unique values;
            1) Very negative
            2) Negative
            3) Neutral
            4) Positive
            5) Very positive
        3. Once the crosstabs has been processed and downloaded, open the file and compare the 
        selected column that you want to sort by name order. 
        4. If it is sorted by the order of the name, then the sort_order() function wort as 
        intended.
'''


