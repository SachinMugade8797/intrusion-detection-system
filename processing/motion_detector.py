import cv2
import numpy as np
from config.settings import BLUR_KERNEL, MOTION_THRESHOLD

class MotionDetector:
    """Detects motion between consecutive frames"""
    
    def __init__(self):
        self.prev_frame = None
    
    def preprocess_frame(self, frame):
        """Convert frame to grayscale and apply blur"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, BLUR_KERNEL, 0)
        return blurred
    
    def detect(self, frame):
        """Detect motion and return motion mask"""
        processed = self.preprocess_frame(frame)
        
        # Initialize previous frame on first call
        if self.prev_frame is None:
            self.prev_frame = processed
            return None
        
        # Calculate absolute difference between frames
        frame_diff = cv2.absdiff(self.prev_frame, processed)
        
        # Apply threshold to get binary motion mask
        _, motion_mask = cv2.threshold(frame_diff, MOTION_THRESHOLD, 255, cv2.THRESH_BINARY)
        
        # Dilate to fill gaps in motion regions
        motion_mask = cv2.dilate(motion_mask, None, iterations=2)
        
        # Update previous frame
        self.prev_frame = processed
        
        return motion_mask