from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.admin_portal.models.user import User
from app.admin_portal.routes.auth import get_current_admin
from app.database.database import get_db


public_router = APIRouter(prefix="/site", tags=["Site settings"])
admin_router = APIRouter(prefix="/admin/site", tags=["Admin site settings"])


class ThemeUpdate(BaseModel):
    theme: Literal["light", "dark"]


@public_router.get("/theme")
def get_site_theme(db: Session = Depends(get_db)):
    theme = db.execute(
        text("SELECT theme FROM platform_theme_settings WHERE singleton_id = 1")
    ).scalar_one_or_none()
    return {"theme": theme if theme in {"light", "dark"} else "light"}


@admin_router.put("/theme")
def update_site_theme(
    request: ThemeUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    db.execute(
        text(
            """
            INSERT INTO platform_theme_settings
                (singleton_id, theme, updated_by, updated_at)
            VALUES (1, :theme, :admin_id, NOW())
            ON CONFLICT (singleton_id) DO UPDATE
            SET theme = EXCLUDED.theme,
                updated_by = EXCLUDED.updated_by,
                updated_at = NOW()
            """
        ),
        {"theme": request.theme, "admin_id": current_admin.id},
    )
    db.commit()
    return {"theme": request.theme, "message": "Site theme updated."}
