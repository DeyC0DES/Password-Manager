import asyncio

from flet import *

from API.requests.AccountRequests import AccountRequests
from API.utils.CaptureToken import CaptureToken
from interfaces.A_components.ElevatedCustomIconButton import ElevatedCustomIconButton

from interfaces.A_components.IconContainer import IconContainer
from interfaces.A_components.NotificationContainer import NotificationContainer

class CreateAccountInterface(UserControl):
    def __init__(self):
        super().__init__()
        self.fav_clicked = False
        self.notification_row = Row(alignment=MainAxisAlignment.END,controls=[])
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

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

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
            _main_container.content.controls[0].content.controls[1].visible = True
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
            _main_container.content.controls[0].content.controls[1].visible = False
            _main_container.update()
            _icons_list_container.update()

        def change_icon(icon):
            _icon_container.icon.name = icon
            _icon_container.update()
            self.page.run_task(hide_icon_list_container)

        def create():
            import main

            def verify_fields():
                if username == '' or username is None\
                        or password == '' or password is None\
                        or name == '' or name is None:
                    return False

                return True

            self.add_load_screen()

            account_request = AccountRequests()

            name = _name_textField.value
            username = _username_textField.value
            password = _password_textField.value
            fav = self.fav_clicked
            icon_string = _icon_container.icon.name

            if not verify_fields():
                self.create_notification('All fields need be filled!!!', 'Fields Empty')
                self.remove_load_screen()
                return

            response = account_request.create_account(name, username, password, icon_string, fav, CaptureToken().capture())

            match response.status_code:
                case 200:
                    main.info_data_storage.set_info_data('Account created!!!')
                    self.page.go('password-manager/accounts')
                case 409:
                    self.create_notification('Already have a account with that nickname!!!', 'Nickname in use')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        _name_textField = TextField(
            width=400,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Nickname',
            suffix_icon=Icons.TEXT_FIELDS,
            content_padding=padding.only(left=15, right=20)
        )

        _username_textField = TextField(
            width=400,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Username',
            suffix_icon=Icons.ACCOUNT_CIRCLE,
            content_padding=padding.only(left=15, right=20)
        )

        _password_textField = TextField(
            width=400,
            password=True,
            can_reveal_password=True,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Password',
            content_padding=padding.only(left=15, right=20)
        )

        _bookmark_container = Container(
            on_hover= lambda e: handle_bookmark_hover(e),
            content=IconButton(
                icon=icons.BOOKMARK_BORDER_ROUNDED,
                icon_size=50,
                icon_color='white',
                on_click=lambda e: handle_bookmark_click(),
            )
        )

        _create_button = ElevatedButton(
            width=300,
            height=70,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=20),
                bgcolor={'': '#9146ff', 'hovered': '#481D85'}
            ),
            on_click= lambda e: create(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'Create',
                        size=25,
                        color='white'
                    )
                ]
            )
        )

        _icon_container = IconContainer(show_icon_list_container)

        _icons_list_container = Container(
            width=200, # 260 active value
            height=200, # 400 active value
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
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Container(
                                                    width=760,
                                                    height=330,
                                                    bgcolor='#262626',
                                                    border_radius=20,
                                                    padding=20,
                                                    content=Stack(
                                                        controls=[
                                                            Column(
                                                                alignment=MainAxisAlignment.START,
                                                                spacing=20,
                                                                controls=[
                                                                    Row(
                                                                        alignment=MainAxisAlignment.START,
                                                                        spacing=25,
                                                                        controls=[
                                                                            _icon_container,

                                                                            Column(
                                                                                spacing=20,
                                                                                controls=[
                                                                                    _name_textField,
                                                                                    _username_textField,
                                                                                    _password_textField
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    ),

                                                                    Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            _create_button,

                                                                            ElevatedButton(
                                                                                width=300,
                                                                                height=70,
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=20),
                                                                                    bgcolor={'': '#333333',
                                                                                             'hovered': '#111111'},
                                                                                    overlay_color={'': '#333333',
                                                                                                   'hovered': '#111111'}
                                                                                ),
                                                                                on_click=lambda e: self.page.go(
                                                                                    'password-manager/accounts'),
                                                                                content=Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        Text(
                                                                                            'Back',
                                                                                            size=25,
                                                                                            color='white'
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            ),

                                                            Column(
                                                                alignment=MainAxisAlignment.START,
                                                                controls=[
                                                                    Row(
                                                                        alignment=MainAxisAlignment.END,
                                                                        controls=[
                                                                            _bookmark_container
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
                                    width=800,
                                    height=530,
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