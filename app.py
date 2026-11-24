"""
Streamlit WebRTC Studio: Real-Time Audio/Video Computer Vision & Diagnostics.
"""

import os
import sys
import cv2
import numpy as np
from PIL import Image
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from core.processors import VideoTransformEngine, FilterMode
from core.ice import ICEManager

st.set_page_config(
    page_title="Streamlit WebRTC Studio",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📡 Streamlit WebRTC & Computer Vision Studio")
st.caption("Production-grade WebRTC real-time media streaming, live computer vision transformations, and ICE / TURN network diagnostics.")

# Initialize engine
engine = VideoTransformEngine()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Stream Configuration")

    filter_mode_str = st.selectbox(
        "Active Video Filter",
        [m.value for m in FilterMode],
        index=0
    )
    current_filter = next(m for m in FilterMode if m.value == filter_mode_str)

    st.markdown("---")
    st.subheader("🌐 ICE / TURN Settings")
    enable_turn = st.checkbox("Enable TURN Server (Recommended for Cloud)", value=True)
    ice_servers = ICEManager.get_ice_servers(use_turn=enable_turn)
    st.caption(f"Loaded {len(ice_servers)} ICE server configurations.")

tabs = st.tabs([
    "🎥 Live Video Stream",
    "📸 Snapshot & Filter Lab",
    "🌐 ICE Diagnostics",
    "📖 Architecture & Deployment Guide"
])

# ----------------- TAB 1: LIVE WEBRTC STREAM -----------------
with tabs[0]:
    st.header("Real-Time WebRTC Video Pipeline")
    st.info("Streams low-latency video via browser WebRTC peer connection, processing frames server-side through OpenCV.")

    col_stream, col_info = st.columns([3, 1])

    with col_info:
        st.markdown("#### Stream Controls")
        st.write(f"**Filter:** `{current_filter.value}`")
        if current_filter == FilterMode.CANNY_EDGES:
            st.caption("Extracts structural contours and gradients.")
        elif current_filter == FilterMode.CARTOON:
            st.caption("Bilateral filtering + adaptive threshold lines.")
        elif current_filter == FilterMode.FACE_DETECTION:
            st.caption("Detects human faces with Haar Cascades.")

    with col_stream:
        # Check if streamlit-webrtc is importable
        has_webrtc = False
        try:
            from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
            import av
            has_webrtc = True
        except ImportError:
            has_webrtc = False

        if has_webrtc:
            class CVVideoProcessor:
                def __init__(self):
                    self.filter = current_filter

                def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
                    img = frame.to_ndarray(format="bgr24")
                    processed = engine.transform(img, self.filter)
                    return av.VideoFrame.from_ndarray(processed, format="bgr24")

            webrtc_streamer(
                key="webrtc_live_stream",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTCConfiguration({"iceServers": ice_servers}),
                video_processor_factory=CVVideoProcessor,
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )
        else:
            st.warning("`streamlit-webrtc` is initializing. You can also use the Snapshot & Filter Lab tab below for instant camera input!")

# ----------------- TAB 2: SNAPSHOT & FILTER LAB -----------------
with tabs[1]:
    st.header("Instant Snapshot & Computer Vision Lab")
    st.write("Capture a frame from your webcam or upload a photo to preview all filters simultaneously.")

    photo = st.camera_input("Capture Instant Snapshot")
    uploaded = st.file_uploader("Or Upload an Image File", type=["jpg", "jpeg", "png", "webp"])

    target_bgr = None
    if photo:
        pil_img = Image.open(photo).convert("RGB")
        target_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    elif uploaded:
        pil_img = Image.open(uploaded).convert("RGB")
        target_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    else:
        # Provide sample test pattern
        if st.button("🧪 Generate Test Color Pattern"):
            pattern = np.zeros((360, 480, 3), dtype=np.uint8)
            # Create color gradient
            for y in range(360):
                for x in range(480):
                    pattern[y, x] = [int(x / 480 * 255), int(y / 360 * 255), 180]
            # Draw shapes and text
            cv2.circle(pattern, (240, 180), 80, (255, 255, 255), -1)
            cv2.putText(pattern, "Streamlit WebRTC", (80, 190), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (20, 20, 20), 2)
            target_bgr = pattern

    if target_bgr is not None:
        st.markdown("### Processed Results")
        processed_bgr = engine.transform(target_bgr, current_filter)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Input Frame")
            st.image(cv2.cvtColor(target_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)
        with col2:
            st.subheader(f"Output ({current_filter.value})")
            st.image(cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        # Download button
        import io
        pil_out = Image.fromarray(cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        pil_out.save(buf, format="PNG")
        st.download_button(
            label="💾 Download Filtered Frame (PNG)",
            data=buf.getvalue(),
            file_name=f"webrtc_filter_{current_filter.name.lower()}.png",
            mime="image/png"
        )

# ----------------- TAB 3: ICE DIAGNOSTICS -----------------
with tabs[2]:
    st.header("ICE & Network Diagnostics")
    diag = ICEManager.test_connectivity()

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.metric("Configured ICE Servers", diag["configured_servers_count"])
        st.metric("Twilio Credentials Present", "Yes" if diag["has_twilio_creds"] else "No (Using OpenRelay + Google STUN)")
    with col_d2:
        st.metric("Primary STUN Endpoint", diag["primary_stun"])

    st.subheader("Active ICE Configuration:")
    st.json(diag["ice_servers"])

# ----------------- TAB 4: ARCHITECTURE GUIDE -----------------
with tabs[3]:
    st.header("WebRTC Architecture & Deployment Best Practices")
    st.markdown("""
    ### Why is STUN/TURN Necessary?
    WebRTC operates using peer-to-peer UDP/TCP connections. When deployed on **Streamlit Community Cloud**, your browser client is behind a Symmetric NAT / Firewall, and the Streamlit container is behind another NAT.
    
    1. **STUN (Session Traversal Utilities for NAT)**: Discovers the client's public IP and port mapping. Works for ~80% of open residential connections.
    2. **TURN (Traversal Using Relays around NAT)**: When both ends are behind restrictive enterprise or symmetric NATs, STUN cannot punch a direct hole. A TURN server acts as an encrypted media relay server.
    
    ### Free Community vs Production TURN
    - **Development / Local**: Free Google STUN (`stun.l.google.com:19302`) works seamlessly.
    - **Community Cloud / Testing**: Metered.ca OpenRelay TURN provides free relay endpoints.
    - **Production**: Configure Twilio Network Traversal API by exporting:
      ```bash
      export TWILIO_ACCOUNT_SID="ACxxx..."
      export TWILIO_AUTH_TOKEN="your_token..."
      ```
    """)
