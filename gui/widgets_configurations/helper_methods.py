from gui.widgets_configurations.button import BUTTON_CONFIG
from gui.widgets_configurations.copyright import COPYRIGHT_CONFIG
from gui.widgets_configurations.logo import LOGO_CONFIG_INIT, LOGO_CONFIG_ADVANCED


def set_button_configuration(btn, text):
    btn.configure(BUTTON_CONFIG)
    btn.configure(text=text)


def set_logo_configuration(logo, image):
    logo.configure(LOGO_CONFIG_INIT)
    logo.configure(image=image)
    logo.configure(LOGO_CONFIG_ADVANCED)


def set_copyright_configuration(copy_right):
    copy_right.configure(COPYRIGHT_CONFIG)