import json
import tracemalloc

from flet import *

from API.requests.AccountRequests import AccountRequests
from API.utils.CaptureToken import CaptureToken
from interfaces.A_components.AccountCardContainer import AccountCardContainer
from interfaces.A_components.NotificationContainer import NotificationContainer

tracemalloc.start()

# noinspection PyTypeChecker
class AccountsInterface(UserControl):
    def __init__(self):
        super().__init__()
        self.notification_row = Row(alignment=MainAxisAlignment.END,controls=[])
        self.account_card_column = Column(alignment=MainAxisAlignment.START, horizontal_alignment=CrossAxisAlignment.START, scroll=ScrollMode.ALWAYS, controls=[])
        self.sort = False
        self.only_fav = False
        self.main_container = None
        self.accounts = None
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

    def create_notification(self, text='None', title = 'Unknown'):
        notification_container = NotificationContainer(text, title)
        self.notification_row.controls.append(notification_container)
        self.notification_row.update()
        self.page.run_task(notification_container.progress_container_decree)

    def makes_visible_false(self):
        self.main_container.content.controls[0].content.controls[1].controls[0].controls[0].visible = False

    def clean_account_column(self):
        self.account_card_column.controls.clear()

    def get_accounts(self):
        account_requests = AccountRequests()
        response_content = account_requests.get_accounts(CaptureToken().capture())
        accounts = json.loads(response_content.content.decode('utf-8'))
        return accounts.get('data', '')

    def verify_notification(self):
        import main

        try:
            message = main.info_data_storage.get_info_data().get('content', None)
        except AttributeError:
            return

        main.info_data_storage.clear()

        if message is None:
            return

        self.create_notification(message, 'Info')

    def change_route(self, name, username, icon, fav = False, old_password = 'Empty'):

        import main

        if username is not None:
            main.account_data_storage.set_account_data(name, username, fav, old_password, icon)

        if name == 'Add':
            self.page.go('password-manager/accounts/create')
        else:
            self.page.go('password-manager/accounts/edit')

    def show_fav_accounts(self):
        self.only_fav = not self.only_fav
        self.create_account_cards()

    def show_az(self):
        self.sort = True
        self.create_account_cards()

    def show_all(self):
        self.sort = False
        self.only_fav = False
        self.create_account_cards()

    def create_account_cards(self, search_value = None):

        def handle_fav_click(name, fav):
            account_request = AccountRequests()
            response = account_request.update_fav_account(name, fav, CaptureToken().capture())

        def add_account_card(name = 'Unknown', icon = 'HELP', old_password = 'Empty', username = None, fav = False, is_add_button = False):
            if not self.account_card_column.controls or len(self.account_card_column.controls[-1].controls) == 4:
                new_row = Row(controls=[])
                self.account_card_column.controls.append(new_row)

            self.account_card_column.controls[-1].controls.append(AccountCardContainer(name, username, old_password, icon, self.change_route, handle_fav_click, fav, is_add_button))
            self.account_card_column.update()

        self.add_load_screen()

        self.account_card_column.controls.clear()

        if self.sort:
            self.accounts.sort(key=lambda x: x['accountName'])
        else:
            self.accounts = self.get_accounts()

        if len(self.accounts) > 0:
            for i in range(len(self.accounts)):
                account_name = self.accounts[i].get('accountName', 'Unknown')

                if self.only_fav:
                    if self.accounts[i].get('favorite', False):
                        if search_value is not None:
                            if account_name.__contains__(search_value):
                                add_account_card(account_name, self.accounts[i].get('icon', 'HELP'),
                                                 self.accounts[i].get('oldAccountPassword', 'Empty'),
                                                 self.accounts[i].get('accountUserName', None),
                                                 self.accounts[i].get('favorite', False))
                        else:
                            add_account_card(account_name, self.accounts[i].get('icon', 'HELP'),
                                             self.accounts[i].get('oldAccountPassword', 'Empty'),
                                             self.accounts[i].get('accountUserName', None),
                                             self.accounts[i].get('favorite', False))
                else:
                    if search_value is not None:
                        if account_name.__contains__(search_value):
                            add_account_card(self.accounts[i].get('accountName', 'Unknown'), self.accounts[i].get('icon', 'HELP'),
                                            self.accounts[i].get('oldAccountPassword', 'Empty'),
                                            self.accounts[i].get('accountUserName', None), self.accounts[i].get('favorite', False))
                    else:
                        add_account_card(account_name, self.accounts[i].get('icon', 'HELP'),
                                         self.accounts[i].get('oldAccountPassword', 'Empty'),
                                         self.accounts[i].get('accountUserName', None),
                                         self.accounts[i].get('favorite', False))

        add_account_card('Add', 'ADD', is_add_button=True)

        self.remove_load_screen()

    def build(self):

        def handle_change_search():
            self.create_account_cards(_search_bar.value)

        def logout():
            import main
            main.user_data_storage.clear()
            main.info_data_storage.clear()

            self.page.go("password-manager/login")


        _search_bar = TextField(
            width=700,
            border_radius=20,
            border_color='Transparent',
            border_width=0,
            border=None,
            content_padding=padding.only(left=25, top=15, bottom=15),
            hint_text='Search',
            text_size=25,
            bgcolor='#333333',
            on_change= lambda e: handle_change_search()
        )

        self.main_container = Container(
            width=1960,
            height=980,
            bgcolor='#111111',
            padding=0,
            content=Stack(
                controls=[
                    Container(
                        width=1960,
                        height=980,
                        content=Stack(
                            controls=[
                                Column(
                                    spacing=0,
                                    expand=True,
                                    alignment=MainAxisAlignment.START,
                                    controls=[
                                        # top board
                                        Container(
                                            width=1960,
                                            height=100,
                                            bgcolor='#262626',
                                            padding=padding.only(right=25),
                                            alignment=alignment.center,
                                            content=Stack(
                                                controls=[
                                                    Row(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        controls=[
                                                            Column(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    _search_bar
                                                                ]
                                                            )
                                                        ]
                                                    ),

                                                    Row(
                                                        alignment=MainAxisAlignment.END,
                                                        controls=[
                                                            Column(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Container(
                                                                        width=70,
                                                                        height=70,
                                                                        border_radius=100,
                                                                        bgcolor='#9146ff',
                                                                        alignment=alignment.center,
                                                                        padding=0,
                                                                        content=PopupMenuButton(
                                                                            icon=icons.ACCOUNT_BOX,
                                                                            icon_size=50,
                                                                            icon_color='#333333',
                                                                            width=70,
                                                                            height=70,
                                                                            items=[
                                                                                PopupMenuItem(
                                                                                    icon=icons.SETTINGS_ROUNDED,
                                                                                    text='Account',
                                                                                    on_click=lambda e: self.page.go(
                                                                                        'password-manager/accounts/settings')),
                                                                                PopupMenuItem(icon=icons.EXIT_TO_APP,
                                                                                              text='Exit',
                                                                                              on_click=lambda
                                                                                                  e: logout())
                                                                            ]
                                                                        )
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),

                                        Row(
                                            alignment=MainAxisAlignment.START,
                                            spacing=0,
                                            controls=[
                                                # dashboard
                                                Container(
                                                    width=300,
                                                    height=900,
                                                    border=border.only(right=BorderSide(2, '#333333')),
                                                    padding=padding.only(top=5),
                                                    content=Column(
                                                        spacing=25,
                                                        controls=[
                                                            # Buttons
                                                            Row(
                                                                alignment=MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    Column(
                                                                        alignment=MainAxisAlignment.CENTER,
                                                                        spacing=15,
                                                                        controls=[
                                                                            ElevatedButton(
                                                                                width=280,
                                                                                height=50,
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=10),
                                                                                    bgcolor={'': '#111111',
                                                                                             'hovered': '#262626'},
                                                                                    overlay_color={'': '#111111',
                                                                                                   'hovered': '#262626'}
                                                                                ),
                                                                                on_click=lambda e: self.show_all(),
                                                                                content=Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        Icon(
                                                                                            name=icons.MENU,
                                                                                            size=25,
                                                                                            color='white'
                                                                                        ),

                                                                                        Text(
                                                                                            'All',
                                                                                            size=25,
                                                                                            color='white'
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ),

                                                                            ElevatedButton(
                                                                                width=280,
                                                                                height=50,
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=10),
                                                                                    bgcolor={'': '#111111',
                                                                                             'hovered': '#262626'},
                                                                                    overlay_color={'': '#111111',
                                                                                                   'hovered': '#262626'}
                                                                                ),
                                                                                on_click=lambda
                                                                                    e: self.show_fav_accounts(),
                                                                                content=Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        Icon(
                                                                                            name=icons.BOOKMARK,
                                                                                            size=25,
                                                                                            color='white'
                                                                                        ),

                                                                                        Text(
                                                                                            'Bookmark',
                                                                                            size=25,
                                                                                            color='white'
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ),

                                                                            ElevatedButton(
                                                                                width=280,
                                                                                height=50,
                                                                                style=ButtonStyle(
                                                                                    shape=RoundedRectangleBorder(
                                                                                        radius=10),
                                                                                    bgcolor={'': '#111111',
                                                                                             'hovered': '#262626'},
                                                                                    overlay_color={'': '#111111',
                                                                                                   'hovered': '#262626'}
                                                                                ),
                                                                                on_click=lambda e: self.show_az(),
                                                                                content=Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        Icon(
                                                                                            name=Icons.TEXT_FIELDS,
                                                                                            size=25,
                                                                                            color='white'
                                                                                        ),

                                                                                        Text(
                                                                                            'A-Z',
                                                                                            size=25,
                                                                                            color='white'
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            ),

                                                            # Alt Button
                                                            Row(
                                                                controls=[
                                                                    Container(
                                                                        width=300,
                                                                        height=80,
                                                                        border=border.only(top=BorderSide(2, '#333333'),
                                                                                           bottom=BorderSide(2,
                                                                                                             '#333333')),
                                                                        content=Column(
                                                                            alignment=MainAxisAlignment.CENTER,
                                                                            controls=[
                                                                                Row(
                                                                                    alignment=MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        ElevatedButton(
                                                                                            width=280,
                                                                                            height=50,
                                                                                            style=ButtonStyle(
                                                                                                shape=RoundedRectangleBorder(
                                                                                                    radius=10),
                                                                                                bgcolor={'': '#111111',
                                                                                                         'hovered': '#262626'},
                                                                                                overlay_color={
                                                                                                    '': '#111111',
                                                                                                    'hovered': '#262626'}
                                                                                            ),
                                                                                            on_click=lambda
                                                                                                e: self.page.go(
                                                                                                'password-manager/accounts/pwdgen'),
                                                                                            content=Row(
                                                                                                alignment=MainAxisAlignment.CENTER,
                                                                                                controls=[
                                                                                                    Icon(
                                                                                                        name=icons.LOCK_ROUNDED,
                                                                                                        size=25,
                                                                                                        color='white'
                                                                                                    ),

                                                                                                    Text(
                                                                                                        'Generator',
                                                                                                        size=25,
                                                                                                        color='white'
                                                                                                    )
                                                                                                ]
                                                                                            )
                                                                                        ),
                                                                                    ]
                                                                                )
                                                                            ]
                                                                        )
                                                                    )
                                                                ]
                                                            ),
                                                        ]
                                                    )
                                                ),

                                                Column(
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Container(
                                                            width=1650,
                                                            height=900,
                                                            padding=20,
                                                            content=self.account_card_column
                                                        )
                                                    ]
                                                ),

                                            ]
                                        )
                                    ]
                                ),

                                Row(
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        Column(
                                            alignment=MainAxisAlignment.END,
                                            controls=[
                                                Container(
                                                    width=550,
                                                    height=250,
                                                    padding=15,
                                                    content=Row(
                                                        alignment=MainAxisAlignment.END,
                                                        controls=[
                                                            Column(
                                                                alignment=MainAxisAlignment.END,
                                                                controls=[
                                                                    self.notification_row
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        )
                    ),

                    self.loading_row
                ]
            )
        )

        return self.main_container