import os
import pandas as pd #imports pandas with pd as an alias to perform data transformations
df = pd.read_csv('players_stats_by_season_full_details.csv') #imports csv file as a dataframe

#creates universal access to file
file_path = os.path.join(os.getcwd(), "players_stats_by_season_full_details.csv")
df = pd.read_csv(file_path)

regular_season_df = df[df["Stage"] =='Regular_Season'] #defines a data frame that includes only data with values 'Regular_Season' in the column 'Stage'
regular_season_df = regular_season_df.reset_index(drop=True) #resets index to avoid future errors

season_counts = regular_season_df.groupby('Player')['Season'].nunique() #takes values from columns 'Players' and 'Season' and groups based off their unique values

most_seasons_player = season_counts.idxmax() #identifies the player with the highest value in season_counts

print("Player with most regular seasons:", most_seasons_player) #prints the player with the most regular seasons
print("Number of seasons played:", season_counts.max()) #prints the number of seasons the player played (max value from season_counts)

player_df = regular_season_df[regular_season_df['Player'] == most_seasons_player].copy() #creates a new dataframe from the data of the player with the highest seasons
player_df["3P%"] = player_df["3PM"] / player_df["3PA"] #creates a new column in the df with each value calculated based off each value of the 3PM / 3PA
season_accuracy = player_df.groupby('Season').agg({'3PM': 'sum','3PA': 'sum'}) #groups the data by each unique season and sums all 3PM values and all 3PA values per season

season_accuracy["3P%"] = season_accuracy["3PM"] / season_accuracy["3PA"] #creates new column in season_accuracy with values based off each season's 3PM / 3PA

print(season_accuracy[["3P%"]]) #prints each season's accuracy

season_accuracy = season_accuracy.reset_index() #resets index of season_accuracy
season_accuracy["Year"] = season_accuracy["Season"].str[:4].astype(int) #converts each year to an integer so it can be used in a line regression

from scipy.stats import linregress #imports line regression from scipy

x = season_accuracy["Year"] #defines x axis as the values from "Year" in season_accuracy
y = season_accuracy["3P%"] #defines y axis as 3 point accuracies from each season

regression = linregress(x, y) #runs linear regression

slope = regression.slope #returns regression's slope
intercept = regression.intercept #returns regression's intercept

season_accuracy["Best_Fit_Line"] = slope * x + intercept #calculates the line of best fit using y=mx+b
earliest = season_accuracy["Year"].min() #defines the first year in regression
latest = season_accuracy["Year"].max() #defines last year in regression

from scipy.integrate import quad #imports quad from scipy

def f(x): #defines function to be integrated in y=mx+b format
    return slope * x + intercept

integral_value, _ = quad(f, earliest, latest) #calculates the definite integral

average_fit_accuracy = integral_value / (latest - earliest) #calculates the average 3 point accuracy for all years played
print("Average 3P%:", average_fit_accuracy)

actual_average_accuracy = season_accuracy["3P%"].mean() #calculates the true mean of all 3P% values
print("Actual average 3P%:", actual_average_accuracy)


difference = average_fit_accuracy - actual_average_accuracy #calculates the difference in the average from the regression and the true average
print("Difference:", difference)

season_accuracy = season_accuracy.sort_values("Year") #sorts season accuracy based on year to reduce errors in interpolation

from scipy.interpolate import interp1d

interp_function = interp1d(season_accuracy["Year"],season_accuracy["3P%"],kind='linear') #defines interpolate function for 3P% for any year in between my data points using a linear model

estimate_2002 = float(interp_function(2002)) #estimates 3P% for 2002
estimate_2015 = float(interp_function(2015))#estimates 3P% for 2015

print("Estimated 3P% for 2002-2003 season:", estimate_2002)
print("Estimated 3P% for 2015-2016 season:", estimate_2015)

import numpy as np
from scipy import stats

fgm = df["FGM"].dropna().values #drops all null values from "FDM"
fga = df["FGA"].dropna().values #drops all null values from "FDA"

fgm_mean = np.mean(fgm) #calculates average of field goals made
fgm_var = np.var(fgm, ddof=1) #calculates a sample variance from fgm values
fgm_skew = stats.skew(fgm) #calculates skew of fgm
fgm_kurt = stats.kurtosis(fgm) #calculates fgm kurtosis

#calculates same stats for field goals made
fga_mean = np.mean(fga)
fga_var = np.var(fga, ddof=1)
fga_skew = stats.skew(fga)
fga_kurt = stats.kurtosis(fga)

print("FGM Statistics")
print("Mean:", fgm_mean)
print("Variance:", fgm_var)
print("Skew:", fgm_skew)
print("Kurtosis:", fgm_kurt)

print("\nFGA Statistics")
print("Mean:", fga_mean)
print("Variance:", fga_var)
print("Skew:", fga_skew)
print("Kurtosis:", fga_kurt)

from scipy.stats import ttest_rel, ttest_ind

paired_df = df[["FGM", "FGA"]].dropna() #pairs FGM and FGA to ensure they have the same number of values and drops null values

fgm_paired = paired_df["FGM"] #defines fgm with correct number of values
fga_paired = paired_df["FGA"] #defines fga with correct number of values

paired_test = ttest_rel(fgm_paired, fga_paired) #performs a paired t test on fga and fgm
print("Paired (Relational) T-Test")
print("t-statistic:", paired_test.statistic)
print("p-value:", paired_test.pvalue)

#performs an independent t test
independent_test = ttest_ind(fgm, fga)
print("\nIndependent T-Test")
print("t-statistic:", independent_test.statistic)
print("p-value:", independent_test.pvalue)



