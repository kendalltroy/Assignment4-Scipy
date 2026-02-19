# Assignment4-Scipy
# Purpose of a Program
The purpose of this program is to analyze NBA data, identify the player with the most regular seasons, and their three point accuracy using a variety of methods. 

# Input
The expected inputs fro this program are a .csv with expected data types. Categorical columns (string): Player, Season, Stage. Numeric Columns (integer): FGA, FGM, 3PA, 3PM.

# Expected Output
The following are the expected outputs for this program:
The player with the most seasons (string)
Season-Based 3 point accuracy table (Pandas DataFrame)
Linear Progression Results (Numeric)
Average Regression-Based 3P% (Float)
Stats on Field Goals Made & Field Goals Attempted (Float)
Independent & Paired T-Test Results (Float)

# Type of Execution
The program is a data pipeline that follows the following execution steps:
1. Load data
2. Filter data
3. Aggregate statistics
4. Perform regression
5. Calculate integral
6. Conduct t testing

This program is deterministic (it should always produce the same result, given the same data) and depends on pandas, NumPy, and SciPy.

# Possible Improvements
Because the program automatically loads the same data, it is assumed proper columns will be included in the data. If not, the program would crash. Extra guardrails to avoid this type of crashing would improve the programs flexibility. 
