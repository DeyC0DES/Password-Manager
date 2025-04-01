from flet import *

from API.requests.UserRequest import UserRequest
from API.utils.CaptureToken import CaptureToken
from interfaces.A_components.NotificationContainer import NotificationContainer
from interfaces.A_components.ReturnButton import ReturnButton

class UserConfigInterface(UserControl):

    def __init__(self):
        super().__init__()
        self.username = None
        self.email = None
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

    def get_user_data(self):
        import main

        user_data = main.user_data_storage.get_user_data()

        if user_data is not None:
            self.username = user_data.get('username', 'Unknown')
            self.email = user_data.get('email', 'Unknown@NoHost')
        else:
            self.username = 'Failed!'
            self.email = 'Unknown@NoHost'

    def update_user_data(self, email = "Empty", username = "Default"):
        import main
        main.user_data_storage.set_user_data(email if email != "Empty" else self.email, username if username != "Default" else self.username, CaptureToken().capture())

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def change_fields_states():
            _username_textField.disabled = True if not _username_textField.disabled else False
            _username_textField.bgcolor = "#333333" if _username_textField.bgcolor == "#262626" else "#262626"
            _email_textField.disabled = True if not _email_textField.disabled else False
            _email_textField.bgcolor = "#333333" if _email_textField.bgcolor == "#262626" else "#262626"
            _username_textField.update()
            _email_textField.update()

        def update_account():

            self.add_load_screen()

            user_request = UserRequest()

            user_content = user_request.update_account(self.email, _username_textField.value, _email_textField.value, CaptureToken().capture())

            match user_content.status_code:
                case 200:
                    self.create_notification('Info updated with successfully!', 'Success')
                    self.update_user_data(self.email, _username_textField.value)
                case 202:
                    import main

                    main.update_user_storage.set_update_data(self.email, _username_textField.value, _email_textField.value)
                    main.info_data_storage.set_info_data('A code was sent on ur old email to confirm the change!')

                    self.update_user_data(self.email, _username_textField.value)
                    self.page.go('password-manager/accounts/settings/email_verify')
                case 401:
                    self.create_notification('Unauthorized change, please rejoin!', 'Unauthorized')
                case _:
                    self.create_notification(f'Error: {user_content.status_code}', 'Error')

            try:
                self.remove_load_screen()
            except Exception:
                pass

        def change_password():
            import main

            user_request = UserRequest()

            user_response = user_request.forget_password_request(self.email)

            match user_response.status_code:
                case 200:
                    main.user_data_storage.set_user_data(self.email, 'Unknown', 'None')
                    main.info_data_storage.set_info_data('A code was sent on your email!')

                    self.page.go('password-manager/forget/verify')
                case 404:
                    self.create_notification('Email not found!', 'Invalid')
                case _:
                    self.create_notification(f'Error: {user_response.status_code}', 'Error')

        def delete_user():

            self.add_load_screen()

            user_request = UserRequest()
            user_response = user_request.request_delete_code(self.email, CaptureToken().capture())

            match user_response.status_code:
                case 200:
                    self.page.go("password-manager/accounts/settings/delete")
                case 404:
                    self.create_notification("Something went wrong with the account!", "Not found")
                case 403:
                    self.create_notification("Something went wrong with the account!", "Forbidden")
                case _:
                    self.create_notification(f"Error: {user_response.status_code}", "Error")

            try:
                self.remove_load_screen()
            except Exception:
                pass


        self.get_user_data()

        _username_textField = TextField(
            label='Username',
            value=self.username,
            width=400,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#262626',
            color='white',
            disabled=True,
            content_padding=padding.only(left=15, right=20)
        )

        _email_textField = TextField(
            label='Email',
            value=self.email,
            width=400,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#262626',
            color='white',
            disabled=True,
            content_padding=padding.only(left=15, right=20)
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
                                        ReturnButton('password-manager/accounts')
                                    ]
                                ),

                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Text(
                                            f'Welcome, {self.username}',
                                            size=40,
                                            color='white',
                                            weight=FontWeight.BOLD
                                        )
                                    ]
                                ),

                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            controls=[
                                                Container(
                                                    width=650,
                                                    height=460,
                                                    bgcolor='#262626',
                                                    border_radius=20,
                                                    padding=15,
                                                    content=Row(
                                                        controls=[
                                                            Column(
                                                                spacing=30,
                                                                controls=[
                                                                    # Icon
                                                                    Row(
                                                                        controls=[
                                                                            Container(
                                                                                width=200,
                                                                                height=200,
                                                                                bgcolor='#333333',
                                                                                border_radius=15,
                                                                                alignment=alignment.center,
                                                                                content=Icon(
                                                                                    name=icons.ACCOUNT_BOX,
                                                                                    size=150,
                                                                                    color='#262626'
                                                                                )
                                                                            ),

                                                                            Column(
                                                                                controls=[
                                                                                    _username_textField,
                                                                                    _email_textField,

                                                                                    # Edit email/username fields
                                                                                    ElevatedButton(
                                                                                        width=400,
                                                                                        height=50,
                                                                                        style=ButtonStyle(
                                                                                            shape=RoundedRectangleBorder(
                                                                                                radius=10),
                                                                                            bgcolor={'': '#9146ff',
                                                                                                     'hovered': '#481D85'}
                                                                                        ),
                                                                                        on_click=lambda
                                                                                            e: change_fields_states(),
                                                                                        content=Text(
                                                                                            'Edit',
                                                                                            size=25,
                                                                                            color='white'
                                                                                        )
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    ),

                                                                    # upper line
                                                                    Container(
                                                                        width=610,
                                                                        height=2,
                                                                        bgcolor='#202020'
                                                                    ),

                                                                    # change password
                                                                    ElevatedButton(
                                                                        width=610,
                                                                        height=50,
                                                                        bgcolor='#161616',
                                                                        style=ButtonStyle(
                                                                            shape=RoundedRectangleBorder(radius=10),
                                                                        ),
                                                                        on_click= lambda e: change_password(),
                                                                        content=Text(
                                                                            'Change password',
                                                                            size=25,
                                                                            color='white'
                                                                        )
                                                                    ),

                                                                    # under line
                                                                    Container(
                                                                        width=610,
                                                                        height=2,
                                                                        bgcolor='#202020'
                                                                    ),

                                                                    Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            # Save button
                                                                            ElevatedButton(
                                                                                width=500,
                                                                                height=50,
                                                                                bgcolor='green',
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=10),
                                                                                ),
                                                                                on_click=lambda e: update_account(),
                                                                                content=Text(
                                                                                    'Save',
                                                                                    size=25,
                                                                                    color='white'
                                                                                )
                                                                            ),

                                                                            # delete button
                                                                            ElevatedButton(
                                                                                width=100,
                                                                                height=50,
                                                                                bgcolor='#161616',
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=10),
                                                                                ),
                                                                                on_click= lambda e: delete_user(),
                                                                                content=Icon(
                                                                                    name=Icons.DELETE_ROUNDED,
                                                                                    size=25,
                                                                                    color='white'
                                                                                )
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),

                                self.notification_row,
                            ]
                        )
                    ),

                    self.loading_row
                ]
            )
        )

        return _main_container