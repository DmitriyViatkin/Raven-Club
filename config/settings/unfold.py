from django.urls import reverse_lazy

UNFOLD = {
    "SITE_HEADER": "Raven Club Administration",
    "SITE_TITLE": "Raven Club Panel",
    "SITE_SYMBOL": "sports_soccer",
    "SHOW_HISTORY": True,

    "SITE_DROPDOWN": [
        {
            "icon": "open_in_new",
            "title": "Відкрити сайт",
            "link": "http://127.0.0.1:8000/",
            "attrs": {"target": "_blank"},
        },
        {
            "icon": "home",
            "title": "Головна адмінки",
            "link": reverse_lazy("admin:index"),
        },
    ],

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,

        "navigation": [
            {
                "title": "Управление",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Игроки (Players)",
                        "icon": "people",
                        "link": reverse_lazy("admin:users_player_changelist"),
                    },
                    {
                        "title": "Группы и права",
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "Лиги и Турниры",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Все лиги",
                        "icon": "emoji_events",
                        "link": reverse_lazy("admin:leagues_league_changelist"),
                    },
                    {
                        "title": "Участники лиг",
                        "icon": "groups",
                        "link": reverse_lazy("admin:leagues_leaguemember_changelist"),
                    },
                    {
                        "title": "Правила начисления",
                        "icon": "gavel",
                        "link": reverse_lazy("admin:leagues_scoringrules_changelist"),
                    },
                ],
            },
            {
                "title": "Матчи и Счета",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Результаты матчей",
                        "icon": "scoreboard",
                        # Исправлено: заменили leagues на results
                        "link": reverse_lazy("admin:results_matchresult_changelist"),
                    },
                ],
            },
        ],
    },

    "COLORS": {
        "primary": {
            "50": "250 250 250",
            "100": "244 244 245",
            "200": "228 228 231",
            "300": "212 212 216",
            "400": "161 161 170",
            "500": "113 113 122",
            "600": "82 82 91",
            "700": "63 63 70",
            "800": "39 39 42",
            "900": "24 24 27",
            "950": "9 9 11",
        }
    },
}