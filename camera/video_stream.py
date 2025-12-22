import cv2
from config.settings import VIDEO_SOURCE, FRAME_WIDTH, FRAME_HEIGHT

class VideoStream:
    """Handles video input from webcam or video file"""
    
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {VIDEO_SOURCE}")
        
        # Set frame dimensions for webcam
        if VIDEO_SOURCE == 0:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        
        self.is_webcam = (VIDEO_SOURCE == 0)
        print(f"Video stream initialized: {'Webcam' if self.is_webcam else 'Video File'}")
    
    def read_frame(self):
        """Read a single frame from video source"""
        ret, frame = self.cap.read()
        
        # Handle video file end by looping
        if not ret and not self.is_webcam:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        
        return ret, frame
    
    def release(self):
        """Release video capture resources"""
        self.cap.release()
        print("Video stream released")
        