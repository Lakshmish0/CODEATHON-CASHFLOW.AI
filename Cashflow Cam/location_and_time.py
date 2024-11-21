from PIL import Image
from exif import Image as ExifImage


def extract_metadata(image_path):
    try:
        # Open the image file
        with open(image_path, 'rb') as img_file:
            img = ExifImage(img_file)

        # Check if EXIF data exists
        if not img.has_exif:
            print("No EXIF metadata found.")
            return

        # Extract metadata
        metadata = {}
        metadata['Capture Time'] = img.datetime if 'datetime' in img.list_all() else "Not Available"

        # Extract GPS data if available
        if 'gps_latitude' in img.list_all() and 'gps_longitude' in img.list_all():
            lat = img.gps_latitude
            lat_ref = img.gps_latitude_ref
            lon = img.gps_longitude
            lon_ref = img.gps_longitude_ref
            metadata['GPS Coordinates'] = convert_gps(lat, lat_ref, lon, lon_ref)
        else:
            metadata['GPS Coordinates'] = "Not Available"

        # Print metadata
        for key, value in metadata.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")


def convert_gps(lat, lat_ref, lon, lon_ref):
    """Convert GPS coordinates to decimal format."""
    lat_deg = lat[0] + lat[1] / 60 + lat[2] / 3600
    if lat_ref != 'N':
        lat_deg = -lat_deg

    lon_deg = lon[0] + lon[1] / 60 + lon[2] / 3600
    if lon_ref != 'E':
        lon_deg = -lon_deg

    return f"{lat_deg}, {lon_deg}"


# Usage
image_path = "test.jpg"  # Replace with your image path
extract_metadata(image_path)
