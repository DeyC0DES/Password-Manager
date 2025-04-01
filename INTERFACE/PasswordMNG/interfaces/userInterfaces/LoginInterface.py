from interfaces.A_components.ExitButton import ExitButton
from API.requests.UserRequest import UserRequest

from flet import *

from interfaces.A_components.NotificationContainer import NotificationContainer


class LoginInterface(UserControl):
    def __init__(self):
        super().__init__()
        self.notification_row = Row(alignment=MainAxisAlignment.END, controls=[])
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

    def verify_notification(self):
        import main

        try:
            message = main.info_data_storage.get_info_data().get('content', None)
        except AttributeError:
            return

        main.info_data_storage.clear()

        if message is None:
            return

        self.create_notification(message, 'Info')

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def forget_password():
            import main

            self.add_load_screen()

            email = _email_textField.value

            if email == '' or email is None:
                self.create_notification('Email field need be filled!', 'Info')
                self.remove_load_screen()
                return

            user_request = UserRequest()
            user_response = user_request.forget_password_request(email)

            match user_response.status_code:
                case 200:
                    main.user_data_storage.set_user_data(email, 'Unknown', 'None')
                    main.info_data_storage.set_info_data('A code was sent on your email!')

                    self.page.go('password-manager/forget/verify')
                case 404:
                    self.create_notification('Email not found!', 'Invalid')
                case _:
                    self.create_notification(f'Error: {user_response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        def login():
            import main

            self.add_load_screen()

            email = _email_textField.value
            password = _password_textField.value

            user_request = UserRequest()
            response = user_request.login_request(email, password)

            match response.status_code:
                case 200:
                    main.user_data_storage.set_user_data(email, None, None)
                    main.info_data_storage.set_info_data('A code was sent to you on your email!!!')
                    self.page.go('password-manager/2steps')
                case 404:
                    self.create_notification('Account not found!!!', 'Not Found')
                case 401:
                    self.create_notification('The passwords does not matches!!!', 'Password Wrong')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

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

        _login_button = ElevatedButton(
            width=250,
            height=60,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
                bgcolor={"": '#9146ff', "hovered": '#481D85'}
            ),
            on_click=lambda e: login(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'Login',
                        size=25,
                        color='white',
                        weight=FontWeight.BOLD
                    )
                ]
            )
        )

        _forget_button = TextButton(
            text='Forget Password',
            autofocus=False,
            on_click=lambda e: forget_password(),
            style=ButtonStyle(
                bgcolor={
                    "": None,
                    "hovered": None},
                overlay_color={
                    "": None,
                    "hovered": None}
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
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        ExitButton(self.page)
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
                                                                    spacing=150,
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
                                                                            controls=[
                                                                                Column(
                                                                                    spacing=60,
                                                                                    controls=[
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
                                                                                                    Row(
                                                                                                        alignment=MainAxisAlignment.END,
                                                                                                        controls=[
                                                                                                            _forget_button
                                                                                                        ]
                                                                                                    ),

                                                                                                    Column(
                                                                                                        spacing=35,
                                                                                                        controls=[
                                                                                                            Row(
                                                                                                                alignment=MainAxisAlignment.CENTER,
                                                                                                                controls=[
                                                                                                                    _login_button
                                                                                                                ]
                                                                                                            ),

                                                                                                            Row(
                                                                                                                alignment=MainAxisAlignment.CENTER,
                                                                                                                controls=[
                                                                                                                    Column(
                                                                                                                        alignment=MainAxisAlignment.CENTER,
                                                                                                                        controls=[
                                                                                                                            Container(
                                                                                                                                width=200,
                                                                                                                                height=1,
                                                                                                                                bgcolor='#9146ff'
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    ),

                                                                                                                    Column(
                                                                                                                        alignment=MainAxisAlignment.CENTER,
                                                                                                                        controls=[
                                                                                                                            Text(
                                                                                                                                'Or',
                                                                                                                                size=15,
                                                                                                                                color='#9146ff',
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    ),

                                                                                                                    Column(
                                                                                                                        alignment=MainAxisAlignment.CENTER,
                                                                                                                        controls=[
                                                                                                                            Container(
                                                                                                                                width=200,
                                                                                                                                height=1,
                                                                                                                                bgcolor='#9146ff'
                                                                                                                            )
                                                                                                                        ]
                                                                                                                    )
                                                                                                                ]
                                                                                                            ),

                                                                                                            Row(
                                                                                                                alignment=MainAxisAlignment.CENTER,
                                                                                                                controls=[
                                                                                                                    ElevatedButton(
                                                                                                                        width=250,
                                                                                                                        height=60,
                                                                                                                        bgcolor='#111111',
                                                                                                                        style=ButtonStyle(
                                                                                                                            shape=RoundedRectangleBorder(
                                                                                                                                radius=10),
                                                                                                                            color={
                                                                                                                                "": '#9146ff',
                                                                                                                                "hovered": 'white'},
                                                                                                                            bgcolor={
                                                                                                                                "": '#111111',
                                                                                                                                "hovered": '#9146ff'},
                                                                                                                            overlay_color={
                                                                                                                                "": '#111111',
                                                                                                                                "hovered": '#9146ff'},
                                                                                                                            elevation={
                                                                                                                                "": 2,
                                                                                                                                "hovered": 2}
                                                                                                                        ),
                                                                                                                        on_click=lambda
                                                                                                                            e: self.page.go(
                                                                                                                            'password-manager/register'),
                                                                                                                        content=Row(
                                                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                                                            controls=[
                                                                                                                                Text(
                                                                                                                                    'Register',
                                                                                                                                    size=25,
                                                                                                                                    weight=FontWeight.BOLD
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