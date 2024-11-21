from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO('yolov8n.pt')  # Use 'yolov8n.pt' for the smallest model; can replace with 'yolov8s.pt' or others

# Load the image
image_path = "/home/greatness-within/PycharmProjects/LoanAproval/crowd.jpg"
image = cv2.imread(image_path)

# Run YOLO detection
results = model(image)

# Extract bounding boxes and class labels
detections = results[0].boxes.data  # Get all detections (bounding boxes, confidence, class)
person_count = 0

# Iterate through detections to count "person" class (class id = 0)
for detection in detections:
    class_id = int(detection[5])  # Last column is the class ID
    if class_id == 0:  # Class ID 0 corresponds to "person"
        person_count += 1

# Print the number of people
print(f"Number of people detected: {person_count}")

# Optional: Display the image with detections
annotated_image = results[0].plot()

