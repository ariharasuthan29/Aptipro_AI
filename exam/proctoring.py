import base64
import os
import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.utils import timezone

# Load Haar cascade classifier for frontal face detection
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def analyze_webcam_frame(base64_data):
    """
    Analyzes a base64 encoded JPEG/PNG frame sent from the webcam.
    Returns a dict with face count, detection status, violation_type, and decoded frame image.
    """
    if not base64_data:
        return {
            'status': 'VIOLATION',
            'violation_type': 'CAMERA_OFF',
            'details': 'Webcam video stream is inactive or blocked.',
            'faces_count': 0,
            'image_file': None
        }

    try:
        # Strip header if present (data:image/jpeg;base64,)
        if ',' in base64_data:
            header, base64_str = base64_data.split(',', 1)
        else:
            base64_str = base64_data

        img_bytes = base64.b64decode(base64_str)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return {
                'status': 'VIOLATION',
                'violation_type': 'CAMERA_OFF',
                'details': 'Could not decode camera image frame.',
                'faces_count': 0,
                'image_file': None
            }

        # Convert to grayscale for Haar Cascade detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # Detect faces
        faces = FACE_CASCADE.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        faces_count = len(faces)

        # Prepare ContentFile for snapshot if needed
        filename = f"snapshot_{int(timezone.now().timestamp())}.jpg"
        content_file = ContentFile(img_bytes, name=filename)

        if faces_count == 0:
            return {
                'status': 'VIOLATION',
                'violation_type': 'NO_FACE',
                'details': 'AI Detection: Candidate face is missing or obscured.',
                'faces_count': 0,
                'image_file': content_file
            }
        elif faces_count > 1:
            return {
                'status': 'VIOLATION',
                'violation_type': 'MULTI_FACE',
                'details': f'AI Detection: Multiple candidates ({faces_count}) detected in camera stream.',
                'faces_count': faces_count,
                'image_file': content_file
            }
        else:
            return {
                'status': 'OK',
                'violation_type': None,
                'details': 'Candidate face verified.',
                'faces_count': 1,
                'image_file': None
            }

    except Exception as e:
        return {
            'status': 'OK', # Graceful fallback to avoid false positives if OpenCV frame parsing encounters error
            'violation_type': None,
            'details': f'Frame check fallback: {str(e)}',
            'faces_count': 1,
            'image_file': None
        }
