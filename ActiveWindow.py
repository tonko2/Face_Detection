import win32gui
import ctypes

def foreground(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd,1)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        return False

win32gui.EnumWindows(foreground, 'Discord')