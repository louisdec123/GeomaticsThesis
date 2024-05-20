import ezdxf
import csv
from scipy.spatial.distance import cdist
import numpy as np

def extract_dxf_data(filepath):
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()

    # Lists to store Trench Labels and their positions
    trench_labels = []
    trench_positions = []

    # List to store cleaned Cable information
    cable_info_cleaned = []
    cable_positions = []

    # Extract Trench Labels from B-PR-PROFIELNR layer
    for text in msp.query('TEXT[layer=="B-PR-PROFIELNR"]'):
        label = text.dxf.text.split()[0]  # First word of the text content
        position = text.dxf.insert
        trench_labels.append(label)
        trench_positions.append([position.x, position.y])

    # Extract and clean Cable Information from B-NW-MAATVOERING layer
    for mtext in msp.query('MTEXT[layer=="B-NW-MAATVOERING"]'):
        info = mtext.text.replace('^I', ' ').strip()  # Clean the text
        position = mtext.dxf.insert
        cable_info_cleaned.append(info)
        cable_positions.append([position.x, position.y])

    # Find the nearest trench label for each cable
    trench_positions_np = np.array(trench_positions)
    cable_positions_np = np.array(cable_positions)
    distances = cdist(cable_positions_np, trench_positions_np, 'euclidean')
    nearest_trench_indices = np.argmin(distances, axis=1)
    nearest_trench_labels = [trench_labels[index] for index in nearest_trench_indices]

    # Splitting cable information into distance, height, and description
    cable_data_split = []
    for info in cable_info_cleaned:
        parts = info.split(maxsplit=2)
        if len(parts) > 2 and '-' in parts[2]:  # Has description with dash
            description_parts = parts[2].split(' - ', 1)
            if len(description_parts) == 2:
                parts[2] = description_parts[1]  # Replace with just the description
        cable_data_split.append(parts)

    # Combine nearest trench label with split cable information
    combined_data = []
    for trench_label, cable_data in zip(nearest_trench_labels, cable_data_split):
        if len(cable_data) == 3:  # Has description
            distance, height, description = cable_data
        else:  # No description, just distance and height
            distance, height = cable_data
            description = ''
        combined_data.append([trench_label, distance, height, description])

    return combined_data


def write_to_csv(filepath, data):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Trench Label', 'Distance', 'Height', 'Description'])
        writer.writerows(data)


# Replace 'filepath' with the path to your DXF file
dxf_filepath = "C:/Users/louis/Desktop/Thesis/Rotterdam/Levering_Graafprofielen_TU/Profiel 1 tm 114.dxf"
combined_data = extract_dxf_data(dxf_filepath)

# Specify the CSV file path where you want to save the output
csv_filepath = "C:/Users/louis/Desktop/Thesis/extracted_cable_info.csv"
write_to_csv(csv_filepath, combined_data)
