# ai_sidebar.py

import os
import http.client
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, messagebox, END, WORD
from threading import Thread
from dotenv import load_dotenv

# Load RapidAPI credentials
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

if not RAPIDAPI_KEY or not RAPIDAPI_HOST:
    raise ValueError("RapidAPI anahtarı veya host bilgisi .env dosyasında tanımlı değil!")

class AISidebar:
    def __init__(self, master, x, y):
        """
        Initialize the AI Sidebar.
        Args:
            master: The main application window.
            x (int): The x-coordinate where the sidebar should appear.
            y (int): The y-coordinate where the sidebar should appear.
        """
        self.master = master

        # Create a new Toplevel window for the sidebar
        self.sidebar = ttk.Toplevel(master)
        self.sidebar.title("Yapay Zeka")
        self.sidebar.geometry(f"400x600+{x}+{y}")  # Position the window
        self.sidebar.resizable(False, False)
        self.sidebar.protocol("WM_DELETE_WINDOW", self.close_sidebar)

        # NOTE: Removed grab_set() so the main window remains accessible
        # self.sidebar.grab_set()
        #
        # We can keep transient if you want the sidebar to stay on top or
        # visually associated with the main window:
        # self.sidebar.transient(master)

        # Create the UI widgets
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the widgets in the sidebar."""
        # Input Label
        self.input_label = ttk.Label(self.sidebar, text="Soru:")
        self.input_label.pack(pady=(10, 0), padx=10, anchor='w')

        # Input Text Box
        self.input_text = scrolledtext.ScrolledText(
            self.sidebar, height=5, wrap=WORD, undo=True
        )
        self.input_text.pack(padx=10, pady=(0, 10), fill='x')

        # Bind shortcuts for copy/paste/select all
        self.bind_text_shortcuts(self.input_text)

        # Send Button
        self.send_button = ttk.Button(
            self.sidebar,
            text="Gönder",
            command=self.handle_send
        )
        self.send_button.pack(pady=(0, 10))

        # Output Label
        self.output_label = ttk.Label(self.sidebar, text="Cevap:")
        self.output_label.pack(pady=(0, 0), padx=10, anchor='w')

        # Output Text Box
        self.output_text = scrolledtext.ScrolledText(
            self.sidebar,
            height=25,
            wrap=WORD,
            state='disabled',
            undo=True
        )
        self.output_text.pack(padx=10, pady=(0, 10), fill='both', expand=True)

        # Also bind shortcuts on output_text (copy, select all, etc.)
        self.bind_text_shortcuts(self.output_text, readonly=True)

    def bind_text_shortcuts(self, text_widget, readonly=False):
        """
        Bind common keyboard shortcuts (Ctrl + C, V, X, A).
        readonly=True will block cut/paste for the output text.
        """

        # Select All
        def select_all(event):
            text_widget.tag_add("sel", "1.0", "end")
            return "break"

        # Copy
        def copy_text(event):
            if text_widget.tag_ranges("sel"):
                text_widget.event_generate("<<Copy>>")
            return "break"

        if not readonly:
            # Cut
            def cut_text(event):
                if text_widget.tag_ranges("sel"):
                    text_widget.event_generate("<<Cut>>")
                return "break"

            # Paste
            def paste_text(event):
                text_widget.event_generate("<<Paste>>")
                return "break"

            text_widget.bind("<Control-v>", paste_text)
            text_widget.bind("<Control-V>", paste_text)
            text_widget.bind("<Control-x>", cut_text)
            text_widget.bind("<Control-X>", cut_text)

        # Common bindings for both read-only and editable
        text_widget.bind("<Control-c>", copy_text)
        text_widget.bind("<Control-C>", copy_text)
        text_widget.bind("<Control-a>", select_all)
        text_widget.bind("<Control-A>", select_all)

    def handle_send(self):
        """Handle the send button click event."""
        user_input = self.input_text.get("1.0", END).strip()
        if not user_input:
            messagebox.showwarning("Uyarı", "Lütfen bir soru giriniz.")
            return

        # Disable the send button to prevent multiple clicks
        self.send_button.config(state='disabled')

        # Start a thread to get AI response
        thread = Thread(target=self.get_ai_response, args=(user_input,))
        thread.start()

    def get_ai_response(self, prompt):
        """Fetch AI response from /gpt4 on chatgpt-42.p.rapidapi.com."""
        try:
            conn = http.client.HTTPSConnection(RAPIDAPI_HOST)

            # Prepare the payload
            payload = json.dumps({
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "web_access": False
            })

            headers = {
                "x-rapidapi-key": RAPIDAPI_KEY,
                "x-rapidapi-host": RAPIDAPI_HOST,
                "Content-Type": "application/json"
            }

            conn.request("POST", "/gpt4", payload, headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()

            # DEBUG: Print raw response
            print("Response status:", res.status)
            print("Raw data:", data)

            response_json = json.loads(data.decode("utf-8"))
            # Example response is:
            #   {"result": "Selam! Size nasıl yardımcı olabilirim?", "status": true, "server_code": "dg"}

            answer = response_json.get("result", "Cevap alınamadı (no 'result' key).")

            # Update the output text
            self.output_text.config(state='normal')
            self.output_text.insert(END, f"Soru: {prompt}\nCevap: {answer}\n\n")
            self.output_text.config(state='disabled')
            self.output_text.see(END)

        except Exception as e:
            messagebox.showerror("Hata", f"AI cevabı alınırken bir hata oluştu: {str(e)}")
        finally:
            # Clear the input box after we get the answer
            self.input_text.delete("1.0", END)

            # Re-enable the send button
            self.send_button.config(state='normal')

    def close_sidebar(self):
        """Handle the sidebar window closing."""
        self.sidebar.destroy() 