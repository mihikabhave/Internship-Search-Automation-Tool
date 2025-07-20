import tkinter as tk
from tkinter import ttk,messagebox,simpledialog
from tkinter import filedialog as fd

from search import build_query, run_new, save_database, download,create_table

class App(tk.Tk):
    def __init__(self):
        create_table()
        super().__init__()
        self.title("Internship Finder")
        self.is_shuffled = tk.BooleanVar()
        self.display_query = tk.Text(self, height=5, wrap="word")
        self.status_label = ttk.Label(self, text="")
        self.page_count = tk.IntVar(value=5)
        self.api_key = None
        self.se_id = None
        self.selected_file = None
        self.ask_credentials()



        ttk.Button(self, text="Select Excel File", command=self.select_file).pack(pady=10)

        ttk.Checkbutton(self, text="Query Shuffle", variable=self.is_shuffled).pack(pady=5)
        ttk.Button(self, text="Display Query", command=self.generate_query).pack()
        self.display_query.pack(padx=10, pady=10, fill="x")

        ttk.Label(self, text="Search between 1 to 10 pages").pack()
        ttk.Spinbox(self, from_=1, to=10, textvariable=self.page_count).pack(pady=5)

        ttk.Button(self, text="Run a search", command=self.run_new_search).pack(pady=5)
        self.status_label.pack()
        
        ttk.Button(self, text="View Saved URLs", command=self.view_urls).pack(pady=10)
        ttk.Button(self, text="Export results as CSV file",command=self.download_data).pack(pady=10)
        

 
    def select_file(self):
     filetypes = (
        ('Excel files', '*.xlsx *.xls'),
    )
     filename = fd.askopenfilename(
        title='Open desired Excel file',
        initialdir='/',
        filetypes=filetypes
    )
     if filename:
        self.selected_file = filename
        messagebox.showinfo(
            title='Selected File',
            message=f"Selected: {filename}"
        )

    def ask_credentials(self):
        self.api_key = simpledialog.askstring("API Key", "Enter your Google API Key:", parent=self)
        if not self.api_key:
            messagebox.showerror("Error","API Key required.")
            self.destroy()  
            return
        
        self.se_id = simpledialog.askstring("Search Engine ID", "Enter Custom Search Engine ID:", parent=self)
        if not self.se_id:
            messagebox.showerror("Error", "Search Engine ID required.")
            self.destroy()
            return
        
    def generate_query(self):
        if not self.selected_file:
         messagebox.showerror("Error", "Please select an Excel file.")
         return
        try:
            query = build_query(file=self.selected_file,shuffle=self.is_shuffled.get())
            self.display_query.delete("1.0", tk.END)
            self.display_query.insert(tk.END, query)
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def run_new_search(self):
     query = self.display_query.get("1.0", tk.END).strip()
     if not query:
        messagebox.showerror("Error","Empty query.")
        return
     try:
        saved_data = save_database()
        saved_urls = set(saved_data['url']) if not saved_data.empty else set()
        results = run_new(query, self.api_key, self.se_id, pages=self.page_count.get())
        new_urls = [url for url in results if url not in saved_urls]
        self.status_label.config(
            text=f"Saved {len(new_urls)} new results." if new_urls else f"{len(saved_data)} results. No new results"
        )
     except Exception as e:
        messagebox.showerror("Error",str(e))

    def view_urls(self):
        df = save_database()
        top = tk.Toplevel(self)
        top.title("Saved URLs")
        text = tk.Text(top,wrap="word")
        text.pack(padx=10, pady=10, fill="both", expand=True)
        for url in df['url']:
            text.insert(tk.END, url + '\n')
    
    def download_data(self):
     file_path = "results.csv"  
     try:
        download()
        messagebox.showinfo("Success", f"Saved results to:\n{file_path} in Project Folder")
     except Exception as e:
        messagebox.showerror("Error", f"Failed to save CSV:\n{str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()