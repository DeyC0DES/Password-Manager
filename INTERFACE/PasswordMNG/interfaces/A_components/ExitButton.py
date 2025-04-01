from flet import *

class ExitButton(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):

        def click_func():
            self.page.window.close()


        return ElevatedButton(
            width=60,
            height=60,
            bgcolor='#ff6961',
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10),
            ),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Icon(
                        icons.EXIT_TO_APP,
                        size=35,
                        color='white'
                    )
                ]
            ),
            on_click= lambda e: click_func()
        )