import praw
import pdb
from prawcore import NotFound as SubredditNotFound
import keys
from collections import Counter
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
    return redditors[0:limit]


def scrap_subreddits(redditors):
    total_subreddits = []
    n = len(redditors)
    for i, redditor in enumerate(redditors):
        print(f'Scraping {redditor.name:<10} {i+1}/{n:<10}', end='')
        user_subreddits = set()
        if not hasattr(redditor, 'is_suspended'):
            for comment in redditor.comments.new(limit=None):
                user_subreddits.add(comment.subreddit.display_name)
            for submission in redditor.submissions.new(limit=None):
                user_subreddits.add(submission.subreddit.display_name)
            print(f'Found {len(user_subreddits)} subreddits')
            total_subreddits.extend(list(user_subreddits))
        else:
            print('SUSPENDED')
    return total_subreddits


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
    common_subreddits = scrap_subreddits(redditors)
    subreddit_occurrences = Counter(common_subreddits).items()
    print(f'\n\nOutput saved at {SUBREDDIT_QUERY} - {USER_LIMIT}.csv')
    with open(f'{SUBREDDIT_QUERY} - {USER_LIMIT}.csv', 'w', encoding='utf-8') as file:
        file.write('Subreddit,Count\n')
        for sub_occur in subreddit_occurrences:
            file.write(f"{sub_occur[0]},{sub_occur[1]}\n")


if __name__ == "__main__":
    main()
