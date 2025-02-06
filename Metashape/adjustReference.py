# This python script will adjust the pitch, roll, yaw angles defined by user input
# By Jeffrey Ian Wilson for the 3D Scanning Masterclass (www.jeffreyianwilson.com)

import pandas as pd

def adjust_camera_angles(input_file, output_file):
    # Load the data
    data = pd.read_csv(input_file, delimiter=' ')

    # Strip any leading/trailing spaces from column names
    data.columns = data.columns.str.strip()

    # Print column names for debugging
    print("Available columns:", data.columns.tolist())
    
    # Get user input for adjustments
    yaw_adjust = float(input("Enter adjustment value for yaw (z): "))
    pitch_adjust = float(input("Enter adjustment value for pitch (y): "))
    roll_adjust = float(input("Enter adjustment value for roll (x): "))
    
    # Apply user-defined adjustments
    if 'yaw(z)' in data.columns:
        data['yaw(z)'] = (data['yaw(z)'] + yaw_adjust) % 360
    if 'pitch(y)' in data.columns:
        data['pitch(y)'] = (data['pitch(y)'] + pitch_adjust) % 360
    if 'roll(x)' in data.columns:
        data['roll(x)'] = (data['roll(x)'] + roll_adjust) % 360
    
    if 'yaw' in data.columns:
        data['yaw'] = (data['yaw'] + yaw_adjust) % 360
    if 'pitch' in data.columns:
        data['pitch'] = (data['pitch'] + pitch_adjust) % 360
    if 'roll' in data.columns:
        data['roll'] = (data['roll'] + roll_adjust) % 360

    # Save the adjusted data to a new file
    data.to_csv(output_file, index=False)
    print(f"Adjusted data saved to {output_file}")

# Example usage
input_file = "reference.csv"  # Replace with your input file path
output_file = "reference_adjusted.csv"  # Replace with your desired output file path
adjust_camera_angles(input_file, output_file)

