# import libraries
import cv2
from ultralytics import YOLO
import supervision as sv

video = cv2.VideoCapture(0)
# load the model
model = YOLO("yolov8n.pt")
bbox_annotator = sv.BoxAnnotator()

while True:
    ret, frame = video.read()
    # resize frame
    frame = cv2.resize(frame, (360, 240))
    results = model(frame)[0]
    detection = sv.Detections.from_yolov8(results)
    detection = detection[detection.confidence > 0.8]
    labels = [
        results.names[class_id]
        for class_id in detection.class_id
    ]
    frame = bbox_annotator.annotate(frame, detection, labels)
    cv2.imshow("Image", frame)
    cv2.waitKey(1)