import csv

def write_csv_file(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["time", "x", "y", "vx", "vy", "heading", "label", "object_type"])
        writer.writerows(data)

def generate_trajectory_data(vehicles, num_steps):
    data = []
    for i, vehicle in enumerate(vehicles):
        for k in range(1, num_steps):
            x = vehicle.states[k].position
            vx = vehicle.states[k].velocity
            label = f"traj_{i}"
            object_type = vehicle.type
            data.append([k, x, 0, vx, 0, 0, label, object_type])
    return data