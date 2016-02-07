import time
import pandas as pd
start = time.time()
x=pd.read_csv('rotation.csv')
end = time.time()
print(end - start)
