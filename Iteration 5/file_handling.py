import csv
import datetime
import os
from itertools import zip_longest

# Combine and write to CSV
def create_csv(track_name, player_times, computer_times):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{track_name}_results_{timestamp}.csv"
    directory = "Checkpoint data"

    file_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Checkpoint Number','Player', 'Computer','Gap'])  # Optional header


        for i, (a, b) in enumerate(zip_longest(player_times, computer_times)):
            if a is None and b is not None:
                writer.writerow([i+1, 'N/A', b, 'N/A'])
            elif b is None and a is not None:
                writer.writerow([i+1, a, 'N/A', 'N/A'])
            else:
                writer.writerow([i+1, a, b, round(a-b),3])


# For testing purposes

# player_times = [1.2, 2.5, 3.8, None]
# computer_times = [1.0, 2.3, 3.6, 5]
# create_csv("test", player_times, computer_times)
