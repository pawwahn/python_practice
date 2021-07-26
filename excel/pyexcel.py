from pyexcel_xlsx import save_data
from collections import OrderedDict
import os
data = OrderedDict() # from collections import OrderedDict
data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]})
data.update({"Sheet 2": [["row 1", "row 2", "row 3"]]})
print os.getcwd()
save_data("your_file.xlsx", data)