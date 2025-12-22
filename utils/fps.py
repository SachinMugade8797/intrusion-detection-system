import time

class FPSCounter:
    """Calculates and tracks frames per second"""
    
    def __init__(self):
        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0
    
    def update(self):
        """Update FPS calculation"""
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        
        # Update FPS every second
        if elapsed > 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = time.time()
    
    def get_fps(self):
        """Get current FPS value"""
        return int(self.fps)