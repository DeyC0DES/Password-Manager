import asyncio
import json

import clipboard
from flet import *

from API.requests.AccountRequests import AccountRequests
from API.utils.CaptureToken import CaptureToken
from interfaces.A_components.ElevatedCustomIconButton import ElevatedCustomIconButton
from interfaces.A_components.IconContainer import IconContainer
from interfaces.A_components.MiniIconButton import MiniIconButton
from interfaces.A_components.NotificationContainer import NotificationContainer
from interfaces.A_components.ReturnButton import ReturnButton


class AccountDetailsInterface(UserControl):
    def __init__(self):
        super().__init__()
        self.password_fields_editable = False
        self.editable = False
        self.fav_clicked = False
        self.notification_row = Row(alignment=MainAxisAlignment.END,controls=[])
        self.delete_mini_button = None
        self.edit_mini_button = None
        self.save_mini_button = None
        self.show_password_mini_button = None
        self.clipboard_mini_button = None
        self.name = None
        self.username = None
        self.old_password = None
        self.icon = None
        self.loading_row = Row(expand=True, alignment=MainAxisAlignment.START, controls=[])

    def add_load_screen(self):
        import main

        main.load_screen.animation_bool = True
        self.loading_row.controls.append(main.load_screen)
        self.page.run_task(main.load_screen.animation)
        self.loading_row.update()

    def remove_load_screen(self):
        import main

        main.load_screen.animation_bool = False
        self.loading_row.clean()

        try:
            self.loading_row.update()
        except Exception:
            pass

    def disable_visible_from_mini_buttons(self):
        self.save_mini_button.visible = False
        self.delete_mini_button.visible = False
        self.delete_mini_button.update()
        self.save_mini_button.update()

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def reset_booleans():
            self.password_fields_editable = False
            self.editable = False

        def get_account_data():
            import main
            content = main.account_data_storage.get_account_data()
            self.name = content.get('name', 'Unknown')
            self.username = content.get('username', 'Unknown')
            self.fav_clicked = content.get('fav', False)
            self.old_password = content.get('old_password', 'Empty')
            self.icon = content.get('icon', '')

        def handle_delete_account():
            import main

            account_requests = AccountRequests()
            response = account_requests.delete_account(self.name, CaptureToken().capture())

            match response.status_code:
                case 200:
                    main.info_data_storage.set_info_data('Account deleted successfully')
                    self.page.go('password-manager/accounts')
                case 403:
                    self.create_notification('Unauthorized. Please select the account again!!!', 'Unauthorized')
                case 404:
                    self.create_notification('Account dont found on data-base!!!', 'Not found')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

        def handle_bookmark_hover(e):
            if e.data == 'true':
                if self.fav_clicked:
                    _bookmark_container.content.icon_color = '#ff6961'
                    _bookmark_container.content.icon = icons.BOOKMARK_REMOVE_ROUNDED
                else:
                    _bookmark_container.content.icon_color = '#fdfd96'
                    _bookmark_container.content.icon = icons.BOOKMARK_ROUNDED
            else:
                if self.fav_clicked:
                    _bookmark_container.content.icon_color = '#fdfd96'
                    _bookmark_container.content.icon = icons.BOOKMARK_ROUNDED
                else:
                    _bookmark_container.content.icon_color = 'white'
                    _bookmark_container.content.icon = icons.BOOKMARK_BORDER_ROUNDED

            _bookmark_container.update()

        def handle_bookmark_click():
            if self.fav_clicked:
                _bookmark_container.content.icon = icons.BOOKMARK_BORDER_ROUNDED
                _bookmark_container.content.icon_color = 'white'
                self.fav_clicked = False
            else:
                _bookmark_container.content.icon = icons.BOOKMARK_ROUNDED
                _bookmark_container.content.icon_color = '#fdfd96'
                self.fav_clicked = True

            _bookmark_container.update()

        async def show_icon_list_container():
            _icons_list_container.visible = True
            _main_container.content.controls[2].visible = True
            _main_container.update()
            _icons_list_container.update()
            await asyncio.sleep(0.2)
            _icons_list_container.width = 260
            _icons_list_container.height = 400
            _icons_list_container.opacity = 1
            _main_container.update()
            _icons_list_container.update()

        async def hide_icon_list_container():
            _icons_list_container.width = 200
            _icons_list_container.height = 200
            _icons_list_container.opacity = 0
            _main_container.update()
            _icons_list_container.update()
            await asyncio.sleep(0.5)
            _icons_list_container.visible = False
            _main_container.content.controls[2].visible = False
            _main_container.update()
            _icons_list_container.update()

        def change_icon(icon):
            _icon_container.icon.username = icon
            _icon_container.update()
            self.page.run_task(hide_icon_list_container)

        def handle_edit_active():
            self.add_load_screen()

            if self.editable:
                _name_textField.disabled = True
                _username_textField.disabled = True
                _password_textField.disabled = True
                self.delete_mini_button.visible = False
                self.save_mini_button.visible = False
                _name_textField.update()
                _username_textField.update()
                _password_textField.update()
                self.delete_mini_button.update()
                self.save_mini_button.update()
                self.editable = False
            else:
                _name_textField.disabled = False
                _username_textField.disabled = False
                _icon_container.disabled = False

                if self.password_fields_editable:
                    print('here')
                    _password_textField.disabled = False
                    _password_textField.update()

                self.delete_mini_button.visible = True
                self.save_mini_button.visible = True
                _name_textField.update()
                _username_textField.update()
                _icon_container.update()
                self.delete_mini_button.update()
                self.save_mini_button.update()
                self.editable = True
            self.remove_load_screen()

        def decode_password():
            self.add_load_screen()
            account_requests = AccountRequests()
            response = account_requests.decode_password(self.name, CaptureToken().capture())
            self.remove_load_screen()
            return json.loads(response.content)

        def handle_password_click():
            self.password_fields_editable = not self.password_fields_editable

            if self.password_fields_editable:
                response_content = decode_password()
                _password_textField.value = response_content.get('message', 'Failed!')
                _password_textField.update()
                _password_old_textField.value = self.old_password if self.old_password is not None else 'Empty'
                _password_old_textField.update()
            else:
                _password_textField.value = '******************'
                _password_textField.update()
                _password_old_textField.value = '******************'
                _password_old_textField.update()

        def handle_save():
            import main

            self.add_load_screen()

            account_requests = AccountRequests()
            password = None

            if _password_textField.value == '******************':
                response_content = decode_password()
                password = response_content.get('message', 'Failed!')

                if password == 'Failed!':
                    self.create_notification('Something went wrong!!!', 'Error')
                    return

            response = account_requests.update_account(self.name, _name_textField.value, _username_textField.value, _password_textField.value if _password_textField.value != '******************' else password, _icon_container.icon.name, self.fav_clicked, CaptureToken().capture())

            match response.status_code:
                case 200:
                    reset_booleans()
                    main.info_data_storage.set_info_data('Account edit saved successfully')
                    self.page.go('password-manager/accounts')
                case 400:
                    self.create_notification('Some error occurred, please try again!!!', 'Error')
                case 401:
                    self.create_notification('Unauthorized. Please select the account again!!!', 'Unauthorized')
                case 404:
                    self.create_notification('Account dont found on data-base!!!', 'Not found')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        def copy_to_clipboard():
            response_content = decode_password()
            clipboard.copy(response_content.get('message', 'Failed!'))
            self.create_notification('Copy to clipboard successfully!!!', 'Success')


        get_account_data()

        _name_textField = TextField(
            width=510,
            value=self.name,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Name',
            disabled=True,
            suffix_icon=Icons.TEXT_FIELDS_ROUNDED,
            content_padding=padding.only(left=15, right=20)
        )

        _username_textField = TextField(
            width=510,
            value=self.username,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Username',
            disabled=True,
            suffix_icon=Icons.ACCOUNT_CIRCLE,
            content_padding=padding.only(left=15, right=20)
        )

        _password_textField = TextField(
            width=510,
            value='******************',
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Password',
            disabled=True,
            suffix_icon=Icons.LOCK_ROUNDED,
            content_padding=padding.only(left=15, right=20)
        )

        _password_old_textField = TextField(
            width=510,
            text_size=25,
            value='******************',
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Old Password',
            disabled=True,
            suffix_icon=Icons.LOCK_OPEN_ROUNDED,
            content_padding=padding.only(left=15, right=20)
        )

        _bookmark_container = Container(
            on_hover=lambda e: handle_bookmark_hover(e),
            content=IconButton(
                icon=icons.BOOKMARK_BORDER_ROUNDED if not self.fav_clicked else icons.BOOKMARK_ROUNDED,
                icon_size=50,
                icon_color='white' if not self.fav_clicked else '#fdfd96',
                on_click=lambda e: handle_bookmark_click(),
            )
        )

        self.delete_mini_button = MiniIconButton('red', icons.DELETE, True, handle_delete_account)
        self.edit_mini_button = MiniIconButton('#161616', icons.EDIT, True, handle_edit_active)
        self.save_mini_button = MiniIconButton('green', icons.SAVE, True, handle_save)
        self.show_password_mini_button = MiniIconButton('#161616', icons.PASSWORD, True, handle_password_click)
        self.clipboard_mini_button = MiniIconButton('#161616', Icons.CONTENT_COPY, True, copy_to_clipboard)

        _icon_container = IconContainer(show_icon_list_container, self.icon)
        _icon_container.disabled = True

        _icons_list_container = Container(
            width=200,  # 260 active value
            height=200,  # 400 active value
            bgcolor='#333333',
            border_radius=20,
            visible=False,
            opacity=0,
            animate=animation.Animation(500, AnimationCurve.EASE_IN_OUT),
            animate_opacity=animation.Animation(550, AnimationCurve.EASE_IN_OUT),
            padding=15,
            content=Column(
                alignment=MainAxisAlignment.START,
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            ElevatedCustomIconButton("EMAIL_ROUNDED", change_icon),
                            ElevatedCustomIconButton("ALTERNATE_EMAIL", change_icon),
                            ElevatedCustomIconButton("ACCOUNT_BALANCE_WALLET", change_icon),
                            ElevatedCustomIconButton("ACCOUNT_BALANCE", change_icon),
                        ]
                    ),

                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            ElevatedCustomIconButton("ACCOUNT_BOX_ROUNDED", change_icon),
                            ElevatedCustomIconButton("ACCOUNT_CIRCLE", change_icon),
                            ElevatedCustomIconButton("PLAY_ARROW_ROUNDED", change_icon),
                            ElevatedCustomIconButton("NETWORK_WIFI", change_icon),
                        ]
                    ),

                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            ElevatedCustomIconButton("LOCK_ROUNDED", change_icon),
                            ElevatedCustomIconButton("VPN_KEY", change_icon),
                            ElevatedCustomIconButton("VPN_LOCK_ROUNDED", change_icon),
                            ElevatedCustomIconButton("HELP_ROUNDED", change_icon),
                        ]
                    )
                ]
            )
        )

        _main_container = Container(
            width=1960,
            height=980,
            bgcolor='#111111',
            content=Stack(
                controls=[
                    Container(
                        width=1960,
                        height=980,
                        padding=15,
                        content=Stack(
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    controls=[
                                        ReturnButton('password-manager/accounts', reset_booleans)
                                    ]
                                ),

                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Container(
                                                    width=760,
                                                    height=320,
                                                    bgcolor='#262626',
                                                    border_radius=20,
                                                    padding=20,
                                                    content=Stack(
                                                        controls=[
                                                            Column(
                                                                controls=[
                                                                    Row(
                                                                        alignment=MainAxisAlignment.START,
                                                                        controls=[
                                                                            _icon_container,

                                                                            Column(
                                                                                controls=[
                                                                                    Column(
                                                                                        controls=[
                                                                                            _name_textField,
                                                                                            _username_textField,
                                                                                            _password_textField,
                                                                                            _password_old_textField
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    ),

                                                                    Row(
                                                                        alignment=MainAxisAlignment.END,
                                                                        controls=[
                                                                            Row(
                                                                                alignment=MainAxisAlignment.START,
                                                                                expand=True,
                                                                                controls=[
                                                                                    _bookmark_container
                                                                                ]
                                                                            ),

                                                                            Row(
                                                                                alignment=MainAxisAlignment.END,
                                                                                controls=[
                                                                                    self.delete_mini_button,
                                                                                    self.edit_mini_button,
                                                                                    self.show_password_mini_button,
                                                                                    self.clipboard_mini_button,
                                                                                    self.save_mini_button,
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                Container(
                                    width=797,
                                    height=550,
                                    visible=False,
                                    content=Row(
                                        alignment=MainAxisAlignment.END,
                                        controls=[
                                            Column(
                                                alignment=MainAxisAlignment.END,
                                                controls=[
                                                    _icons_list_container
                                                ]
                                            )
                                        ]
                                    )
                                ),

                                self.loading_row,
                            ]
                        )
                    ),

                    self.notification_row
                ]
            )
        )

        return _main_container