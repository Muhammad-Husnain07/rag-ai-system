from typing import List, Optional, Dict, Any
from datetime import datetime
import hashlib
import hmac
import json


class WebhookService:
    """Service for handling webhooks."""
    
    def __init__(self, secret: str = ""):
        self.secret = secret
        self.webhooks: Dict[str, dict] = {}
    
    def register_webhook(
        self,
        user_id: int,
        url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> dict:
        """Register a new webhook."""
        webhook_id = hashlib.sha256(f"{user_id}_{url}_{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        
        self.webhooks[webhook_id] = {
            "id": webhook_id,
            "user_id": user_id,
            "url": url,
            "events": events,
            "secret": secret or self.secret,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }
        
        return self.webhooks[webhook_id]
    
    def delete_webhook(self, webhook_id: str, user_id: int) -> bool:
        """Delete a webhook."""
        if webhook_id in self.webhooks:
            if self.webhooks[webhook_id]["user_id"] == user_id:
                del self.webhooks[webhook_id]
                return True
        return False
    
    def get_webhooks(self, user_id: int) -> List[dict]:
        """Get all webhooks for a user."""
        return [
            webhook for webhook in self.webhooks.values()
            if webhook["user_id"] == user_id
        ]
    
    def verify_signature(self, payload: str, signature: str, webhook_id: str) -> bool:
        """Verify webhook signature."""
        if webhook_id not in self.webhooks:
            return False
        
        webhook = self.webhooks[webhook_id]
        if not webhook.get("secret"):
            return True
        
        expected_signature = hmac.new(
            webhook["secret"].encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
    
    async def trigger_event(
        self,
        event: str,
        data: dict,
        user_id: int
    ):
        """Trigger webhook events for specific user."""
        user_webhooks = self.get_webhooks(user_id)
        
        for webhook in user_webhooks:
            if event in webhook["events"] and webhook["active"]:
                await self._send_webhook(webhook, event, data)
    
    async def _send_webhook(self, webhook: dict, event: str, data: dict):
        """Send webhook payload to endpoint."""
        import aiohttp
        
        payload = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    webhook["url"],
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                )
        except Exception:
            pass


webhook_service = WebhookService()
