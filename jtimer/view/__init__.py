from importlib import resources

ADD_ICON = str(resources.path("images", "add.png"))
PLAY_ICON = str(resources.path("images", "play.png"))
PAUSE_ICON = str(resources.path("images", "pause.png"))
CHART_ICON = str(resources.path("images", "chart.png"))
DELETE_ICON = str(resources.path("images", "delete.png"))
STOPWATCH_ICON = str(resources.path("images", "timer.png"))

BACKGROUND_COLOR = "#242942"
BORDER_COLOR = "#464A63"

BOLD_LABEL_STYLE = f"border: 1px solid {BORDER_COLOR}; font-weight: bold;"
NORMAL_LABEL_STYLE = f"border: 1px solid {BORDER_COLOR}; font-weight: normal;"
