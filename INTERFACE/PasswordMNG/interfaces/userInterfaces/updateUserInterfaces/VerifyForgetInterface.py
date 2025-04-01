import json
import tracemalloc

from interfaces.A_components.NotificationContainer import NotificationContainer
from API.requests.UserRequest import UserRequest

from flet import *

from interfaces.A_components.ReturnButton import ReturnButton

tracemalloc.start()

class VerifyForgetInterface(UserControl):
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

    def create_notification(self, text = 'None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def send_code():
            import main

            self.add_load_screen()

            user_data = main.user_data_storage.get_user_data()
            email = user_data.get('email', 'unknown@NoHost')

            user_request = UserRequest()
            user_response = user_request.forget_password_verify(email, _code_textField.value)

            match user_response.status_code:
                case 200:
                    response = json.loads(user_response.content.decode('utf-8'))

                    main.user_data_storage.set_user_data(email, "Unknown", response.get('data', 'empty'))
                    self.page.go("password-manager/update/password")
                case 400:
                    self.create_notification("Code is invalid!", "Invalid")
                case 401:
                    self.create_notification("Code expired!", "Expired")
                case 404:
                    self.create_notification("The code dont exist!", "Invalid")
                case _:
                    self.create_notification(f'Error: {user_response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        _code_textField = TextField(
            width=240,
            text_size=40,
            bgcolor='#333333',
            border=None,
            border_width=0,
            border_radius=20,
            color='white',
            hint_text='code',
            content_padding=padding.only(left=15, right=15, top=15, bottom=15),
            text_align=TextAlign.CENTER,
            max_length=4
        )

        _send_button = ElevatedButton(
            width=240,
            height=70,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=20),
                bgcolor={'': '#262626', 'hovered': '#9146ff'}
            ),
            on_click=lambda e: send_code(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'SEND',
                        size=25,
                        color='white',
                        weight=FontWeight.BOLD
                    )
                ]
            )
        )

        _main_container = Container(
            width=1980,
            height=980,
            bgcolor='#111111',
            content=Stack(
                controls=[
                    Container(
                        width=1980,
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
                                                    width=500,
                                                    height=400,
                                                    bgcolor='#1a1a1a',
                                                    border_radius=20,
                                                    content=Row(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        controls=[
                                                            Column(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            _code_textField,
                                                                        ]
                                                                    ),

                                                                    Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            _send_button
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

                                self.loading_row,
                            ]
                        )
                    ),

                    self.notification_row
                ]
            )
        )

        return _main_container