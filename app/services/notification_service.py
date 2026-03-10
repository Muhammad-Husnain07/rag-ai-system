from typing import List, Optional
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    """Types of notifications."""
    DOCUMENT_PROCESSED = "document_processed"
    DOCUMENT_FAILED = "document_failed"
    CONVERSATION_STARTED = "conversation_started"
    SYSTEM_ANNOUNCEMENT = "system_announcement"


class NotificationService:
    """Service for managing user notifications."""
    
    def __init__(self):
        self._notifications: dict = {}
    
    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.SYSTEM_ANNOUNCEMENT,
        data: Optional[dict] = None
    ) -> dict:
        """Create a new notification for a user."""
        notification_id = f"notif_{user_id}_{datetime.utcnow().timestamp()}"
        
        notification = {
            "id": notification_id,
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "data": data or {},
            "read": False,
            "created_at": datetime.utcnow().isoformat()
        }
        
        if user_id not in self._notifications:
            self._notifications[user_id] = []
        
        self._notifications[user_id].append(notification)
        
        return notification
    
    def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[dict]:
        """Get notifications for a user."""
        user_notifications = self._notifications.get(user_id, [])
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n["read"]]
        
        return sorted(
            user_notifications,
            key=lambda x: x["created_at"],
            reverse=True
        )[:limit]
    
    def mark_as_read(self, user_id: int, notification_id: str) -> bool:
        """Mark a notification as read."""
        user_notifications = self._notifications.get(user_id, [])
        
        for notif in user_notifications:
            if notif["id"] == notification_id:
                notif["read"] = True
                return True
        
        return False
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user."""
        user_notifications = self._notifications.get(user_id, [])
        count = 0
        
        for notif in user_notifications:
            if not notif["read"]:
                notif["read"] = True
                count += 1
        
        return count
    
    def delete_notification(self, user_id: int, notification_id: str) -> bool:
        """Delete a notification."""
        user_notifications = self._notifications.get(user_id, [])
        
        for i, notif in enumerate(user_notifications):
            if notif["id"] == notification_id:
                user_notifications.pop(i)
                return True
        
        return False
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications."""
        user_notifications = self._notifications.get(user_id, [])
        return sum(1 for n in user_notifications if not n["read"])


notification_service = NotificationService()
