from starlette.requests import Request

from viewmodels.shared.viewmodel import ViewModelBase


class LoginViewModel(ViewModelBase):

    def __init__(self, request: Request):
        super().__init__(request)

        self.email = ""
        self.password = ""

    async def load(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

        if not self.email or not self.email.strip():
            self.error = "Your email is required"
        elif not self.password or not self.password.strip():
            self.error = "Your name is required"


