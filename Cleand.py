import pandas as pd
import shutil
import os
# clean process of the employee file
dfemp = pd.read_csv('D:\HR_Dataset\Employee.csv')
print(dfemp.columns)
print(dfemp.shape)
print(dfemp.isnull().sum())  # no null values in the data
print(dfemp.duplicated())    # no duplicate values 
print(dfemp.dtypes)
# change data type of colunm hiredate to date type
dfemp['HireDate']=pd.to_datetime(dfemp['HireDate']) 
print(dfemp.dtypes) 
dfemp['FirstName']=dfemp['FirstName']+' '+ dfemp['LastName']
dfemp.drop(columns='LastName', axis=1 , inplace=True)
dfemp.rename({'FirstName':'EmployeeName'},inplace=True,axis=1)
print(dfemp.head())
# cleaning process of the performance file
dfperf= pd.read_csv('D:\HR_Dataset\PerformanceRating.csv')
print(dfperf.columns)
print (dfperf.isnull().sum())
print(dfperf.duplicated)
print(dfperf.dtypes)
#change the type of reviewdate to date type
dfperf['ReviewDate']=pd.to_datetime(dfperf['ReviewDate']) 
print(dfperf.dtypes)
#merging table of employee with performancerating table
dfemplperf=pd.merge(dfperf,dfemp,on='EmployeeID',how='left')
print (dfemplperf.columns)
print (dfemplperf.shape)
#define the rest of the files
dfedu=  pd.read_csv('D:\HR_Dataset\EducationLevel.csv')
dfrat=  pd.read_csv('D:\HR_Dataset\RatingLevel.csv')
dfsat=  pd.read_csv('D:\HR_Dataset\SatisfiedLevel.csv')
print(dfedu.columns)
print(dfrat.columns)
print(dfsat.columns)
#merging all tables to build data model
merged_df = (
    dfemp.merge(dfperf, on="EmployeeID", how="left")
               .merge(dfedu, left_on="Education", right_on="EducationLevelID", how="left")
               .merge(dfrat, left_on="SelfRating", right_on="RatingID", how="left")
               .merge(dfsat, left_on="JobSatisfaction", right_on="SatisfactionID", how="left")
)

print(merged_df.head())
print(merged_df.columns)
# drop the id columns 
drop_cols = ["EducationLevelID", "RatingID", "SatisfactionID"]
merged_df.drop(columns=[col for col in drop_cols if col in merged_df.columns], inplace=True)
print(merged_df.columns)
print(merged_df.shape) # found 6899 rows , 35 columns 
print(merged_df.head())
print(merged_df.isnull().sum())

#found 190 null values in the merged data frame
# Replace missing categorical values with "Unknown"
for col in ["RatingLevel", "SatisfactionLevel"]:
    merged_df[col] = merged_df[col].fillna("Unknown")

# Fill missing numerical values with median
for col in [
    "EnvironmentSatisfaction", "JobSatisfaction", "RelationshipSatisfaction",
    "TrainingOpportunitiesWithinYear", "TrainingOpportunitiesTaken", "WorkLifeBalance",
    "SelfRating", "ManagerRating"
]:
    median_value = merged_df[col].median()
    merged_df[col] = merged_df[col].fillna(median_value)
print(merged_df.isnull().sum())
print(merged_df.shape)
# there are two columns which have 190 null values (PerformanceID ,ReviewDate ) 
# Fill missing PerformanceID with NOReview
merged_df["PerformanceID"] = merged_df["PerformanceID"].fillna("NoReview")
# Convert ReviewDate to datetime and fill missing with a placeholder date or NaT
merged_df["ReviewDate"] = pd.to_datetime(merged_df["ReviewDate"], errors="coerce")
# Fill with a placeholder date instead of NaT
merged_df["ReviewDate"] = merged_df["ReviewDate"].fillna(pd.Timestamp("1900-01-01"))
print(merged_df.shape)
print(merged_df.head())
print(merged_df.isnull().sum())  
# Save the cleaned DataFrame to a CSV file
merged_df.to_csv("HR_Dataset_Cleaned.csv", index=False)
print("File saved successfully at:", os.path.abspath("HR_Dataset_Cleaned.csv"))


