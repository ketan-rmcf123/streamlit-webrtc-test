"""
Unit Tests for Streamlit WebRTC Studio.
"""

import os
import sys
import unittest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.processors import VideoTransformEngine, FilterMode
from core.ice import ICEManager


class TestVideoProcessors(unittest.TestCase):
    def setUp(self):
        self.engine = VideoTransformEngine()
        # Synthetic test frame
        self.frame = np.random.randint(0, 256, (120, 160, 3), dtype=np.uint8)

    def test_canny_filter(self):
        res = self.engine.apply_canny(self.frame)
        self.assertEqual(res.shape, self.frame.shape)

    def test_cartoon_filter(self):
        res = self.engine.apply_cartoon(self.frame)
        self.assertEqual(res.shape, self.frame.shape)

    def test_sepia_filter(self):
        res = self.engine.apply_sepia(self.frame)
        self.assertEqual(res.shape, self.frame.shape)

    def test_heatmap_filter(self):
        res = self.engine.apply_heatmap(self.frame)
        self.assertEqual(res.shape, self.frame.shape)

    def test_blur_filter(self):
        res = self.engine.apply_blur(self.frame, ksize=15)
        self.assertEqual(res.shape, self.frame.shape)

    def test_face_detection_pipeline(self):
        res = self.engine.apply_face_detection(self.frame)
        self.assertEqual(res.shape, self.frame.shape)

    def test_transform_router(self):
        for mode in FilterMode:
            out = self.engine.transform(self.frame, mode)
            self.assertEqual(out.shape, self.frame.shape)


class TestICEManager(unittest.TestCase):
    def test_ice_servers_fallback(self):
        servers = ICEManager.get_ice_servers(use_turn=True)
        self.assertIsInstance(servers, list)
        self.assertGreater(len(servers), 0)
        # Check structure
        self.assertIn("urls", servers[0])

    def test_diagnostics(self):
        diag = ICEManager.test_connectivity()
        self.assertIn("configured_servers_count", diag)
        self.assertGreaterEqual(diag["configured_servers_count"], 1)


if __name__ == "__main__":
    unittest.main()
