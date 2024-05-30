from datetime import datetime, timedelta

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

# Function to find the next special event
def find_next_special_event(local_current_time):
    # Adjust current time to the UK time zone (subtract 2 hours)
    uk_current_time = local_current_time - timedelta(hours=2)

    # Create the schedule for the next 24 hours based on the UK current time
    schedule = []
    start_time = uk_current_time.replace(minute=0, second=0, microsecond=0)

    for i in range(24):
        event_time = start_time + timedelta(hours=i)
        event = rotation_full[event_time.hour % len(rotation_full)]
        schedule.append((event_time, event))

    # Filter out special events
    special_events = [
        (time, event) for time, event in schedule if "Special" in event[0]
    ]

    # Find the next special event
    for event_time, event in special_events:
        if event_time > uk_current_time:
            # Adjust event time back to the user's local time (add 2 hours)
            local_event_time = event_time + timedelta(hours=2)
            return local_event_time, event

    # If no future special events in the next 24 hours, consider the schedule loop
    first_event_time, first_event = special_events[0]
    local_first_event_time = first_event_time + timedelta(hours=2)
    return local_first_event_time, first_event
