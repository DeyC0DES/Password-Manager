from flet import *

class MiniIconButton(UserControl):
    def __init__(self, color, icon, visible, func1):
        super().__init__()
        self.color = color
        self.icon = icon
        self.visible = visible
        self.func1 = func1

    def build(self):
        return ElevatedButton(
            width=50,
            height=50,
            visible=self.visible,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                bgcolor=self.color
            ),
            on_click= lambda e: self.func1(),
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=self.icon,
                        size=30,
                        color='white'
                    )
                ]
            )
        )