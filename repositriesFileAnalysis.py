import pandas as pd
import sqlite3

repos_df = pd.read_csv('repositories.csv')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
conn = sqlite3.connect('repositories.db')                                 

repos_df.to_sql('repositories', conn, if_exists='replace', index=False)

#query = "Select language,Count(language) from repositories where created_at > '2020-12-31T59:59:00Z' group by language order by Count(language) desc"   #Q2
query = "Select license_name,Count(license_name) from repositories group by license_name order by Count(license_name) desc"    #Q8

repos_df['popular_licenses'] = pd.read_sql_query(query, conn)

Top3_popular_license = repos_df.nlargest(3, 'popular_licenses')

print(Top3_popular_license)
conn.close()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------
      #Q7
language_stats = repos_df.groupby('language').agg(
    total_stars=('stargazers_count', 'sum'),
    total_repos=('full_name', 'count')
).reset_index()

language_stats['average_stars'] = language_stats['total_stars'] / language_stats['total_repos']

highest_avg_language = language_stats.loc[language_stats['average_stars'].idxmax()]

print(f"The language with the highest average number of stars per repository is {highest_avg_language['language']} "
      f"with an average of {highest_avg_language['average_stars']:.2f} stars.")



#------------------------------------------------------------------------------------------------------------------------------------------------------------------


repos_df['has-projects-enabled'] = repos_df.apply(lambda row: 'Yes' if (row['has_projects'] == True) else 'No', axis=1 )
repos_df['has-wiki-enabled'] = repos_df.apply( lambda row: 'Yes' if (row['has_wiki'] == False) else 'No', axis=1)

repos_df['has-projects-enabled'] = repos_df['has-projects-enabled'].map({'Yes': 1, 'No': 0})
repos_df['has-wiki-enabled'] = repos_df['has-wiki-enabled'].map({'Yes':1, 'No':0})
# repos_df['has-projects-enabled'] = np.where((repos_df['has_projects'] == True, 'Yes', 'No'))
# repos_df['has-wiki-enabled'] = np.where((repos_df['has_wiki'] == True, 'Yes', 'No'))
corr = repos_df['has-projects-enabled'].corr(repos_df['has-wiki-enabled'])
print(round(corr,3))

repos_df['has_projects'] = repos_df['has_projects'].astype(bool)
repos_df['has_wiki'] = repos_df['has_wiki'].astype(bool)

condition = (repos_df['has_projects'] == True) & (repos_df['has_wiki'] == True)
filtered_repos = repos_df[condition]

correlation = filtered_repos['has_projects'].corr(filtered_repos['has_wiki'])
print(round(correlation, 3))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# #Q14
repos_df['created_at'] = pd.to_datetime(repos_df['created_at'])
repos_df['day_of_week'] = repos_df['created_at'].dt.dayofweek
weekend_repos = repos_df[repos_df['day_of_week'].isin([5, 6])]
repo_counts = weekend_repos['login'].value_counts()


top_5_users = repo_counts.head(5).index.tolist()
print(top_5_users)
