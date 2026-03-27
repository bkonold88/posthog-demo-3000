import time
import random
from datetime import datetime
import os
from posthog import Posthog

posthog = Posthog(os.getenv('PH_PROJECT_KEY'), host=os.getenv('PH_HOST'))

plans = ['Free', 'Premium', 'Max-imal']
search_queries = ['action', 'comedy', 'family', 'thriller', 'frozen', 'lion', 'adventure', 'drama']
users = [f'simuser_{i}@hogflix.com' for i in range(1, 101)]

def simulate_event():
    user = random.choice(users)
    event_type = random.choices(
        ['pageview', 'search', 'movie_view', 'signup', 'login', 'logout', 'plan_change'],
        weights=[40, 20, 20, 5, 8, 4, 3]
    )[0]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if event_type == 'pageview':
        posthog.capture(distinct_id=user, event='$pageview', properties={
            '$current_url': random.choice([
                'http://localhost:5000/',
                'http://localhost:5000/plans',
                'http://localhost:5000/blog',
                'http://localhost:5000/profile'
            ])
        })
    elif event_type == 'search':
        posthog.capture(distinct_id=user, event='search_performed', properties={
            'query': random.choice(search_queries)
        })
    elif event_type == 'movie_view':
        posthog.capture(distinct_id=user, event='$pageview', properties={
            '$current_url': f'http://localhost:5000/movie/{random.randint(1, 20)}'
        })
    elif event_type == 'signup':
        plan = random.choice(plans)
        posthog.capture(distinct_id=user, event='user_signed_up', properties={
            'plan': plan, 'date_time': now
        })
        posthog.capture(distinct_id=user, event='subscription_purchased', properties={
            'plan': plan,
            'months': 1,
            'price': int({'Free': 0, 'Premium': 9.99, 'Max-imal': 19.99}[plan] * 100),
            'currency': 'USD'
        })
    elif event_type == 'login':
        posthog.capture(distinct_id=user, event='user_logged_in', properties={
            'date_time': now
        })
    elif event_type == 'logout':
        posthog.capture(distinct_id=user, event='user_logged_out', properties={
            'date_time': now
        })
    elif event_type == 'plan_change':
        posthog.capture(distinct_id=user, event='plan_changed', properties={
            'new_plan': random.choice(plans), 'date_time': now
        })

    print(f"[{now}] Captured '{event_type}' for {user}")

print("Starting activity simulation...")
for i in range(50):
    simulate_event()
    time.sleep(2)
print("Simulation complete!")
posthog.shutdown()
