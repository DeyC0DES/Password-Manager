from random import Random

import clipboard
from flet import *

from interfaces.A_components.NotificationContainer import NotificationContainer
from interfaces.A_components.ReturnButton import ReturnButton


class PasswordGeneratorInterface(UserControl):
    def __init__(self):
        super().__init__()
        self.notification_row = Row(alignment=MainAxisAlignment.END,controls=[])
        self.signs = False
        self.letters = False

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        notification_container.page.run_task(notification_container.progress_container_decree)

    def build(self):

        def go_back():
            self.signs = False
            self.letters = False

        def handle_click_active(button, types):

            if types == 'sign':
                self.signs = not self.signs
                button.bgcolor = '#9146ff' if self.signs else '#161616'
            else:
                self.letters = not self.letters
                button.bgcolor = '#9146ff' if self.letters else '#161616'

            button.update()

        def copy_to_clipboard():
            clipboard.copy(_password_textField.value)
            self.create_notification('Copy to clipboard successfully!!!', 'Success')

        def generate_password():
            letter = 'abcdefghijklmnopqrstuvwxyz'
            numbers = '1234567890'
            signs = '!@#$%^&*()-_=+[]{}|;:,.<>?/'

            alphabet = list(numbers)

            if self.letters:
                alphabet.extend(letter)

            if self.signs:
                alphabet.extend(signs)

            value = 0
            try:
                value = int(_limit_chars_textField.value)
            except ValueError:
                value = 15

            password = ''
            random = Random()
            while len(password) < value:
                password += random.choice(alphabet)

            _password_textField.value = password
            _password_textField.update()


        _password_textField = TextField(
            width=340,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Password',
            disabled=True,
            content_padding=padding.only(left=15, right=20)
        )

        _limit_chars_textField = TextField(
            width=100,
            text_size=25,
            border=None,
            border_width=0,
            border_color='Transparent',
            bgcolor='#333333',
            color='white',
            hint_text='Limit.',
            max_length=2,
            content_padding=padding.only(left=15, right=20)
        )

        _signs_button = ElevatedButton(
            width=100,
            height=47.5,
            bgcolor='#161616',
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
            ),
            on_click= lambda e: handle_click_active(_signs_button, 'sign'),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        '!#$',
                        size=25,
                        color='white',
                        weight=FontWeight.BOLD
                    )
                ]
            )
        )

        _letter_button = ElevatedButton(
            width=100,
            height=47.5,
            bgcolor='#161616',
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
            ),
            on_click=lambda e: handle_click_active(_letter_button, 'letter'),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(
                        'A-Z',
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
            padding=15,
            content=Stack(
                controls=[
                    Row(
                        controls=[
                            ReturnButton('password-manager/accounts', go_back)
                        ]
                    ),

                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        width=400,
                                        height=250,
                                        bgcolor='#262626',
                                        border_radius=20,
                                        padding=30,
                                        content=Column(
                                            spacing=25,
                                            controls=[
                                                Row(
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        _password_textField
                                                    ]
                                                ),

                                                Column(
                                                    controls=[
                                                        Row(
                                                            spacing=20,
                                                            controls=[
                                                                _limit_chars_textField,
                                                                _signs_button,
                                                                _letter_button
                                                            ]
                                                        ),

                                                        Row(
                                                            alignment=MainAxisAlignment.CENTER,
                                                            controls=[
                                                                ElevatedButton(
                                                                    width=250,
                                                                    height=50,
                                                                    style=ButtonStyle(
                                                                        shape=RoundedRectangleBorder(radius=10),
                                                                        bgcolor={"": '#9146ff', "hovered": '#481D85'}
                                                                    ),
                                                                    on_click= lambda e: generate_password(),
                                                                    content=Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            Text(
                                                                                'Generate',
                                                                                size=25,
                                                                                color='white',
                                                                                weight=FontWeight.BOLD
                                                                            )
                                                                        ]
                                                                    )
                                                                ),

                                                                ElevatedButton(
                                                                    width=50,
                                                                    height=50,
                                                                    bgcolor='#161616',
                                                                    style=ButtonStyle(
                                                                        shape=RoundedRectangleBorder(radius=10),
                                                                    ),
                                                                    on_click= lambda e: copy_to_clipboard(),
                                                                    content=Row(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        controls=[
                                                                            Icon(
                                                                                name=Icons.CONTENT_COPY,
                                                                                size=25,
                                                                                color='white'
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
                    ),

                    self.notification_row
                ]
            )
        )

        return _main_container