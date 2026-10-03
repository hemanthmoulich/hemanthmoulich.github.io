import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from pathlib import Path

# Main window
root = tk.Tk()
root.geometry("380x270")
root.resizable(False, False)
root.title("Wi-Fi Profile Exporter")

# Downloads folder for the current Windows user
DOWNLOADS = Path.home() / "Downloads"


def showmsg():
    try:
        # Ensure the destination folder exists
        DOWNLOADS.mkdir(parents=True, exist_ok=True)

        # Export Wi-Fi profiles without requesting clear-text keys
        result = subprocess.run(
            [
                "netsh",
                "wlan",
                "export",
                "profile",
                f"folder={DOWNLOADS}"
            ],
            capture_output=True,
            text=True,
            check=False,
            shell=False
        )

        if result.returncode == 0:
            messagebox.showinfo(
                "Export Complete",
                "Wi-Fi profile export finished.\n\n"
                f"Save location:\n{DOWNLOADS}\n\n"
                f"Result:\n{result.stdout.strip() or 'Command completed.'}\n\n"
                "Note: This does not request clear-text passwords."
            )
        else:
            messagebox.showerror(
                "Export Failed",
                result.stderr.strip()
                or result.stdout.strip()
                or "Windows could not export the profiles."
            )

    except OSError as error:
        messagebox.showerror("Error", str(error))


# Run button
button = tk.Button(
    root,
    text="Run",
    width=25,
    height=1,
    font=("Arial", 15),
    borderwidth=2,
    relief="solid",
    command=showmsg
)
button.place(x=55, y=140)

# Optional window icon
icon_path = Path(
    r"C:\Users\A1\Downloads\wifi-signal.png"
)

if icon_path.is_file():
    try:
        img = tk.PhotoImage(file=str(icon_path))
        root.iconphoto(False, img)
    except tk.TclError:
        pass

# Disclaimer
label = tk.Label(
    root,
    text="Disclaimer!!:",
    font=("Arial", 14),
    foreground="red"
)
label.place(x=127, y=20)

label1 = tk.Label(
    root,
    text="Do Not Touch Mouse, Keyboard",
    font=("Arial", 13)
)
label1.place(x=55, y=65)

label2 = tk.Label(
    root,
    text="During Run",
    font=("Arial", 13)
)
label2.place(x=134, y=92)

# Copyright
copyright_label = tk.Label(
    root,
    text="© Hemanth Tricks",
    foreground="red",
    font=("Arial", 10, "bold")
)
copyright_label.place(x=5, y=240)

# Destination information
label3 = tk.Label(
    root,
    text="Exports profiles to your Downloads folder",
    font=("Arial", 9),
    foreground="green"
)
label3.place(x=40, y=195)

root.mainloop()
