# banglore-users
This repo contains data of users in Bangalore with over 100 followers and their repositories.


3 Bullet Points
---------------

1. Made a GET request with filter criteria as query param. For the users recieved in response, fetched user details. Using the same process fetched data for Repository details. Saved the data incsv files as required.

2. Pascal language having highest average number of stars per repository, although the language's popularity has waned substantially..

3. To make your work popular, keep adding repos as from the analysis it is evident that the users who create more repositories tend to attract more followers.




Detailed steps of Scrapping
----------------------------
1. First of all, I generated a token for Github API with validity of 30 days.
2. Then using the criteria provided (i.e. location:Banglore & followers>=100), searched the users.
3. After I have the result for the users meeting the specified criteria, I fetched the User   details for every user in my list.
4. Similarly I fetched the repository information for all the users in our list.
5. Stored all the fetched data into csv files, done for each Users and Repositries individually.
