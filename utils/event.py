from datetime import datetime

class Event:
    """Represents a detection event"""
    
    @staticmethod
    def create_intrusion_event():
        """Create intrusion detection event"""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "intrusion_detected",
            "value": 1
        }
    
    @staticmethod
    def create_motion_event(motion_intensity):
        """Create motion detection event with intensity"""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": "motion_detected",
            "value": motion_intensity
        }
        