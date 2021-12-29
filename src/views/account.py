import fastapi
from fastapi_chameleon import template
from starlette import status
from starlette.requests import Request

from infrastructure import cookie_auth
from services import user_service
from viewmodels.account.account_viewmodel import AccountViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel

router = fastapi.APIRouter()


@router.get('/account')
@template()
def index(request: Request):
    vm = AccountViewModel(request)
    return vm.to_dict()


@router.get('/account/register')
@template()
def register(request: Request):
    vm = RegisterViewModel(request)
    return vm.to_dict()


@router.post('/account/register')
@template()
async def register(request: Request):
    vm = RegisterViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    # TODO: create account
    account = user_service.create_account(vm.name, vm.email, vm.password)

    # TODO: login account
    response = fastapi.responses.RedirectResponse(url="/account",
                                                  status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, account.id)
    print("TODO: Redirect")
    return response


### LOGIN

@router.get('/account/login')
@template(template_file='account/login.pt')
def login_get(request: Request):
    vm = LoginViewModel(request)
    return vm.to_dict()


@router.post('/account/login')
@template(template_file='account/login.pt')
async def login_post(request: Request):
    vm = LoginViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    account = user_service.login_user(vm.email, vm.password)
    if not account:
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    response = fastapi.responses.RedirectResponse(url="/account",
                                                  status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, account.id)
    return response


@router.get('/account/logout')
def logout(request: Request):
    response = fastapi.responses.RedirectResponse(url="/",
                                                  status_code=status.HTTP_302_FOUND)
    cookie_auth.logout(response)
    return response
