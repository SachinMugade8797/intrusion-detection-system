import time
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict
from config.settings import PERIMETER_LINE, EVENT_COOLDOWN, MAX_DISAPPEARED, MAX_TRACKING_DISTANCE

class CentroidTracker:
    """Tracks objects using centroid tracking algorithm"""
    
    def __init__(self):
        self.next_object_id = 0
        self.objects = OrderedDict()  # Object ID -> centroid
        self.disappeared = OrderedDict()  # Object ID -> frames disappeared
        self.prev_positions = OrderedDict()  # Object ID -> previous centroid
    
    def register(self, centroid):
        """Register new object with unique ID"""
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.prev_positions[self.next_object_id] = centroid
        self.next_object_id += 1
    
    def deregister(self, object_id):
        """Remove object from tracking"""
        del self.objects[object_id]
        del self.disappeared[object_id]
        if object_id in self.prev_positions:
            del self.prev_positions[object_id]
    
    def update(self, input_centroids):
        """Update tracked objects with new centroids"""
        # If no centroids detected, mark all as disappeared
        if len(input_centroids) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > MAX_DISAPPEARED:
                    self.deregister(object_id)
            return self.objects
        
        # Convert to numpy array
        input_centroids = np.array(input_centroids)
        
        # If no existing objects, register all
        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            # Get current object IDs and centroids
            object_ids = list(self.objects.keys())
            object_centroids = np.array(list(self.objects.values()))
            
            # Calculate distance between each pair
            D = dist.cdist(object_centroids, input_centroids)
            
            # Find minimum distances
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            # Track which rows/cols used
            used_rows = set()
            used_cols = set()
            
            # Match existing objects to new centroids
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                # Check if distance is reasonable
                if D[row, col] > MAX_TRACKING_DISTANCE:
                    continue
                
                object_id = object_ids[row]
                self.prev_positions[object_id] = self.objects[object_id]  # Store previous
                self.objects[object_id] = input_centroids[col]  # Update current
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Handle disappeared objects
            unused_rows = set(range(D.shape[0])) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > MAX_DISAPPEARED:
                    self.deregister(object_id)
            
            # Register new objects
            unused_cols = set(range(D.shape[1])) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col])
        
        return self.objects


class IntrusionDetector:
    """Detects intrusions when objects cross virtual perimeter"""
    
    def __init__(self):
        self.tracker = CentroidTracker()
        self.crossed_objects = set()  # Objects that already crossed
        self.last_event_time = {}  # Object ID -> last event time
        self.line_y = PERIMETER_LINE[1]  # Horizontal line Y coordinate
    
    def check_line_cross(self, object_id, prev_centroid, curr_centroid):
        """Check if object crossed the line"""
        prev_y = prev_centroid[1]
        curr_y = curr_centroid[1]
        
        # Check if crossed from either direction
        crossed = (prev_y < self.line_y and curr_y >= self.line_y) or \
                  (prev_y > self.line_y and curr_y <= self.line_y)
        
        # Check cooldown for this specific object
        current_time = time.time()
        if object_id in self.last_event_time:
            time_since_last = current_time - self.last_event_time[object_id]
            if time_since_last < EVENT_COOLDOWN:
                return False
        
        if crossed:
            self.last_event_time[object_id] = current_time
            return True
        
        return False
    
    def update(self, centroids):
        """Update tracking and check for intrusions"""
        # Update tracker with new centroids
        objects = self.tracker.update(centroids)
        
        intrusion_detected = False
        crossed_object_id = None
        
        # Check each tracked object for line crossing
        for object_id, centroid in objects.items():
            if object_id in self.tracker.prev_positions:
                prev_centroid = self.tracker.prev_positions[object_id]
                
                # Check if this object crossed the line
                if self.check_line_cross(object_id, prev_centroid, centroid):
                    intrusion_detected = True
                    crossed_object_id = object_id
                    print(f"[ALERT] Object #{object_id} crossed the perimeter!")
                    break
        
        return intrusion_detected, objects, crossed_object_id