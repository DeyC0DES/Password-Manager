import asyncio

from flet import *
from fontTools.varLib.featureVars import buildGSUB


class AccountCardContainer(UserControl):
    def __init__(self, name, username, old_password, icon, func1, func2, fav, is_add_button):
        super().__init__()
        self.name = name
        self.username = username
        self.old_password = old_password
        self.icon = icon
        self.func1 = func1 if func1 is not None else self.handle_click
        self.icon_fav = icons.BOOKMARK_ROUNDED if fav else icons.BOOKMARK_BORDER_ROUNDED
        self.icon_fav_color = '#fdfd96' if fav else 'white'
        self.fav = fav
        self.add_button = is_add_button
        self.func2 = func2

    def handle_click(self):
        pass

    def build(self):

        def handle_bookmark_hover(e):
            if e.data == 'true':
                if self.fav:
                    _container.content.controls[0].controls[0].content.controls[0].icon_color = '#ff6961'
                    _container.content.controls[0].controls[0].content.controls[0].icon = icons.BOOKMARK_REMOVE_ROUNDED
                else:
                    _container.content.controls[0].controls[0].content.controls[0].icon_color = '#fdfd96'
                    _container.content.controls[0].controls[0].content.controls[0].icon = icons.BOOKMARK_ROUNDED
            else:
                if self.fav:
                    _container.content.controls[0].controls[0].content.controls[0].icon_color = '#fdfd96'
                    _container.content.controls[0].controls[0].content.controls[0].icon = icons.BOOKMARK_ROUNDED
                else:
                    _container.content.controls[0].controls[0].content.controls[0].icon_color = 'white'
                    _container.content.controls[0].controls[0].content.controls[0].icon = icons.BOOKMARK_BORDER_ROUNDED

            _container.update()

        def handler_container_hover(e):
            if e.data == 'true':
                _container.bgcolor = '#9146ff'
                # Add text to the column
                _text_row.controls.append(_text)
                # Changing the icon
                _container.content.controls[1].controls[0].controls[0].width = 120
                _container.content.controls[1].controls[0].controls[0].height = 120
                _container.content.controls[1].controls[0].controls[0].content.controls[0].size = 70
                _container.content.controls[1].controls[0].controls[0].content.controls[0].color = '#9146ff'
                # Changing bookmark
                if not self.add_button:
                    _container.content.controls[0].controls[0].bgcolor = '#9146ff'
                    _container.content.controls[0].controls[0].content.controls[0].visible = True
            else:
                _container.bgcolor = '#262626'
                # Add text to the column
                _text_row.controls.remove(_text)
                # Changing the icon
                _container.content.controls[1].controls[0].controls[0].width = 140
                _container.content.controls[1].controls[0].controls[0].height = 140
                _container.content.controls[1].controls[0].controls[0].content.controls[0].size = 100
                _container.content.controls[1].controls[0].controls[0].content.controls[0].color = '#333333'
                # Changing bookmark
                if not self.add_button:
                    _container.content.controls[0].controls[0].bgcolor = '#262626'
                    _container.content.controls[0].controls[0].content.controls[0].visible = False

            _container.update()

        def handle_bookmark_click():
            if self.fav:
                _bookmark_container.content.icon = icons.BOOKMARK_BORDER_ROUNDED
                _bookmark_container.content.icon_color = 'white'
                self.fav = False
            else:
                _bookmark_container.content.icon = icons.BOOKMARK_ROUNDED
                _bookmark_container.content.icon_color = '#fdfd96'
                self.fav = True

            self.update()
            self.func2(self.name, self.fav)

        _text = Text(
            self.name,
            size=27,
            color='white',
        )

        _text_row = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[

            ]
        )

        _bookmark_row = Row(
            alignment=MainAxisAlignment.START,
            controls=[

            ]
        )

        _bookmark_container = Container(
            width=60,
            height=60,
            bgcolor='#262626',
            animate=animation.Animation(500, AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: handle_bookmark_hover(e),
            content=Row(
                controls=[
                    IconButton(
                        icon=self.icon_fav,
                        icon_size=40,
                        icon_color=self.icon_fav_color,
                        width=60,
                        height=60,
                        animate_opacity=animation.Animation(500, AnimationCurve.EASE_IN_OUT),
                        visible=False,
                        on_click=lambda e: handle_bookmark_click(),
                    )
                ]
            )
        )

        if not self.add_button:
            _bookmark_row.controls.append(_bookmark_container)

        _container = Container(
            width=380,
            height=230,
            bgcolor='#262626',
            animate=animation.Animation(500, AnimationCurve.EASE_IN_OUT),
            border_radius=15,
            on_hover= lambda e: handler_container_hover(e),
            on_click= lambda e: self.func1(self.name, self.username,  self.icon, self.fav, self.old_password,),
            content=Stack(
                controls=[
                    _bookmark_row,

                    Column(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        width=140,
                                        height=140,
                                        bgcolor='#1a1a1a',
                                        border_radius=100,
                                        animate=animation.Animation(500, AnimationCurve.EASE_IN_OUT),
                                        alignment=alignment.center,
                                        content=Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            controls=[
                                                Icon(
                                                    name=self.icon,
                                                    size=100,
                                                    color='#333333',
                                                )
                                            ]
                                        )
                                    ),
                                ]
                            ),

                            _text_row
                        ]
                    )
                ]
            )
        )

        return _container