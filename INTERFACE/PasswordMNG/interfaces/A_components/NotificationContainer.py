import asyncio

from flet import *

class NotificationContainer(UserControl):
    def __init__(self, text, title):
        super().__init__()
        self.text = text
        self.title = title
        self.progress_container = Container()

    def destroy(self):
        self.parent.controls.remove(self)
        self.parent.update()

    async def progress_container_decree(self):
        while self.progress_container.width > 0:
            self.progress_container.width = self.progress_container.width - 1
            self.progress_container.update()

        await asyncio.sleep(2)

        try:
            self.destroy()
        except AttributeError:
            pass

    def build(self):
        self.progress_container = Container(
            width=500,
            height=5,
            bgcolor='#9146ff',
            animate=animation.Animation(2000, AnimationCurve.EASE_IN_OUT)
        )

        _container = Container(
            width=500,
            height=200,
            bgcolor='#1a1a1a',
            border_radius=20,
            padding=padding.only(right=10, top=10),
            visible=True,
            content=Stack(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(
                                self.title,
                                size=30,
                                color='#9146ff'
                            )
                        ]
                    ),

                    Row(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            IconButton(
                                icon=icons.CLOSE_ROUNDED,
                                icon_size=25,
                                icon_color='#ff6961',
                                on_click= lambda e: self.destroy()
                            )
                        ]
                    ),

                    Row(
                        controls=[
                            Container(
                                width=450,
                                height=175,
                                padding=30,
                                content=Row(
                                    controls=[
                                        Text(
                                            self.text,
                                            size=18,
                                        )
                                    ]
                                )
                            )
                        ]
                    ),

                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            Column(
                                alignment=MainAxisAlignment.END,
                                controls=[
                                    self.progress_container
                                ]
                            )
                        ]
                    )
                ]
            )
        )

        return Row(
                alignment=MainAxisAlignment.END,
                controls=[
                    Column(
                        alignment=MainAxisAlignment.END,
                        controls=[
                            _container
                        ]
                    )
                ]
            )