from __future__ import annotations

from fastapi import HTTPException

from app.data.seed import USERS
from app.models.schemas import RequestContext


class RoleGuardService:
    GLOBAL_ADMIN_IDS = {"admin_root"}

    def validate_actor(self, context: RequestContext) -> None:
        actor = USERS.get(context.requester_id)
        if not actor:
            raise HTTPException(status_code=401, detail="Unknown requester_id")
        if actor.role != context.requester_role.value:
            raise HTTPException(status_code=403, detail="Role mismatch for requester")

    def can_access_staff(self, context: RequestContext, staff_id: str) -> None:
        self.validate_actor(context)
        if context.requester_role.value == "staff" and context.requester_id != staff_id:
            raise HTTPException(status_code=403, detail="Staff can only access their own data")
        if context.requester_role.value == "admin" and context.requester_id not in self.GLOBAL_ADMIN_IDS:
            actor = USERS[context.requester_id]
            staff = USERS.get(staff_id)
            if not staff or staff.store_id != actor.store_id:
                raise HTTPException(status_code=403, detail="Store manager can only access staff in their own store")

    def can_access_store(self, context: RequestContext, store_id: str) -> None:
        self.validate_actor(context)
        if context.requester_role.value == "staff":
            actor = USERS[context.requester_id]
            if actor.store_id != store_id:
                raise HTTPException(status_code=403, detail="Staff can only access their own store")
        if context.requester_role.value == "admin" and context.requester_id not in self.GLOBAL_ADMIN_IDS:
            actor = USERS[context.requester_id]
            if actor.store_id != store_id:
                raise HTTPException(status_code=403, detail="Store manager can only access their own store")
