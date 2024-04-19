from app.component_module.table import write_table
from pathlib import Path
import pandas as pd
from app.chart_module.chart import load_chart
from app.component_module.viz import draw_chart

# --------------------------- Crosstabs Generator ------------------------------------------
'''
NOTE: 
    1. Base script: crosstabs.py (in crosstabs_module folder)
    2. Middle script: processor.py (in utils_module folder)
    3. Top script: table.py (in component_module folder)

Only top script will be gone through unit testing process.
Reason: 
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
        '1. [LIKERT] Opinions regarding the cancellation of the Batu Pahat factory license that made Allah stockings',
        '2. What is your dream job field?'
    ]
    multi = []
    name_sort = ['1. [LIKERT] Opinions regarding the cancellation of the Batu Pahat factory license that made Allah stockings']
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





