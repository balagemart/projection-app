DARK_THEME = """
/* GLOBAL BASE */
QMainWindow {
    background-color: #2b2b2b;
}

QWidget {
    color: #dddddd;
}

/* LAYOUT AREAS */
#LeftPanel {
    background-color: #353535;
    border-right: 1px solid #444;
}

#RightPane {
    background-color: #2e2e2e;
}

#TopBar {
    background-color: #3a3a3a;
    border-bottom: 1px solid #444;
}

#Viewport {
    background-color: #1e1e1e;
}


/* MENU BAR */
QMenuBar {
    background-color: #2b2b2b;
}

QMenuBar::item {
    padding: 4px 10px;
}

QMenuBar::item:selected {
    background: #444;
}


/* DROPDOWN MENUS */
QMenu {
    background-color: #353535;
    border: 1px solid #444;
}

QMenu::item:selected {
    background-color: #555;
}


/* TOOL BUTTONS (TopBar) */
#TopBar QToolButton {
    background-color: #454545;
    border: 1px solid #555;
    padding: 4px 8px;
}

#TopBar QPushButton {
    background-color: #454545;
    border: 1px solid #555;
    padding: 4px 8px;
}

#TopBar QToolButton:hover {
    background-color: #5a5a5a;
}

#TopBar QToolButton::menu-indicator {
    image: none;
}


/* PUSH BUTTONS (Left panel) */
#LeftPanel QPushButton {
    background-color: #454545;
    border: 1px solid #555;
    padding: 4px;
}

#LeftPanel QPushButton:hover {
    background-color: #5a5a5a;
}

/* LIST WIDGET */
#LeftPanel QListWidget {
    background-color: #2f2f2f;
    border: 1px solid #444;
}

#LeftPanel QListWidget::item {
    padding: 4px;
}

#LeftPanel QListWidget::item:selected {
    background-color: #555;
}


/* PROPERTY AREA (spinboxok stb) */
#LeftPanel QDoubleSpinBox,
#LeftPanel QSpinBox,
#LeftPanel QLineEdit {
    background-color: #2f2f2f;
    border: 1px solid #444;
    padding: 2px;
}


/* SPINBOX BUTTONS */
#LeftPanel QAbstractSpinBox::up-button,
#LeftPanel QAbstractSpinBox::down-button {
    background-color: #454545;
    border-left: 1px solid #555;
}

#LeftPanel QAbstractSpinBox::up-button:hover,
#LeftPanel QAbstractSpinBox::down-button:hover {
    background-color: #5a5a5a;
}
"""
