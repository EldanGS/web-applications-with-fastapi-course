from typing import Optional

from starlette.requests import Request

from services import user_service
from viewmodels.shared.viewmodel import ViewModelBase


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request):
        super().__init__(request)

        self.email: Optional[str] = None
        self.name: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.email = form.get("email")
        self.password = form.get("password")

        if not self.name or not self.name.strip():
            self.error = "Your name is required"
        elif not self.email or not self.email.strip():
            self.error = "Your email is required"
        elif not self.password or len(self.password.strip()) < 5:
            self.error = "Your password is required and must be at least 5 characters"
        elif user_service.get_user_by_email(self.email):
            self.error = f"That email: {self.email} is already used."
