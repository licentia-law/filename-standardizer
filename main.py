import sys
import os
import tkinter as tk

# --- PyInstaller 강제 인식용 import ---
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.scrolledtext
# ------------------------------------

from gui import App

if hasattr(sys, '_MEIPASS'):
    sys.path.append(sys._MEIPASS)

def main():
    """애플리케이션의 메인 진입점입니다."""
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()