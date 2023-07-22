import pandas as pd
df = pd.read_csv('job_data.csv')

#remove records with no salary
df = df.dropna(subset=['Salary'])

#hourly salary
df['hourly'] = df['Salary'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

#check if salary provided by employer
df['employer provided'] = df['Salary'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

#salary parsing to numbers
#remove glassdoor estimate
salary = df['Salary'].apply(lambda x:x.split("(")[0])

#remove K and $
salary = salary.apply(lambda x:x.replace('K','').replace('$',''))

#remove employer provided salary
salary = salary.apply(lambda x:x.split(':')[1] if len(x.split(':'))>1 else x)

#remove per hour
clean_salary = salary.apply(lambda x:x.replace('Per Hour',''))

df['min_salary'] = clean_salary.apply(lambda x:float(x.split('-')[0]))

df['max_salary'] = clean_salary.apply(lambda x:float(x.split('-')[1] if(len(x.split('-'))>1) else 0))

df['avg_salary'] = df.apply(lambda row:(row['min_salary']+row['max_salary'])/2 if row['max_salary']>0 else row['min_salary'], axis=1)

#extracting state
df['job_state'] = df['Location'].apply(lambda x:x.split(',')[1].strip() if(len(x.split(','))>1) else x)
df.job_state.value_counts()

#age of company
df['age'] = df.Founded.apply(lambda x:x if x < 1 else 2023-x)

#parsing job description (python etc.)
#python
df['python_yn'] = df['Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
#r studio
df['R_yn'] = df['Description'].apply(lambda x: 1 if 'r studio' in x.lower() else 0)
df.R_yn.value_counts()
#spark
df['spark_yn'] = df['Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()
#aws
df['aws_yn'] = df['Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws_yn.value_counts()
#excel
df['excel_yn'] = df['Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel_yn.value_counts()

df.columns
df_out = df.drop(['Number'], axis=1)

df_out.to_csv('Salary_data_cleaned.csv',index = False)

pd.read_csv('Salary_data_cleaned.csv')