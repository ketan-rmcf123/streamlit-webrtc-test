# 📡 Streamlit WebRTC & Computer Vision Studio

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://img.shields.io/badge/Interface-Streamlit-red.svg)](https://streamlit.io)
[![WebRTC](https://img.shields.io/badge/WebRTC-PeerConnection-orange.svg)](https://webrtc.org)
[![Tests: Passing](https://img.shields.io/badge/Tests-9%20Passed-brightgreen.svg)]()

> High-performance WebRTC real-time media streaming studio built with **Streamlit**, **OpenCV**, and **streamlit-webrtc**, featuring live video filters, snapshot lab, and ICE / STUN / TURN NAT-traversal network diagnostics.

---

## 🌟 Key Features

- **🎥 Low-Latency Real-Time WebRTC Streaming**:
  - Bi-directional browser-to-server media pipeline using WebRTC PeerConnection.
  - Asynchronous frame processing with zero browser UI lag.
- **🎨 Real-Time Computer Vision Filters**:
  - **Edge Detection**: High-contrast Canny gradient contour extraction.
  - **Artistic Cartoonizer**: Bilateral color smoothing combined with adaptive edge sketches.
  - **Vintage Sepia**: Matrix-transformed nostalgic warmth.
  - **Thermal Heatmap**: False-color JET colormap luminance visualization.
  - **Privacy Blur**: Gaussian blur for meeting privacy.
  - **Face Detection**: Real-time facial region scanning and bounding annotations.
- **📸 Snapshot & Filter Lab**:
  - Instant high-res photo capture with one-click PNG filter export.
  - Support for custom image file uploads.
- **🌐 Network & ICE Diagnostics Console**:
  - Automated inspection of STUN and TURN candidates.
  - Twilio Network Traversal API integration with automatic fallback to Metered.ca OpenRelay & Google Public STUN.
- **☁️ Cloud Deployment Ready**:
  - Pre-configured for seamless deployment on **Streamlit Community Cloud**, Hugging Face Spaces, or Docker.

---

## 📐 Architecture

```
+-------------------------------------------------------------+
|                     Browser WebRTC Client                   |
|               (getUserMedia + PeerConnection)               |
+------------------------------+------------------------------+
                               |  SDP Offer / Answer
                               |  SRTP Media Stream
+------------------------------v------------------------------+
|                     ICE Server Traversal                    |
|        (Google STUN:19302 / Metered OpenRelay / Twilio)      |
+------------------------------+------------------------------+
                               |
+------------------------------v------------------------------+
|               Streamlit Server (streamlit-webrtc)           |
|                                                             |
|   +-----------------------------------------------------+   |
|   |            VideoTransformEngine (OpenCV)            |   |
|   |  - Canny Edge   - Cartoonizer   - Sepia / Heatmap   |   |
|   |  - Privacy Blur - Face Detect   - Snapshot Lab      |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
```

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/ketan-rmcf123/streamlit-webrtc-test.git
cd streamlit-webrtc-test
pip install -r requirements.txt
```

### 2. Launch Studio

```bash
streamlit run app.py
```
Open `http://localhost:8501` to start streaming and applying real-time filters.

### 3. (Optional) Configure Production TURN

For deployment behind restrictive firewalls (or corporate networks):

```bash
export TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
```

---

## 🧪 Testing

Run the automated test suite:

```bash
python -m unittest discover -s tests
# or using pytest
pytest tests/
```

All 9 unit tests validate filter matrix transformations, dimensions, pipeline routing, and ICE fallback logic.

---

## 📁 Repository Structure

```
streamlit-webrtc-test/
├── app.py                      # Modern Multi-Tab Streamlit Web Application
├── pyproject.toml              # Modern package manifest
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
├── core/                       # Core WebRTC & CV engines
│   ├── __init__.py
│   ├── processors.py           # Real-time video filters & face detection
│   └── ice.py                  # ICE / STUN / TURN server manager
├── utils/                      # Legacy Twilio helper (maintained for backwards compat)
│   └── turn.py
├── webrtc_ice.py               # Minimalist loopback script (maintained)
└── tests/
    ├── __init__.py
    └── test_webrtc_studio.py   # Unit test suite
```

---

## 📜 License

MIT License. Open for educational and commercial applications.
