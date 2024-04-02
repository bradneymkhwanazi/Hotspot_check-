import numpy as np
import matplotlib.pyplot as plt

# Defining The Parameters
area_size = 10  # in km
num_hotspots = 5000
min_distance = 10  # in m
interference_distance = 350  # in m
num_channels = 5

# Generating random hotspot locations
hotspot_locations = np.random.rand(num_hotspots, 2) * area_size

# Ensuring minimum distance between hotspots
for i in range(1, num_hotspots):
    for j in range(0, i):
        distance = np.linalg.norm(hotspot_locations[i] - hotspot_locations[j])
        if distance < min_distance:
            direction = hotspot_locations[i] - hotspot_locations[j]
            direction /= np.linalg.norm(direction)
            hotspot_locations[i] += (min_distance - distance) * direction

# Randomly Assigning Channels To Hotspots
hotspot_channels = np.random.randint(0, num_channels, num_hotspots)

# Function to check interference between hotspots
def check_interference(hotspot1, hotspot2):
    distance = np.linalg.norm(hotspot1 - hotspot2)
    return distance < interference_distance

# Initialize interference count
interference_count = np.zeros(num_hotspots)

# Calculate interference count for each hotspot
for i in range(num_hotspots):
    for j in range(num_hotspots):
        if i != j and hotspot_channels[i] == hotspot_channels[j]:
            if check_interference(hotspot_locations[i], hotspot_locations[j]):
                interference_count[i] += 1

# Find hotspots with the most interference
most_interfered = np.argsort(interference_count)[-10:]

# Change frequencies to minimize interference
for hotspot_index in most_interfered:
    min_interference = interference_count[hotspot_index]
    for channel in range(num_channels):
        if channel != hotspot_channels[hotspot_index]:
            interference = 0
            for i in range(num_hotspots):
                if hotspot_channels[i] == channel and check_interference(hotspot_locations[hotspot_index], hotspot_locations[i]):
                    interference += 1
            if interference < min_interference:
                min_interference = interference
                hotspot_channels[hotspot_index] = channel

# Plot the hotspots
channel_colors = ['b', 'g', 'r', 'c', 'm']
for i in range(num_hotspots):
    color = channel_colors[hotspot_channels[i]]
    if i in most_interfered:
        plt.scatter(hotspot_locations[i, 0], hotspot_locations[i, 1], color=color, edgecolors='r', linewidths=1)
    else:
        plt.scatter(hotspot_locations[i, 0], hotspot_locations[i, 1], color=color, edgecolors='k', linewidths=1)

plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.title('Hotspot Locations')
plt.grid(True)
plt.show()
