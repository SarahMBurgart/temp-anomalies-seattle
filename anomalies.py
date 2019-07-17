import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as scs

#make it pretty
plt.style.use('ggplot')



# clean data set of null values for one column
# returns new dataframe

def no_more_null (df, col_1, col_2):
    #drop rows where both columns are null
    
    df_mask = df[(df[col_1].isna()) & (df[col_2].isna())]
    df.drop(df_mask.index, inplace=True)
    return df

def year_month_cols (df):
    df['year'] = pd.DatetimeIndex(df.loc[:,'DATE']).year
    df['month'] = pd.DatetimeIndex(df.loc[:,'DATE']).month
    return df

def months_equally_weighted(df,lst_years,col):
    # for each year in the df
    # each month equal to 1/12 of the average if there are 12
    # return list of year:month for any month that doesn't have values
    
    # create list to return with month means = 0
    zero_months = []
    half_years = []
    # list of years,means
    weighted_years = []
    # year_means = pd.DataFrame(year_ms["HourlyDryBulbTemperature"].mean())
    # for each year lst of years in df
    for year in lst_years:
        # list of means from months
        means = []
        temp_df = df[df["year"] == year]
        #print(year)
        # get mean value for each month in the year:
        for x in range(1,13):
            res = temp_df[temp_df["month"] == x][col].astype(float).mean()
            #print(res)
            #if res == np.inf:
                #return temp_df[temp_df["month"] == x][col]
                #print("shape is:", temp_df[temp_df["month"] == x][col].shape)
            # if mean = 0, add (year,month) to list
            if res is np.nan:
                zero_months.append((year, x))
            # else, add to means list
            else:
                means.append(res)
            
        # if the means list length = 12, find average and add to weighted years list as a tuple year, mean
        if len(means) == 12:
            year_mean = ((sum(means))/ 12)
            weighted_years.append((year, year_mean))
        elif len(means) > 6:
            half_years.append(year)
            
        
    # return lists
   # f"months with a mean of zero: {zero_months}  years with all months present: {weighted_years} years with half data: {half_years}"
    return weighted_years