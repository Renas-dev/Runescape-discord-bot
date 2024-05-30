from datetime import datetime, timedelta

# Define the provided rotation with all events in UK time zone
rotation_full = [
    ("Infernal Star (Special)", 0),
    ("Lost Souls", 1),
    ("Ramokee Incursion", 2),
    ("Displaced Energy", 3),
    ("Evil Bloodwood Tree (Special)", 4),
    ("Spider Swarm", 5),
    ("Unnatural Outcrop", 6),
    ("Stryke the Wyrm (Special)", 7),
    ("Demon Stragglers", 8),
    ("Butterfly Swarm", 9),
    ("King Black Dragon Rampage (Special)", 10),
    ("Forgotten Soldiers", 11),
    ("Surprising Seedlings", 22),
    ("Hellhound Pack", 23),
]


# Function to get the special events for the next 24 hours
def get_special_events_for_day(local_current_time):
    # Adjust current time to the UK time zone (subtract 2 hours)
    uk_current_time = local_current_time - timedelta(hours=2)

    # Create the schedule for the next 24 hours based on the UK current time
    schedule = []
    start_time = uk_current_time.replace(minute=0, second=0, microsecond=0)

    for i in range(24):
        event_time = start_time + timedelta(hours=i)
        event = rotation_full[event_time.hour % len(rotation_full)]
        schedule.append((event_time, event))

    # Filter out special events and adjust their times back to the user's local time (add 2 hours)
    special_events = [
        (time + timedelta(hours=2), event)
        for time, event in schedule
        if "Special" in event[0]
    ]

    return special_events


# Get the current time
current_time = datetime.now()

# Get the special events for the next 24 hours
special_events_for_day = get_special_events_for_day(current_time)

# Print the special events for the day
print("Special events for the next 24 hours:")
for event_time, event in special_events_for_day:
    print(f"{event_time.strftime('%Y-%m-%d %H:%M:%S')} - {event[0]}")

# Example output:
# Special events for the next 24 hours:
# 2024-05-30 02:00:00 - Infernal Star (Special)
# 2024-05-30 04:00:00 - Evil Bloodwood Tree (Special)
# ...
