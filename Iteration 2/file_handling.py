import csv
# Combine and write to CSV
def create_csv(player_times, computer_times):
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Checkpoint Number','Player', 'Computer'])  # Optional header
        for i ,(a, b) in enumerate(zip(player_times, computer_times)):
            writer.writerow([i+1, a, b])

player_times = [1.2, 2.5, 3.8]
computer_times = [1.0, 2.3, 3.6]
create_csv(player_times, computer_times)
