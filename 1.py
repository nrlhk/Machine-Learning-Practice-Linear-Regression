import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read data, fix header fr dataset, state NA values:
df = pd.read_excel(
    'indo_12_1.xls',
    header=3,
    na_values = '-'
)

# Take data that needed only:
df = df[0:34]

# for Checking purpose only:
# print(df)
# print(df.iloc[33])
# print(df.iloc[0])
# print(df.head(2))
# print(df.columns)

# Transpose dataframe
dfT = df[0:34].T
# print(dfT)

# Create header var
header = dfT.iloc[0]
# print(header)

# replace dataframe which not contain first row
dfT = dfT[1:]
# print(dfT)

# header become column name
dfT = dfT.rename(columns = header)
# print(dfT)

# Data cleaning, 1: drop NA value
dfT = dfT.dropna(how='all')
# another way >> 2. change to 0 >>> dfT = dfT.fillna(0)

# Find MIN in 1971
# Cek mintahun 1971
min = dfT.iloc[0].sort_values().head(1)
minI = min.index
# print(dfT[minI])

# Find MAX in 2010
max = dfT.iloc[5].sort_values(ascending=False).head(2)
maxI = max.index[1]
# print(dfT[maxI])

# Plotting subplot 1
plt.figure('1', figsize=(13, 5))
plt.style.use('ggplot')
plt.subplot(121)
plt.plot(
    dfT.index, dfT[maxI], 'g-',
    dfT.index, dfT[minI], 'b-',
    dfT.index, dfT['INDONESIA'], 'r-',
    dfT.index, dfT[minI], 'bo',
    dfT.index, dfT[maxI], 'go',
    dfT.index, dfT['INDONESIA'], 'ro',
)

plt.title('Jumlah Penduduk Indonesia (1971-2010)')
plt.xlabel('Tahun')
plt.ylabel('Jumlah penduduk (ratus juta jiwa)')
plt.legend(['Jawa Barat', 'Bengkulu', 'INDONESIA'])
plt.grid(True)
 
# plt.show()


# Linear regression sklearn
from sklearn import linear_model
model = linear_model.LinearRegression()
dfR = dfT.reset_index()
print(dfR)

# training fir for Indonesia prediction and best fit line
fitInd = model.fit(dfR[['index']], dfT['INDONESIA'])
print('Slope = ', model.coef_)
print('Slope = ', model.intercept_)
print(model.predict([[2050]]))

dfT['IndoBest'] = model.predict(dfR[['index']])
# print(dfT)

# training for max by province prediction and best fit line
fitMaxI = model.fit(dfR[['index']], dfT[maxI])
print('Slope = ', model.coef_)
print('Slope = ', model.intercept_)
print(model.predict([[2050]]))
dfT['2010Max'] = model.predict(dfR[['index']])

# training for min by province prediction and best fit line
fitMinI = model.fit(dfR[['index']], dfT[minI])
print('Slope = ', model.coef_)
print('Slope = ', model.intercept_)
print(model.predict([[2050]]))
dfT['1971Min'] = model.predict(dfR[['index']])
# print(dfT)

# Plotting subplot 2
plt.style.use('ggplot')
plt.subplot(122)

plt.plot(
    dfT.index, dfT[maxI], 'g-',
    dfT.index, dfT[minI], 'b-',
    dfT.index, dfT['INDONESIA'], 'r-',
    dfT.index, dfT['IndoBest'], 'y-',
    dfT.index, dfT['2010Max'], 'y-',
    dfT.index, dfT['1971Min'], 'y-',
    dfT.index, dfT[minI], 'bo',
    dfT.index, dfT[maxI], 'go',
    dfT.index, dfT['INDONESIA'], 'ro',
)

plt.title('Jumlah Penduduk Indonesia (1971-2010)')
plt.xlabel('Tahun')
plt.ylabel('Jumlah penduduk (ratus juta jiwa)')
plt.legend(['Jawa Barat', 'Bengkulu', 'INDONESIA', 'Best Fit Line'])
plt.grid(True)

plt.subplots_adjust(
    left=0.06, bottom=0.11, right=0.97, top=0.88,
    wspace=.2, hspace=.2
)

plt.savefig('PendudukIndo.png')
plt.show()
