import json
import tracemalloc

from interfaces.A_components.NotificationContainer import NotificationContainer
from API.requests.UserRequest import UserRequest

from flet import *

from interfaces.A_components.ReturnButton import ReturnButton

tracemalloc.start()

class StepsVerificationInterface(UserControl):
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

        def clear_storage():
            import main
            main.user_data_storage.clear()

        def request_new_code():

            self.add_load_screen()

            user_data = self.page.client_storage.get("user_data")
            email = user_data.get("email", "Unknown")

            user_request = UserRequest()
            response = user_request.request_code(email)

            match response.status_code:
                case 200:
                    self.create_notification('A new code was sent to you on your email!!!', 'New code request!')
                case 404:
                    self.create_notification('Some error occurred while verification, please login again!!!', 'Error')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        def do_login():
            import main

            self.add_load_screen()

            code = _code_textField.value

            user_data = main.user_data_storage.get_user_data()
            email = user_data.get("email", "Unknown")

            user_request = UserRequest()
            response = user_request.steps_verify(email, code)

            match response.status_code:
                case 200:
                    self.page.client_storage.clear()

                    response_content = json.loads(response.content.decode('utf-8'))

                    token = response_content.get('message', 'empty')
                    username = response_content.get('data', 'Unknown')
                    main.user_data_storage.set_user_data(email, username, token)
                    main.info_data_storage.set_info_data('Login completed successfully!!!')

                    self.page.go('password-manager/accounts')
                case 400:
                    self.create_notification('Code is invalid!!!', 'Invalid!')
                case 401:
                    self.create_notification('Code is expired!!!', 'Expired!')
                case _:
                    self.create_notification(f'Error: {response.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        _code_textField = TextField(
            width=150,
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
            on_click=lambda e: do_login(),
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

        _request_code_button = ElevatedButton(
            width=80,
            height=80,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=20),
                bgcolor={'': '#262626', 'hovered': '#9146ff'},
            ),
            on_click=lambda e: request_new_code(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Icon(
                        icons.LOOP_ROUNDED,
                        size=40,
                        color='white'
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
                                        ReturnButton('password-manager/login', clear_storage)
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
                                                                        controls=[
                                                                            _code_textField,
                                                                            _request_code_button
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

                                self.notification_row
                            ]
                        )
                    ),

                    self.loading_row,
                ]
            )
        )

        return _main_container