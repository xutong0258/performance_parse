import pandas as pd
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *
from base.fileOP import *

file = r'D:\小拉\tdms_issues_202508121503\tdms_issues_202508121503.csv'
content_list = get_file_content_list(file)
print(content_list[0])