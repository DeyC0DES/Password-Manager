from flet import *

class ReturnButton(UserControl):
    def __init__(self, path = 'password-manager/login', func = None):
        super().__init__()
        self.path = path
        self.func = func

    def build(self):

        def click_func():
            self.page.go(self.path)

            if self.func is not None:
                self.func()

        _button = ElevatedButton(
            width=60,
            height=60,
            bgcolor='#333333',
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            ),
            on_click= lambda e: click_func(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Icon(
                        icons.ARROW_BACK,
                        size=35,
                        color='white'
                    )
                ]
            ),
        )

        return _button