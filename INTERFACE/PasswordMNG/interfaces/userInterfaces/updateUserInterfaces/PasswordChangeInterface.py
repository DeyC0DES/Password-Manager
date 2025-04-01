from API.utils.CaptureToken import CaptureToken
from interfaces.A_components.ExitButton import ExitButton
from API.requests.UserRequest import UserRequest

from flet import *

from interfaces.A_components.NotificationContainer import NotificationContainer
from interfaces.A_components.ReturnButton import ReturnButton


class PasswordChangeInterface(UserControl):
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

        def change():
            import main

            self.add_load_screen()

            user_data = main.user_data_storage.get_user_data()
            email = user_data.get('email', 'unknown@NoHost')

            if _password_confirm_textField.value == '' or _password_confirm_textField.value == '':
                self.create_notification('The password fields is empty', 'Info')
                self.remove_load_screen()
                return

            if _password_textField.value == _password_confirm_textField.value:

                if email == 'unknown@NoHost' or email is None:
                    self.create_notification('Something went wrong with your email. Please rejoin', 'Error')
                    self.remove_load_screen()
                    return

                user_request = UserRequest()

                user_response = user_request.update_password(email, _password_textField.value, CaptureToken().capture())

                match user_response.status_code:
                    case 200:
                        main.info_data_storage.set_info_data('The password was changed with successfully!')
                        main.user_data_storage.clear()
                        self.page.go('password-manager/login')

                        try:
                            self.remove_load_screen()
                        except Exception:
                            pass
                    case 404:
                        self.create_notification('Something went wrong with your email. Please rejoin', 'Not found')
                    case _:
                        self.create_notification(f'Error: {user_response.status_code}')
                self.remove_load_screen()
                return

            self.create_notification('The passwords need be the same!', 'Unauthorized')
            self.remove_load_screen()

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

        _password_confirm_textField = TextField(
            width=500,
            password=True,
            can_reveal_password=True,
            text_size=25,
            border=InputBorder.UNDERLINE,
            border_width=3,
            border_color='#9146ff',
            color='white',
            hint_text='Confirm password',
            content_padding=padding.only(left=15, right=20)
        )

        _change_button = ElevatedButton(
            width=250,
            height=60,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
                bgcolor={"": '#9146ff', "hovered": '#481D85'}
            ),
            on_click=lambda e: change(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'Change',
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
                                                    height=650,
                                                    border_radius=20,
                                                    border=border.all(2, '#333333'),
                                                    alignment=alignment.center,
                                                    content=Row(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        controls=[
                                                            Container(
                                                                width=735,
                                                                height=630,
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
                                                                                    "Reset Password",
                                                                                    weight=FontWeight.BOLD,
                                                                                    color='white',
                                                                                    size=40
                                                                                )
                                                                            ]
                                                                        ),

                                                                        Column(
                                                                            spacing=100,
                                                                            controls=[
                                                                                Column(
                                                                                    spacing=60,
                                                                                    controls=[
                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _password_textField
                                                                                            ]
                                                                                        ),

                                                                                        Row(
                                                                                            alignment=MainAxisAlignment.CENTER,
                                                                                            controls=[
                                                                                                _password_confirm_textField
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
                                                                                                                    _change_button
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

                                self.loading_row,
                            ]
                        )
                    ),

                    self.notification_row
                ]
            )
        )

        return _main_container