import pandas as pd
import sqlite3
from collections import Counter
import statsmodels.api as sm


df = pd.read_csv('users.csv')

df['created_at'] = pd.to_datetime(df['created_at'])
df_sorted = df.sort_values(by='created_at')
quick5s = df_sorted['login'].head
print(quick5s)


conn = sqlite3.connect('users.db')


df.to_sql('users', conn, if_exists='replace', index=False)

query = "SELECT * FROM users"
result = pd.read_sql_query(query, conn)


conn.close()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q8
df['leader_strength'] = df['followers'] / (1 + df['following'])    

# Get the top 5 users by leader_strength
top_users = df.nlargest(5, 'leader_strength')

# Extract their logins and format as a comma-separated string
top_logins = ','.join(top_users['login'])

print(top_logins)



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q16
def extract_surname(name):                                            
    if pd.isna(name) or name.strip()=="":
        return None
    return name.strip().split()[-1]

df['surname'] = df['name'].apply(extract_surname)

surnames = df['surname'].dropna()

surname_counts = Counter(surnames)
max_count = max(surname_counts.values())
most_common_surnames = [surname for surname , count in surname_counts.items() if count == max_count]
print(most_common_surnames)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Q9
correlation = df['followers'].corr(df['public_repos'])
print(round(correlation, 3))

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
userCount = df.count() 


df['email'] = df['email'].fillna('') 


filtered_hireable_mail = df[(df['hireable']) & (df['email'] != '' )]
total_hireable = df[df['hireable']]
fraction_users_hireableWithEmail = round(filtered_hireable_mail.count()/total_hireable.count(), 3)

filtered_rest_with_mail = df[(df['hireable'] != True) & (df['email'] != '' )]
total_non_hireable = df[df['hireable'] == False]
fraction_users_restWithEmail = round(filtered_rest_with_mail.count()/total_non_hireable.count(),3)


print(fraction_users_hireableWithEmail)
print(fraction_users_restWithEmail)

#--------------------------------------------------------------------------------------------------------------------------

# # Q10

df = df[['public_repos', 'followers']].dropna()

X = df['public_repos']
y = df['followers']

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

slope = model.params['public_repos']

print(round(slope, 3))

#-----------------------------------------------------------------------------------------------------------
df['created_at'] = pd.to_datetime(df['created_at'])

df['day_of_week'] = df['created_at'].dt.dayofweek

weekend_repos = df[(df['day_of_week'] == 5) | (df['day_of_week'] == 6)]

user_counts = weekend_repos['login'].value_counts().head(5)

top_users = user_counts.index.tolist()

print(top_users)
