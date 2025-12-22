import cv2
import requests
import threading
from camera.video_stream import VideoStream
from processing.motion_detector import MotionDetector
from processing.contour_utils import ContourProcessor
from processing.intrusion_logic import IntrusionDetector
from utils.event import Event
from utils.fps import FPSCounter
from backend.api import run_api
from config.settings import (API_URL, PERIMETER_LINE, SHOW_FPS, 
                              FONT_SCALE, FONT_THICKNESS, LINE_THICKNESS, ALERT_DURATION)

def send_event_to_api(event):
    """Send event to backend API"""
    try:
        response = requests.post(API_URL, json=event, timeout=2)
        if response.status_code == 200:
            print(f"[OK] Event sent: {event['event_type']} at {event['timestamp']}")
        else:
            print(f"[ERROR] Failed to send event: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[WARNING] API connection error: {e}")

def draw_perimeter(frame):
    """Draw virtual perimeter line on frame"""
    x1, y1, x2, y2 = PERIMETER_LINE
    # Draw thick red line
    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), LINE_THICKNESS)
    # Add label with background
    label = "DO NOT CROSS"
    (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_THICKNESS)
    cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w + 10, y1), (0, 0, 255), -1)
    cv2.putText(frame, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                FONT_SCALE, (255, 255, 255), FONT_THICKNESS)

def draw_tracked_objects(frame, objects):
    """Draw tracked objects with IDs"""
    for object_id, centroid in objects.items():
        # Draw centroid as large circle
        cx, cy = int(centroid[0]), int(centroid[1])
        cv2.circle(frame, (cx, cy), 8, (0, 255, 255), -1)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), 2)
        
        # Draw object ID
        text = f"ID: {object_id}"
        cv2.putText(frame, text, (cx - 30, cy - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 255), 2)

def draw_contours(frame, contours):
    """Draw detected motion contours"""
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

def draw_fps(frame, fps):
    """Draw FPS counter on frame"""
    fps_text = f"FPS: {fps}"
    cv2.rectangle(frame, (5, 5), (120, 40), (0, 0, 0), -1)
    cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)

def draw_intrusion_alert(frame, object_id):
    """Draw intrusion alert banner"""
    h, w = frame.shape[:2]
    # Draw red banner at top
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 0, 255), -1)
    cv2.rectangle(frame, (0, 0), (w, 80), (255, 255, 255), 3)
    
    # Alert text
    alert_text = "!!! INTRUSION DETECTED !!!"
    (text_w, text_h), _ = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
    cv2.putText(frame, alert_text, ((w - text_w) // 2, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    
    # Object ID
    id_text = f"Object #{object_id} crossed perimeter"
    (id_w, id_h), _ = cv2.getTextSize(id_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    cv2.putText(frame, id_text, ((w - id_w) // 2, 65), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

def draw_status(frame, motion_detected, objects_count):
    """Draw system status"""
    h, w = frame.shape[:2]
    # Status background
    cv2.rectangle(frame, (w - 280, 5), (w - 5, 85), (0, 0, 0), -1)
    cv2.rectangle(frame, (w - 280, 5), (w - 5, 85), (255, 255, 255), 2)
    
    # Motion status
    motion_status = "Motion: YES" if motion_detected else "Motion: NO"
    motion_color = (0, 255, 0) if motion_detected else (100, 100, 100)
    cv2.putText(frame, motion_status, (w - 270, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, motion_color, 2)
    
    # Objects tracked
    obj_text = f"Tracking: {objects_count} objects"
    cv2.putText(frame, obj_text, (w - 270, 55), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Instructions
    cv2.putText(frame, "Press 'Q' to quit", (w - 270, 75), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

def main():
    """Main application loop"""
    # Start Flask API in separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Initialize components
    video_stream = VideoStream()
    motion_detector = MotionDetector()
    contour_processor = ContourProcessor()
    intrusion_detector = IntrusionDetector()
    fps_counter = FPSCounter()
    
    print("\n" + "="*60)
    print("VIRTUAL PERIMETER INTRUSION DETECTION SYSTEM")
    print("="*60)
    print("Video Source: Initialized")
    print("API Server: Running on http://localhost:5000")
    print("Perimeter Line: Active")
    print("Press 'Q' to quit")
    print("="*60 + "\n")
    
    alert_frames_remaining = 0
    alert_object_id = None
    
    try:
        while True:
            # Read frame from video source
            ret, frame = video_stream.read_frame()
            if not ret:
                print("[WARNING] End of video or camera disconnected")
                break
            
            # Detect motion
            motion_mask = motion_detector.detect(frame)
            motion_detected = False
            
            if motion_mask is not None:
                # Find contours and centroids
                centroids, contours = contour_processor.get_centroids(motion_mask)
                motion_detected = len(centroids) > 0
                
                # Update intrusion detector with centroids
                intrusion, objects, crossed_id = intrusion_detector.update(centroids)
                
                # If intrusion detected, create and send event
                if intrusion:
                    event = Event.create_intrusion_event()
                    send_event_to_api(event)
                    alert_frames_remaining = ALERT_DURATION
                    alert_object_id = crossed_id
                
                # Draw visualizations
                draw_contours(frame, contours)
                draw_tracked_objects(frame, objects)
            else:
                # Still update tracker even without new detections
                intrusion_detector.update([])
            
            # Draw perimeter line (always visible)
            draw_perimeter(frame)
            
            # Show intrusion alert if active
            if alert_frames_remaining > 0:
                draw_intrusion_alert(frame, alert_object_id)
                alert_frames_remaining -= 1
            
            # Draw status info
            objects_count = len(intrusion_detector.tracker.objects)
            draw_status(frame, motion_detected, objects_count)
            
            # Update and draw FPS
            fps_counter.update()
            if SHOW_FPS:
                draw_fps(frame, fps_counter.get_fps())
            
            # Display frame
            cv2.imshow('Intrusion Detection System', frame)
            
            # Exit on 'q' or 'Q' key
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                print("\n[STOP] Stopping system...")
                break
    
    except KeyboardInterrupt:
        print("\n[WARNING] Interrupted by user")
    
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
    
    finally:
        # Cleanup
        video_stream.release()
        cv2.destroyAllWindows()
        print("[OK] System stopped successfully\n")

if __name__ == "__main__":
    main()