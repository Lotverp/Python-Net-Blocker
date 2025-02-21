import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import psutil
import os
import threading
from pathlib import Path
from ttkbootstrap import Style
from typing import Optional, Any
import webbrowser
import locale

# Dizionario per le traduzioni in diverse lingue
translations = {
    'en': {
        'title': "Python Net Blocker",
        'search_label': "Search:",
        'search_placeholder': "Search...",
        'consentito': "✅ Allowed",
        'bloccato': "❌ Blocked",
        'block': "Block",
        'unblock': "Unblock",
        'unblock_all': "Unblock All",
        'refresh': "Refresh",
        'add_app': "Add App",
        'sort': "Sort: None",
        'warning_title': "Warning",
        'warning_select_app': "Select an application!",
        'success_title': "Success",
        'success_block': "{} blocked!",
        'error_title': "Error",
        'error_block': "Unable to create rule (administrator?)",
        'success_unblock': "{} unblocked!",
        'error_unblock': "Rule not found or insufficient permissions",
        'info_title': "Info",
        'info_no_rule': "No rule to remove.",
        'success_unblock_all': "All applications have been unblocked!",
        'error_unblock_all': "Unable to unblock the following: {}",
        'select_executable': "Select an executable",
        'file_exe': "Executable Files",
        'all_files': "All Files",
        'language': "Language",
        'theme': "Theme",
        'light': "Light",
        'dark': "Dark",
        'app_name': "Application Name",
        'path': "Path",
        'status': "Status",
        'github': "GitHub",
        'donate': "Donate"
    },
    'it': {
        'title': "Python Net Blocker",
        'search_label': "Cerca:",
        'search_placeholder': "Cerca...",
        'consentito': "✅ Consentito",
        'bloccato': "❌ Bloccato",
        'block': "Blocca",
        'unblock': "Sblocca",
        'unblock_all': "Sblocca Tutti",
        'refresh': "Aggiorna",
        'add_app': "Aggiungi App",
        'sort': "Ordinamento: Nessuno",
        'warning_title': "Attenzione",
        'warning_select_app': "Seleziona un'applicazione!",
        'success_title': "Successo",
        'success_block': "{} bloccata!",
        'error_title': "Errore",
        'error_block': "Impossibile creare la regola (amministratore?)",
        'success_unblock': "{} sbloccata!",
        'error_unblock': "Regola non trovata o permessi insufficienti",
        'info_title': "Info",
        'info_no_rule': "Nessuna regola da rimuovere.",
        'success_unblock_all': "Tutte le applicazioni sono state sbloccate!",
        'error_unblock_all': "Impossibile sbloccare i seguenti: {}",
        'select_executable': "Seleziona un'eseguibile",
        'file_exe': "File eseguibili",
        'all_files': "Tutti i file",
        'language': "Lingua",
        'theme': "Tema",
        'light': "Chiaro",
        'dark': "Scuro",
        'app_name': "Nome Applicazione",
        'path': "Percorso",
        'status': "Stato",
        'github': "GitHub",
        'donate': "Donate"
    },
    # ... (altre lingue: 'es', 'fr', 'de', 'pt', 'ru', 'zh', 'ja', 'ko' – omesse per brevità)
}

# Mappa per i nomi visualizzati delle lingue
display_names = {
    'en': "English",
    'it': "Italiano",
    'es': "Español",
    'fr': "Français",
    'de': "Deutsch",
    'pt': "Português",
    'ru': "Русский",
    'zh': "中文",
    'ja': "日本語",
    'ko': "한국어"
}

def get_system_language() -> str:
    default = "en"
    try:
        sys_locale = locale.getdefaultlocale()[0]  # es. "en_US"
        if sys_locale:
            lang = sys_locale.split('_')[0]
            if lang in translations:
                return lang
    except Exception:
        pass
    return default

class NetBlockerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        # Imposta la lingua di default in base al sistema
        self.current_language = get_system_language()
        self.current_theme = "darkly"  # tema scuro di default
        self.style = Style(theme=self.current_theme)
        self.root.title(translations[self.current_language]['title'])
        self.root.geometry("800x600")

        # Pannello superiore: selezione lingua e frame per pulsanti GitHub, Donate e tema
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.language_label = tk.Label(self.top_frame, text=translations[self.current_language]['language'] + ":")
        self.language_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.language_var = tk.StringVar(value=display_names[self.current_language])
        self.language_combobox = ttk.Combobox(
            self.top_frame, textvariable=self.language_var,
            values=[display_names[code] for code in display_names],
            state="readonly", width=10
        )
        self.language_combobox.pack(side=tk.LEFT)
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)
        
        # Frame per i pulsanti sulla destra
        self.top_right_frame = tk.Frame(self.top_frame)
        self.top_right_frame.pack(side=tk.RIGHT)
        
        self.github_button = ttk.Button(
            self.top_right_frame,
            text="🌐 " + translations[self.current_language]['github'],
            command=self.open_github,
            bootstyle="primary",
            padding=(12, 8)
        )
        self.github_button.pack(side=tk.LEFT, padx=5)
        
        self.donate_button = ttk.Button(
            self.top_right_frame,
            text="💰 " + translations[self.current_language]['donate'],
            command=self.open_donate,
            bootstyle="success",
            padding=(12, 8)
        )
        self.donate_button.pack(side=tk.LEFT, padx=5)
        
        self.theme_button = ttk.Button(
            self.top_right_frame,
            text="🎨 " + translations[self.current_language]['theme'] + ": " + translations[self.current_language]['dark'],
            command=self.toggle_theme,
            bootstyle="info",
            padding=(12, 8)
        )
        self.theme_button.pack(side=tk.LEFT, padx=5)

        # Barra di ricerca con etichetta a sinistra (con emoji lente)
        self.search_frame = tk.Frame(root)
        self.search_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.search_label = tk.Label(self.search_frame, text="🔍 " + translations[self.current_language]['search_label'])
        self.search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        self.btn_clear_search = ttk.Button(self.search_frame, text="❌", command=self.clear_search, bootstyle="secondary", padding=(6, 4))
        self.btn_clear_search.pack(side=tk.LEFT, padx=5)

        # Etichetta per l'ordinamento
        self.sort_label = tk.Label(root, text=translations[self.current_language]['sort'], font=("Arial", 10))
        self.sort_label.pack(pady=5)

        # Configurazione della Treeview:
        # Le colonne "Name" e "Path" hanno larghezze fisse mentre "Status" si espande per occupare lo spazio residuo (quindi rimane a destra)
        self.app_list = ttk.Treeview(root, columns=("Name", "Path", "Status"), show="headings")
        self.app_list.heading("Name", text=translations[self.current_language]['app_name'], command=lambda: self.sort_column("Name", False))
        self.app_list.heading("Path", text=translations[self.current_language]['path'], command=lambda: self.sort_column("Path", False))
        self.app_list.heading("Status", text=translations[self.current_language]['status'], anchor="w", command=lambda: self.sort_column("Status", False))
        self.app_list.column("Name", anchor="w", width=250, stretch=False)
        self.app_list.column("Path", anchor="w", width=350, stretch=False)
        self.app_list.column("Status", anchor="w", width=150, stretch=True)
        self.app_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pulsanti inferiori (usiamo ttk.Button per un look uniforme)
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.btn_block = ttk.Button(self.btn_frame, text="🔒 " + translations[self.current_language]['block'],
                                    command=self.block_app, bootstyle="danger", padding=(12, 8))
        self.btn_block.pack(side=tk.LEFT, padx=5)

        self.btn_unblock = ttk.Button(self.btn_frame, text="🔓 " + translations[self.current_language]['unblock'],
                                      command=self.unblock_app, bootstyle="info", padding=(12, 8))
        self.btn_unblock.pack(side=tk.LEFT, padx=5)

        # Il tasto "Unblock All" ora itera su tutti gli elementi e rimuove la regola per ciascuno
        self.btn_unblock_all = ttk.Button(self.btn_frame, text="🚫 " + translations[self.current_language]['unblock_all'],
                                          command=self.unblock_all_apps, bootstyle="warning", padding=(12, 8))
        self.btn_unblock_all.pack(side=tk.LEFT, padx=5)

        self.btn_refresh = ttk.Button(self.btn_frame, text="💡 " + translations[self.current_language]['refresh'],
                                      command=self.refresh_apps, bootstyle="secondary", padding=(12, 8))
        self.btn_refresh.pack(side=tk.LEFT, padx=5)

        self.btn_add = ttk.Button(self.btn_frame, text="➕ " + translations[self.current_language]['add_app'],
                                  command=self.add_app, bootstyle="success", padding=(12, 8))
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.current_sort_column: Optional[str] = None
        self.sort_ascending: bool = False

        self.refresh_apps()

    def update_ui_texts(self) -> None:
        t = translations[self.current_language]
        self.root.title(t['title'])
        self.language_label.config(text=t['language'] + ":")
        self.search_label.config(text="🔍 " + t['search_label'])
        theme_text = t['dark'] if self.current_theme == "darkly" else t['light']
        self.theme_button.config(text="🎨 " + t['theme'] + ": " + theme_text)
        self.sort_label.config(text=t['sort'])
        self.btn_block.config(text="🔒 " + t['block'])
        self.btn_unblock.config(text="🔓 " + t['unblock'])
        self.btn_unblock_all.config(text="🚫 " + t['unblock_all'])
        self.btn_refresh.config(text="💡 " + t['refresh'])
        self.btn_add.config(text="➕ " + t['add_app'])
        self.github_button.config(text="🌐 " + t['github'])
        self.donate_button.config(text="💰 " + t['donate'])
        self.app_list.heading("Name", text=t['app_name'], command=lambda: self.sort_column("Name", False))
        self.app_list.heading("Path", text=t['path'], command=lambda: self.sort_column("Path", False))
        self.app_list.heading("Status", text=t['status'], anchor="w", command=lambda: self.sort_column("Status", False))
        self.app_list.column("Status", anchor="w")

    def change_language(self, event: tk.Event) -> None:
        selected = self.language_var.get()
        if selected == "Italiano":
            self.current_language = "it"
        elif selected == "Español":
            self.current_language = "es"
        elif selected == "Français":
            self.current_language = "fr"
        elif selected == "Deutsch":
            self.current_language = "de"
        elif selected == "Português":
            self.current_language = "pt"
        elif selected == "Русский":
            self.current_language = "ru"
        elif selected == "中文":
            self.current_language = "zh"
        elif selected == "日本語":
            self.current_language = "ja"
        elif selected == "한국어":
            self.current_language = "ko"
        else:
            self.current_language = "en"
        self.update_ui_texts()
        self.refresh_apps()

    def toggle_theme(self) -> None:
        self.current_theme = "flatly" if self.current_theme == "darkly" else "darkly"
        self.style.theme_use(self.current_theme)
        self.update_ui_texts()

    def open_github(self) -> None:
        webbrowser.open("https://github.com/Lotverp/Python-Net-Blocker")

    def open_donate(self) -> None:
        webbrowser.open("https://www.paypal.me/GabrielPolverini")

    def on_search(self, event: Optional[tk.Event] = None) -> None:
        filter_text = self.search_var.get().lower()
        self.refresh_apps(filter_text)

    def clear_search(self) -> None:
        self.search_var.set("")
        self.refresh_apps()

    def refresh_apps(self, filter_text: Optional[str] = None) -> None:
        self.app_list.delete(*self.app_list.get_children())
        threading.Thread(target=self._refresh_apps, args=(filter_text,), daemon=True).start()

    def _refresh_apps(self, filter_text: Optional[str] = None) -> None:
        t = translations[self.current_language]
        apps: dict[str, dict[str, Any]] = {}
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] and "Windows" not in proc.info['exe']:
                    name = proc.info['name'].lower()
                    path = proc.info['exe'].lower()
                    if filter_text and filter_text not in name and filter_text not in path:
                        continue
                    status = t['bloccato'] if self.check_firewall_rule(proc.info['exe']) else t['consentito']
                    if path not in apps:
                        apps[path] = {"name": proc.info['name'], "status": status, "count": 1}
                    else:
                        apps[path]["count"] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        for path, details in apps.items():
            name = details["name"]
            status = details["status"]
            count = details["count"]
            display_name = f"{name} ({count} instances)" if count > 1 else name
            self.app_list.insert("", "end", values=(display_name, path, status))

        if self.current_sort_column:
            self.sort_column(self.current_sort_column, self.sort_ascending)

    def check_firewall_rule(self, exe_path: str) -> bool:
        rule_name = f"Block_{Path(exe_path).name}"
        result = subprocess.run(
            f'netsh advfirewall firewall show rule name={rule_name}',
            shell=True,
            capture_output=True,
            text=True
        )
        return rule_name in result.stdout

    def block_app(self) -> None:
        t = translations[self.current_language]
        selected = self.app_list.selection()
        if not selected:
            messagebox.showwarning(t['warning_title'], t['warning_select_app'])
            return

        exe_path = self.app_list.item(selected[0])['values'][1]
        rule_name = f"Block_{Path(exe_path).name}"
        try:
            subprocess.run(
                f'netsh advfirewall firewall add rule name="{rule_name}" dir=out program="{exe_path}" action=block',
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            messagebox.showinfo(t['success_title'], t['success_block'].format(Path(exe_path).name))
            self.refresh_apps()
        except subprocess.CalledProcessError:
            messagebox.showerror(t['error_title'], t['error_block'])

    def unblock_app(self) -> None:
        t = translations[self.current_language]
        selected = self.app_list.selection()
        if not selected:
            messagebox.showwarning(t['warning_title'], t['warning_select_app'])
            return

        exe_path = self.app_list.item(selected[0])['values'][1]
        rule_name = f"Block_{Path(exe_path).name}"
        try:
            subprocess.run(
                f'netsh advfirewall firewall delete rule name={rule_name}',
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            messagebox.showinfo(t['success_title'], t['success_unblock'].format(Path(exe_path).name))
            self.refresh_apps()
        except subprocess.CalledProcessError:
            messagebox.showerror(t['error_title'], t['error_unblock'])

    def unblock_all_apps(self) -> None:
        t = translations[self.current_language]
        # Itera su tutti gli elementi della Treeview e prova a rimuovere la regola per ciascuno
        errors = []
        for item in self.app_list.get_children():
            exe_path = self.app_list.item(item)['values'][1]
            rule_name = f"Block_{Path(exe_path).name}"
            try:
                subprocess.run(
                    f'netsh advfirewall firewall delete rule name="{rule_name}"',
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError:
                # Se la regola non esiste, ignoriamo l'errore
                pass
        if errors:
            messagebox.showerror(t['error_title'], t['error_unblock_all'].format(", ".join(errors)))
        else:
            messagebox.showinfo(t['success_title'], t['success_unblock_all'])
        self.refresh_apps()

    def add_app(self) -> None:
        t = translations[self.current_language]
        exe_path = filedialog.askopenfilename(
            title=t['select_executable'],
            filetypes=((t['file_exe'], "*.exe"), (t['all_files'], "*.*"))
        )
        if exe_path:
            self.app_list.insert("", "end", values=(Path(exe_path).name, exe_path, t['consentito']))

    def sort_column(self, column: str, reverse: bool) -> None:
        self.current_sort_column = column
        self.sort_ascending = not reverse
        t = translations[self.current_language]
        sort_direction = "Ascending" if self.sort_ascending else "Descending"
        self.sort_label.config(text=f"{t['sort']} ({sort_direction})")
        items = [(self.app_list.set(child, column), child) for child in self.app_list.get_children('')]
        items.sort(reverse=not self.sort_ascending)
        for index, (_, child) in enumerate(items):
            self.app_list.move(child, '', index)
        self.app_list.heading(column, command=lambda: self.sort_column(column, not reverse))

def main() -> None:
    root = tk.Tk()
    app = NetBlockerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
