# This python script will convert an ascii ply point cloud to a colmap compatible point cloud format
# By Jeffrey Ian Wilson for the 3D Scanning Masterclass (www.jeffreyianwilson.com)

import sys
import numpy as np

# Define functions for reading PLY and writing COLMAP points3D

def read_ply_ascii(file_path):
    """
    Reads an ASCII PLY file and extracts the point cloud data.

    Args:
        file_path (str): Path to the PLY file.

    Returns:
        points (np.ndarray): Array of shape (N, 6) or (N, 3) containing point cloud data.
    """
    with open(file_path, 'r') as file:
        header = []
        while True:
            line = file.readline().strip()
            header.append(line)
            if line == "end_header":
                break

        # Parse header for format and property info
        has_color = False
        for line in header:
            if "property uchar" in line:
                has_color = True

        # Load points
        data = np.loadtxt(file)
        if has_color:
            return data[:, :6]  # x, y, z, r, g, b
        else:
            return data[:, :3]  # x, y, z

def write_colmap_points(points, output_path):
    """
    Writes a COLMAP-compatible points3D.txt file.

    Args:
        points (np.ndarray): Array of shape (N, 6) or (N, 3).
        output_path (str): Path to the output points3D.txt file.
    """
    with open(output_path, 'w') as file:
        for i, point in enumerate(points):
            x, y, z = point[:3]
            r, g, b = point[3:] if point.shape[0] > 3 else (0, 0, 0)
            track_id = -1  # No track info available
            file.write(f"{i + 1} {x:.6f} {y:.6f} {z:.6f} {r} {g} {b} {track_id}\n")

# Main conversion function
def convert_ply_to_colmap(ply_path, colmap_path):
    """
    Converts a PLY file to COLMAP points3D.txt format.

    Args:
        ply_path (str): Path to the input PLY file.
        colmap_path (str): Path to the output points3D.txt file.
    """
    points = read_ply_ascii(ply_path)
    write_colmap_points(points, colmap_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ply2colmap.py pointCloud.ply points3D.txt")
        sys.exit(1)

    ply_path = sys.argv[1]
    colmap_path = sys.argv[2]

    convert_ply_to_colmap(ply_path, colmap_path)
    print(f"Converted {ply_path} to COLMAP format at {colmap_path}")
