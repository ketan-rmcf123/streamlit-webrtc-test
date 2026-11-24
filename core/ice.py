"""
WebRTC ICE, STUN, and TURN Server Management.
"""

import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ICEManager:
    """Manages ICE servers for WebRTC peer connections."""

    # Public free STUN servers with high uptime
    PUBLIC_STUN_SERVERS = [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun.cloudflare.com:3478"]},
    ]

    # OpenRelay free community TURN server
    OPENRELAY_TURN_SERVER = [
        {
            "urls": ["turn:openrelay.metered.ca:80"],
            "username": "openrelayproject",
            "credential": "openrelayproject",
        }
    ]

    @classmethod
    def get_ice_servers(cls, use_turn: bool = True) -> List[Dict[str, Any]]:
        """
        Derive optimal ICE server list:
        1. Twilio Network Traversal API (if credentials present)
        2. Free OpenRelay TURN + Google STUN
        3. Public STUN servers
        """
        # 1. Try Twilio
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        if account_sid and auth_token:
            try:
                from twilio.rest import Client
                client = Client(account_sid, auth_token)
                token = client.tokens.create()
                logger.info("Successfully fetched Twilio TURN credentials.")
                return token.ice_servers
            except Exception as e:
                logger.warning(f"Failed to fetch Twilio TURN credentials: {e}. Falling back to OpenRelay.")

        # 2. OpenRelay + Google STUN
        if use_turn:
            return cls.OPENRELAY_TURN_SERVER + cls.PUBLIC_STUN_SERVERS

        # 3. STUN only
        return cls.PUBLIC_STUN_SERVERS

    @classmethod
    def test_connectivity(cls) -> Dict[str, Any]:
        """Check configuration status and report diagnostic details."""
        has_twilio = bool(os.environ.get("TWILIO_ACCOUNT_SID") and os.environ.get("TWILIO_AUTH_TOKEN"))
        servers = cls.get_ice_servers(use_turn=True)
        return {
            "has_twilio_creds": has_twilio,
            "configured_servers_count": len(servers),
            "ice_servers": servers,
            "primary_stun": servers[-1]["urls"][0] if servers else None,
        }
