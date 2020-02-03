import praw
import pdb
from prawcore import NotFound as SubredditNotFound
import keys
SUBREDDIT_QUERY = None
REDDIT_CLIENT = praw.Reddit(client_id=keys.client_id,
                            client_secret=keys.client_secret,
                            user_agent=keys.user_agent)


def scrap_redditors(subreddit_ins, limit=100):
    redditors = []
    post_ids = []
    posts = subreddit_ins.top('week')
    for p in posts:
        redditors.append(p.author)
        post_ids.append(p.id)
    for p_id in post_ids:
        if len(redditors) < limit:
            submission = REDDIT_CLIENT.submission(
                id=p_id)
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                if len(redditors) < limit:
                    redditors.append(comment.author)
                else:
                    break
        else:
            break
    return redditors


def main():
    global SUBREDDIT_QUERY, USER_LIMIT
    SUBREDDIT_QUERY = input(
        'Enter subreddit name(e.g MachineLearning): ').strip()
    try:
        subreddit_instance = REDDIT_CLIENT.subreddits.search_by_name(
            SUBREDDIT_QUERY, exact=True)[0]
    except SubredditNotFound and IndexError:
        print(f'ERROR: Incorrect subreddit name, try again.')
        exit(1)
    try:
        USER_LIMIT = int(input('Enter number of users to scrap: '))
    except ValueError:
        print(f'ERROR: Incorrect users number, try again.')
        exit(1)

    redditors = scrap_redditors(subreddit_instance, USER_LIMIT)


if __name__ == "__main__":
    main()
