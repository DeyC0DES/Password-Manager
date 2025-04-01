from flet import *

from interfaces.A_components.LoadingScreen import LoadingScreen
from interfaces.accountInterfaces.AccountDetailsInterface import AccountDetailsInterface
from interfaces.accountInterfaces.AccountsInterface import AccountsInterface
from interfaces.accountInterfaces.CreateAccountInterface import CreateAccountInterface
from interfaces.dataStorages.UpdateUserDataStorage import UpdateUserDataStorage
from interfaces.passwordGenerator.PasswordGeneratorInterface import PasswordGeneratorInterface
from interfaces.userInterfaces.LoginInterface import LoginInterface
from interfaces.userInterfaces.RegisterInterface import RegisterInterface
from interfaces.userInterfaces.StepsVerificationInterface import StepsVerificationInterface
from interfaces.userInterfaces.updateUserInterfaces.EmailVerificationInterface import EmailVerificationInterface
from interfaces.userInterfaces.updateUserInterfaces.PasswordChangeInterface import PasswordChangeInterface
from interfaces.userInterfaces.updateUserInterfaces.UserConfigInterface import UserConfigInterface
from interfaces.dataStorages.AccountDataStorage import AccountDataStorage
from interfaces.dataStorages.InfoDataStorage import InfoDataStorage
from interfaces.dataStorages.UserDataStorage import UserDataStorage
from interfaces.userInterfaces.updateUserInterfaces.VerifyDeleteInterface import VerifyDeleteInterface
from interfaces.userInterfaces.updateUserInterfaces.VerifyForgetInterface import VerifyForgetInterface

# Global classes
# data storage
update_user_storage = UpdateUserDataStorage()
account_data_storage = AccountDataStorage()
user_data_storage = UserDataStorage()
info_data_storage = InfoDataStorage()

# animations
load_screen = LoadingScreen()

def start(page: Page):

    # route config
    def change_route(route):

        def column_presets(interface):
            _main_column.controls.clear()
            _main_column.controls.append(interface)
            _main_column.controls.append(_notification_row)

        def add_view(interface):
            column_presets(interface)
            page.views.append(
                View(
                    'password-manager/login',
                    padding=0,
                    controls=[
                        _main_column
                    ]
                )
            )
            page.update()

        page.views.clear()

        if _main_column.controls not in page.controls:
            page.add(_main_column)

        match page.route:
            case 'password-manager/login':
                add_view(login_interface)
                login_interface.verify_notification()

            case 'password-manager/2steps':
                add_view(steps_verification_interface)
                steps_verification_interface.verify_notification()

            case 'password-manager/register':
                add_view(register_interface)

            case 'password-manager/forget/verify':
                add_view(verify_forget_interface)
                verify_forget_interface.verify_notification()

            case 'password-manager/update/password':
                add_view(password_change_interface)

            case 'password-manager/accounts':
                add_view(accounts_interface)
                accounts_interface.clean_account_column()
                accounts_interface.create_account_cards()
                accounts_interface.verify_notification()
                accounts_interface.makes_visible_false()

            case 'password-manager/accounts/edit':
                add_view(accounts_edit_interface)
                accounts_edit_interface.disable_visible_from_mini_buttons()

            case 'password-manager/accounts/create':
                add_view(create_accounts_interface)

            case 'password-manager/accounts/pwdgen':
                add_view(password_generator_interface)

            case 'password-manager/accounts/settings':
                add_view(account_config_interface)

            case 'password-manager/accounts/settings/delete':
                add_view(delete_verify_interface)

            case 'password-manager/accounts/settings/email_verify':
                add_view(email_verification_interface)
                email_verification_interface.verify_notification()
                email_verification_interface.get_update_data()

    # page config
    page.window.width = 1960
    page.window.height = 1020
    page.title = 'Password MNG'
    page.padding = 0

    # Interfaces
    login_interface = LoginInterface()
    register_interface = RegisterInterface()
    steps_verification_interface = StepsVerificationInterface()
    accounts_interface = AccountsInterface()
    create_accounts_interface = CreateAccountInterface()
    accounts_edit_interface = AccountDetailsInterface()
    password_generator_interface = PasswordGeneratorInterface()
    account_config_interface = UserConfigInterface()
    email_verification_interface = EmailVerificationInterface()
    verify_forget_interface = VerifyForgetInterface()
    password_change_interface = PasswordChangeInterface()
    delete_verify_interface = VerifyDeleteInterface()

    _notification_row = Row(
        controls=[

        ]
    )

    #
    _main_column = Stack(
        controls=[
            _notification_row
        ]
    )

    page.on_route_change=change_route
    page.go('password-manager/login')
    page.update()

if __name__ == '__main__':
    app(target=start)