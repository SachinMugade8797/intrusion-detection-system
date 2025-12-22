# Configuration settings for the intrusion detection system

# Video source: 0 for webcam, or path to video file

VIDEO_SOURCE = "data/Video1.mp4"  # Change to 0 for webcam

## Frame processing
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Motion detection
BLUR_KERNEL = (21, 21)
MOTION_THRESHOLD = 25

# Contours
MIN_CONTOUR_AREA = 2500

# Bottom-left perimeter line
PERIMETER_LINE = (40, 430, 600, 430)

# Tracking
MAX_DISAPPEARED = 30
MAX_TRACKING_DISTANCE = 80


# Event cooldown per object (seconds)
EVENT_COOLDOWN = 3.0

# Backend API settings
API_URL = "http://localhost:5000/api/events"

# Database settings
DB_PATH = "data/events.db"

# Display settings
SHOW_FPS = True
LINE_THICKNESS = 3  # Thicker line for better visibility
FONT_SCALE = 0.7
FONT_THICKNESS = 2
ALERT_DURATION = 45  # Frames to show alert