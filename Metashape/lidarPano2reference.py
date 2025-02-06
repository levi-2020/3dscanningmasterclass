# This python script will export lidar panorama positions to a reference file
# By Jeffrey Ian Wilson for the 3D Scanning Masterclass (www.jeffreyianwilson.com)

import Metashape
import math

def rotation_matrix_to_ypr(R):
    """
    Convert a 3x3 rotation matrix R into yaw, pitch, roll angles (in degrees).
    Assuming a Z-Y'-X'' convention:
    Yaw: rotation about Z
    Pitch: rotation about Y'
    Roll: rotation about X''

    This is one common interpretation:
    Yaw   = atan2(R[1,0], R[0,0])
    Pitch = -asin(R[2,0])
    Roll  = atan2(R[2,1], R[2,2])

    Note: Ensure the signs and the angle extraction match your desired convention.
    """
    # R is Metashape.Matrix object, convert to list or use direct indexing:
    r00, r01, r02 = R[0,0], R[0,1], R[0,2]
    r10, r11, r12 = R[1,0], R[1,1], R[1,2]
    r20, r21, r22 = R[2,0], R[2,1], R[2,2]

    # Compute angles in radians
    yaw = math.degrees(math.atan2(r10, r00))
    pitch = math.degrees(-math.asin(r20))
    roll = math.degrees(math.atan2(r21, r22))

    return yaw, pitch, roll

# Get current document and chunk
doc = Metashape.app.document
chunk = doc.chunk

# Ensure that chunk.crs is defined (coordinate system from LiDAR)
if not chunk.crs:
    print("No coordinate system defined for the chunk. Please set a CRS before running this script.")
    raise SystemExit

# For each camera (panorama), we want to set its reference location and rotation
for camera in chunk.cameras:
    if not camera.transform:
        # If camera is not aligned or no transform is available, skip
        continue
    
    # Extract camera center in chunk coordinates
    # camera.center returns camera position in chunk internal coordinates
    camera_center = camera.center
    # Convert to georeferenced coordinates
    camera_coord = chunk.crs.project(chunk.transform.matrix.mulp(camera_center))

    # Extract rotation matrix from camera.transform
    # camera.transform is a 4x4 matrix. The top-left 3x3 part is rotation.
    R = Metashape.Matrix([[camera.transform[0,0], camera.transform[0,1], camera.transform[0,2]],
                          [camera.transform[1,0], camera.transform[1,1], camera.transform[1,2]],
                          [camera.transform[2,0], camera.transform[2,1], camera.transform[2,2]]])

    yaw, pitch, roll = rotation_matrix_to_ypr(R)

    # Set camera reference
    camera.reference.location = Metashape.Vector(camera_coord)
    camera.reference.rotation = Metashape.Vector([yaw, pitch, roll])
