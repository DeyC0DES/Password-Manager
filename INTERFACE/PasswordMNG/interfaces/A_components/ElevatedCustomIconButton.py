from flet import *

class ElevatedCustomIconButton(UserControl):
    def __init__(self, icon, func):
        super().__init__()
        self.icon = icon
        self.func = func

    def build(self):
        return ElevatedButton(
            width=50,
            height=50,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=20),
                bgcolor={'': '#262626', 'hovered': '#181818'},
                overlay_color={'': '#262626', 'hovered': '#181818'},
                color='white'
            ),
            on_click= lambda e: self.func(self.icon),
            content=Icon(
                name=self.icon
            )
        )