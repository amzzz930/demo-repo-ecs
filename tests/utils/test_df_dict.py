import sys
from pathlib import Path

from utils.df_dict import df_a

def test_df_a():

    result = df_a()
    result_dict = result.to_dict(orient='records')
    assert result_dict[0]['column1'] == 7