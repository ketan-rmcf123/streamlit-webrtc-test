"""
Real-time Video and Audio Stream Processing Filters.
"""

from enum import Enum
from typing import Optional, Tuple
import cv2
import numpy as np


class FilterMode(str, Enum):
    PASSTHROUGH = "Original Feed"
    CANNY_EDGES = "Edge Detection (Canny)"
    CARTOON = "Cartoonizer"
    SEPIA = "Vintage Sepia"
    HEATMAP = "Color Inversion & Heatmap"
    GAUSSIAN_BLUR = "Privacy Blur"
    FACE_DETECTION = "Face Landmark Bounding Box"


class VideoTransformEngine:
    """Core image processing algorithms applicable to single frames or WebRTC streams."""

    def __init__(self) -> None:
        self.face_cascade = None
        if hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def apply_canny(self, frame: np.ndarray, thresh1: int = 100, thresh2: int = 200) -> np.ndarray:
        """Convert frame to high-contrast Canny edges."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, thresh1, thresh2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def apply_cartoon(self, frame: np.ndarray) -> np.ndarray:
        """Artistic cartoon effect combining bilateral smoothing and sketch edges."""
        # 1. Edge extraction
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )
        # 2. Color quantization via bilateral filtering
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        # 3. Combine
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        return cartoon

    def apply_sepia(self, frame: np.ndarray) -> np.ndarray:
        """Classic vintage warm sepia tone."""
        sepia_matrix = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        transformed = cv2.transform(frame, sepia_matrix)
        return np.clip(transformed, 0, 255).astype(np.uint8)

    def apply_heatmap(self, frame: np.ndarray) -> np.ndarray:
        """False-color thermal heatmap visualization."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    def apply_blur(self, frame: np.ndarray, ksize: int = 31) -> np.ndarray:
        """Gaussian privacy blur."""
        k = ksize if ksize % 2 == 1 else ksize + 1
        return cv2.GaussianBlur(frame, (k, k), 0)

    def apply_face_detection(self, frame: np.ndarray) -> np.ndarray:
        """Detect and annotate faces in the frame."""
        output = frame.copy()
        if self.face_cascade is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 120), 2)
                line_len = int(w * 0.2)
                cv2.line(output, (x, y), (x + line_len, y), (0, 255, 120), 4)
                cv2.line(output, (x, y), (x, y + line_len), (0, 255, 120), 4)
                cv2.putText(
                    output, "FACE DETECTED", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 120), 1, cv2.LINE_AA
                )
        else:
            # Subtle center focus viewport
            h, w = frame.shape[:2]
            cx, cy = w // 2, h // 2
            bx, by = int(w * 0.2), int(h * 0.2)
            cv2.rectangle(output, (cx - bx, cy - by), (cx + bx, cy + by), (0, 255, 120), 1)
            cv2.putText(
                output, "AI VIEWPORT READY", (cx - bx, cy - by - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 120), 1, cv2.LINE_AA
            )
        return output

    def transform(self, frame: np.ndarray, mode: FilterMode) -> np.ndarray:
        """Route frame to requested filter."""
        if mode == FilterMode.CANNY_EDGES:
            return self.apply_canny(frame)
        elif mode == FilterMode.CARTOON:
            return self.apply_cartoon(frame)
        elif mode == FilterMode.SEPIA:
            return self.apply_sepia(frame)
        elif mode == FilterMode.HEATMAP:
            return self.apply_heatmap(frame)
        elif mode == FilterMode.GAUSSIAN_BLUR:
            return self.apply_blur(frame)
        elif mode == FilterMode.FACE_DETECTION:
            return self.apply_face_detection(frame)
        return frame
