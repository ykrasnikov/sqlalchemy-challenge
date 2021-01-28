# sqlalchemy-challenge

sqlalchemy Homework - Climate API 

<img src="Images/anaconda.gif" align="left" height="200"/>
<img src="Images/panda.gif" align="right" height="200"/>
<img src="Images/surfs-up.png" align="center" height="200"/>

please note - code is PythonCode directory

_______________________

## Part 1. 
### 1.1 Climate Analysis & Exploration

connect to database
sqlite database -[Resources\hawaii.sqlite](Resources/hawaii.sqlite)

- 2 tables - Measurements with weather data and Stations with weather stations data

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)


______________________

### 1.2. Precipitation Analysis 
Most recent data date '2017-08-23'.
Data query for 365 days back  from most recent data date

#### Plot Precipitation vs date barchart all stations data 
<img src="Images/daily_prcp.png" align="center" height="300"/>

_______________

#### summary statistics for the precipitation data

data|	prcp
---|    ---
count|	2021.000000
mean|	0.177279
std|    0.461190
min|	0.000000
25%|    0.000000
50%|	0.020000
75%|	0.130000
max|	6.700000

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)

____________________

#### Plot AVERAGE Precipitation vs date barchart all stations data 

<img src="Images/daily_average_prcp.png" align="center" height="300"/>

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)

______________________

### 1.3. Station Analysis 
#### Most active stations
Station id|Station| Data count
---|---|---
7| 'USC00519281'| 2772
1| 'USC00519397'| 2724
2| 'USC00513117'| 2709
6| 'USC00519523'| 2669
9| 'USC00516128'| 2612
3| 'USC00514830'| 2202
8| 'USC00511918'| 1979
4| 'USC00517948'| 1372
5| 'USC00518838'| 511

Most Active Weather Station ID = 7

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)
____________________

#### Temperature for most active station
for most active station id, calculate the lowest, highest, and average temperature.

mostactive station = 7, min temp = 54.0, max temp = 85.0, avg temp = 71.7
Temp|DegF
---|---
min temp|54.0
max temp|85.0
avg temp|71.7

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)
____________________

### 1.4 Temperature Analysis

Temperature histogram over 12 bins (1 year data)

<img src="Images/temp_his.png" align="center" height="300"/>

jupyter notebook  - [PythonCode\climate.ipynb](PythonCode/climate.ipynb)
____________________

## 2.Part 2 Climate App


Flask API  - [PythonCode/app.py](PythonCode/app.py)

____________________

## 3. Bonus 1. Other Analysis
### 3.1 Temperature - t-test
#### 1. Data is not normally distributed - we do not meet conditions for both t-test
    Jun data 
    ShapiroResult(statistic=0.9833921790122986, pvalue=1.6506709193953029e-12)
    Dec Data
    ShapiroResult(statistic=0.9817761778831482, pvalue=2.471981820628688e-12)

#### 2. The observations are sampled independently - well it is not - so we do not meet another requirement for t-test
    Temp on 2nd june is linked to temp on 1st june and so on .

#### 3. t-test null hypotheisis states that samples means are equal, resulted p-value is very low 
    Ttest_indResult(statistic=30.865349991562194, pvalue=9.8415346259008e-182)
#### 4. samples sizes are not identical - problematic to do paired t-test, and it does not make sense as temp in Dec is not paired to temp in June
#### 5. Extreamly low P-value indicates than we can reject null hypothesis as statistically insignificant 
#### 6. bottom line - bad example 
#### 7.but t-tets shows significant difference in means between the two groups of data showing that difference is not acciddental ...

jupyter notebook  - [PythonCode\temp_analysis_bonus_1.ipynb](PythonCode/temp_analysis_bonus_1.ipynb)
________________________
### 3.2 Expected temp during vacation

<img src="Images/bonus_barchart_temp.png" align="center" height="300"/>

jupyter notebook  - [PythonCode\temp_analysis_bonus_2.ipynb](PythonCode/temp_analysis_bonus_2.ipynb)
_____________________

### 3.3 Daily Normal Temperatures during vacation

<img src="Images/bonus_areaplot_temp.png" align="center" height="300"/>

jupyter notebook  - [PythonCode\temp_analysis_bonus_2.ipynb](PythonCode/temp_analysis_bonus_2.ipynb)
