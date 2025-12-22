import cv2
from config.settings import MIN_CONTOUR_AREA

class ContourProcessor:
    """Processes contours and calculates centroids"""
    
    def find_contours(self, motion_mask):
        """Find contours in motion mask"""
        contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def filter_contours(self, contours):
        """Filter contours by minimum area"""
        valid_contours = [c for c in contours if cv2.contourArea(c) >= MIN_CONTOUR_AREA]
        return valid_contours
    
    def calculate_centroid(self, contour):
        """Calculate centroid (cx, cy) of a contour"""
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return None
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)
    
    def get_centroids(self, motion_mask):
        """Get all valid centroids from motion mask"""
        contours = self.find_contours(motion_mask)
        valid_contours = self.filter_contours(contours)
        
        centroids = []
        for contour in valid_contours:
            centroid = self.calculate_centroid(contour)
            if centroid:
                centroids.append(centroid)
        
        return centroids, valid_contours