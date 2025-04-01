import asyncio

from flet import *

class LoadingScreen(UserControl):
    def __init__(self):
        super().__init__()
        self.animation_bool = True
        self.container_1 = None
        self.container_2 = None
        self.container_3 = None

    async def animation(self):

        async def activate_1():
            self.container_1.width = 50 if self.container_1.width == 35 else 35
            self.container_1.height = 50 if self.container_1.height == 35 else 35
            self.container_1.update()
            await asyncio.sleep(0.25)

        async def activate_2():
            self.container_2.width = 50 if self.container_2.width == 35 else 35
            self.container_2.height = 50 if self.container_2.height == 35 else 35
            self.container_2.update()
            await asyncio.sleep(0.25)

        async def activate_3():
            self.container_3.width = 50 if self.container_3.width == 35 else 35
            self.container_3.height = 50 if self.container_3.height == 35 else 35
            self.container_3.update()
            await asyncio.sleep(0.25)


        while self.animation_bool:
            await activate_1()
            await asyncio.sleep(0.25)
            await activate_2()
            await asyncio.sleep(0.25)
            await activate_3()

    def build(self):
        self.container_1 = Container(
            width=35,
            height=35,
            border_radius=100,
            bgcolor='#9146ff',
            animate=animation.Animation(250, AnimationCurve.EASE_IN_OUT)
        )

        self.container_2 = Container(
            width=35,
            height=35,
            border_radius=100,
            bgcolor='#9146ff',
            animate=animation.Animation(250, AnimationCurve.EASE_IN_OUT)
        )
        self.container_3 = Container(
            width=35,
            height=35,
            border_radius=100,
            bgcolor='#9146ff',
            animate=animation.Animation(250, AnimationCurve.EASE_IN_OUT)
        )


        _main_container = Container(
            width=1960,
            height=980,
            content=Stack(
                controls=[
                    Row(
                        alignment=MainAxisAlignment.START,
                        controls=[
                            Container(
                                width=1960,
                                height=980,
                                bgcolor='#000000',
                                opacity=0.75
                            )
                        ]
                    ),

                    Column(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    self.container_1,
                                    self.container_2,
                                    self.container_3
                                ]
                            )
                        ]
                    )

                ]
            )
        )

        return _main_container