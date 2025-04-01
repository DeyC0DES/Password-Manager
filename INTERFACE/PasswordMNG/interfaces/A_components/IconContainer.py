from flet import *

from interfaces.A_components.ElevatedCustomIconButton import ElevatedCustomIconButton

class IconContainer(UserControl):
    def __init__(self, func1, icon_name = "ACCOUNT_CIRCLE"):
        super().__init__()
        self.func1 = func1
        self.icon = Icon(name=icon_name, color='#262626', size=150)

    def build(self):

        def handle_icon_container_hover(e):
            if e.data == 'true':
                _icon_container.bgcolor = "#222222"
                self.icon.color = "#161616"
            else:
                _icon_container.bgcolor = "#333333"
                self.icon.color = "#262626"

            _icon_container.update()

        _icon_container = Container(
            width=200,
            height=200,
            bgcolor='#333333',
            border_radius=20,
            alignment=alignment.center,
            animate=animation.Animation(200, AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: handle_icon_container_hover(e),
            on_click=lambda e: self.page.run_task(self.func1),
            content=self.icon
        )

        return _icon_container