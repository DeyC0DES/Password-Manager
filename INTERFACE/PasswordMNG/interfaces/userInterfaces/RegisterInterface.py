from API.requests.UserRequest import UserRequest

from flet import *

from interfaces.A_components.NotificationContainer import NotificationContainer
from interfaces.A_components.ReturnButton import ReturnButton


class RegisterInterface(UserControl):
    def __init__(self):
        super().__init__()
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

    def create_notification(self, text = 'None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def verify_camps(username, email, password, confirm_password):
            if email == '' or email is None or password == '' or password is None or confirm_password == '' or confirm_password is None or username == '' or username is None:
                self.create_notification('All fields must be filled in!!!', 'Fields Empty')
                return False

            if password != confirm_password:
                self.create_notification('The password does not matches!!!', 'Password Wrong')
                return False

            return True

        def register():
            import main

            self.add_load_screen()

            email = _email_textField.value
            password = _password_textField.value
            confirm_password = _confirm_password_textField.value
            username = _username_textField.value

            if not verify_camps(username, email, password, confirm_password):
                self.remove_load_screen()
                return

            user_request = UserRequest()
            response = user_request.register_request(username, email, password, confirm_password)

            match response.status_code:
                case 200:
                    main.info_data_storage.set_info_data('Your account has been created!!!')
                    self.page.go('password-manager/login')
                case 409:
                    self.create_notification('Already have an account with that email!!!', 'Email in use!')
                case 401:
                    self.create_notification('The passwords does not matches!!!', 'Password Wrong')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        _username_textField = TextField(
            width=500,
            text_size=25,
            border=InputBorder.UNDERLINE,
            border_width=3,
            border_color='#9146ff',
            color='white',
            hint_text='Username',
            suffix_icon=icons.ACCOUNT_CIRCLE_ROUNDED,
            content_padding=padding.only(left=15, right=20)
        )

        _email_textField = TextField(
            width=500,
            text_size=25,
            border=InputBorder.UNDERLINE,
            border_width=3,
            border_color='#9146ff',
            color='white',
            hint_text='Email',
            suffix_icon=icons.EMAIL,
            content_padding=padding.only(left=15, right=20)
        )

        _password_textField = TextField(
            width=500,
            password=True,
            can_reveal_password=True,
            text_size=25,
            border=InputBorder.UNDERLINE,
            border_width=3,
            border_color='#9146ff',
            color='white',
            hint_text='Password',
            content_padding=padding.only(left=15, right=20)
        )

        _confirm_password_textField = TextField(
            width=500,
            password=True,
            can_reveal_password=True,
            text_size=25,
            border=InputBorder.UNDERLINE,
            border_width=3,
            border_color='#9146ff',
            color='white',
            hint_text='Confirm',
            content_padding=padding.only(left=15, right=20)
        )

        _register_button = ElevatedButton(
            width=250,
            height=60,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
                bgcolor={"": '#9146ff', "hovered": '#481D85'}
            ),
            on_click=lambda e: register(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'Register',
                        size=25,
                        color='white',
                        weight=FontWeight.BOLD
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
                                        ReturnButton('password-manager/login')
                                    ]
                                ),

                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Container(
                                                    width=750,
                                                    height=800,
                                                    border_radius=20,
                                                    border=border.all(2, '#333333'),
                                                    alignment=alignment.center,
                                                    content=Row(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        controls=[
                                                            Container(
                                                                width=735,
                                                                height=785,
                                                                gradient=LinearGradient(
                                                                    begin=alignment.top_left,
                                                                    end=alignment.bottom_right,
                                                                    colors=['#333333', '#161616']
                                                                ),
                                                                border_radius=15,
                                                                padding=25,
                                                                content=Column(
                                                                    spacing=125,
                                                                    controls=[
                                                                        Row(
                                                                            alignment=MainAxisAlignment.CENTER,
                                                                            controls=[
                                                                                Text(
                                                                                    "Password",
                                                                                    weight=FontWeight.BOLD,
                                                                                    color='white',
                                                                                    size=40
                                                                                ),

                                                                                Text(
                                                                                    "Manager",
                                                                                    weight=FontWeight.BOLD,
                                                                                    color='#9146ff',
                                                                                    size=40
                                                                                )
                                                                            ]
                                                                        ),

                                                                        Column(
                                                                            spacing=80,
                                                                            controls=[
                                                                                Column(
                                                                                    spacing=60,
                                                                                    controls=[
                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _username_textField
                                                                                            ]
                                                                                        ),

                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _email_textField
                                                                                            ]
                                                                                        ),

                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _password_textField
                                                                                            ]
                                                                                        ),

                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _confirm_password_textField
                                                                                            ]
                                                                                        )
                                                                                    ]
                                                                                ),

                                                                                Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        Container(
                                                                                            width=500,
                                                                                            height=350,
                                                                                            content=Column(
                                                                                                spacing=80,
                                                                                                controls=[
                                                                                                    Column(
                                                                                                        spacing=35,
                                                                                                        controls=[
                                                                                                            Row(
                                                                                                                alignment=MainAxisAlignment.CENTER,
                                                                                                                controls=[
                                                                                                                    _register_button
                                                                                                                ]
                                                                                                            ),
                                                                                                        ]
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                self.notification_row
                            ]
                        )
                    ),

                    self.loading_row,
                ]
            )
        )

        return _main_container