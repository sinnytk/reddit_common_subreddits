# Reddit: Common Subreddits
## Freelance project
### Python 3
### Dependencies: 

A PRAW based Python bot which finds similar subreddits given any subreddit.
## Features:
- Number of users to scrap(more the amount, more data. However too many users might slow down the script heavily)

- Skip suspended accounts(sometimes suspended accounts don't have their posts/comments removed, so keeping them)

- To retrieve subreddits of a user, I am iterating over each of his/her comments and each of his posts

- From these submissions and comments, I get the belonging subreddit and make sure same subreddit comment/submission isn't counted multiple times.

- Each user has a set of subreddits, at the end: all such subreddits are output along with amount of time it occured, e.g out of 20 users following X, 5 also follow Y.