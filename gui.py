import tkinter as tk
from tkinter import *
from tkinter import messagebox

import combiner
import processor
import summary


def init():
    """
    Initializes the GUI for the application.
    """
    root = tk.Tk()
    root.title("Review Scraper")
    root.geometry("720x480")

    header_summary = tk.Label(root, text="Summary")
    header_summary.config(font=("helvetica", 16, "bold"))
    header_summary.place(x=5, y=5)

    text_summary = tk.Text(root, height=25, width=30)
    text_summary.config(state=DISABLED)
    text_summary.place(x=5, y=35)

    label_input = tk.Label(root, text="Enter product model:")
    label_input.config(font=("helvetica", 16, "bold"))
    label_input.place(x=300, y=65)

    label_list = tk.Label(root, text="Search results:")
    label_list.config(font=("helvetica", 16, "bold"))
    label_list.place(x=300, y=140)

    entry = tk.Entry(root, width=30)
    entry.config(font=("arial", 12))
    entry.place(x=300, y=95)

    button_submit = tk.Button(root, text="Search")
    button_submit.config(relief=RAISED, bg="lightblue", )
    button_submit.place(x=580, y=93)

    status = tk.Label(root, text="Waiting...")
    status.place(x=5, y=450)

    urls = []
    listbox = tk.Listbox(root, height=15, width=60)
    listbox.place(x=300, y=170)

    def update_results():
        """
        Gets the product in the input field and sends it
        to the scrappers to get a list of the top 5 resulting search hits.
        """
        value = entry.get()
        status.config(text="Searching...")
        status.update()
        search_hits = combiner.search(value)  # List of dictionaries containing url and model name.
        status.config(text="Waiting...")
        status.update()
        # Clear the Listbox and url list
        listbox.delete(0, tk.END)
        urls.clear()

        # Add the five closest related hits to the Listbox
        for hit in search_hits:
            urls.append(search_hits[hit])
            listbox.insert(tk.END, hit)

    def handle_click(event):
        """
        Gets clicked product model from `listbox`,
        calls `confirm_search` to confirm that the user
        want to search for the selected product model.
        :param event: Unused.
        """
        index = listbox.curselection()[0]
        product = listbox.get(index)
        url = urls[index]

        # Ask if the user wants to search for the selected product model
        confirm_search(product, url)

    def confirm_search(product: str, url: dict):
        """
        Asks the user if they want to proceed to search for selected product model.
        Retrieves a list of reviews from of the product model by passing url and
        the amount of reviews to retrieve.
        """
        confirmed = messagebox.askyesno("Confirmation", "Do you want to search for: " + product)
        if confirmed:
            status.config(text="Gathering reviews (this can take a while)...")
            status.update()
            gathered = combiner.gather(url)

            score = processor.score(gathered["score"])

            sources = gathered["sources"]

            status.config(text="Processing...")
            reviews = summary.summary(processor.process(gathered["ratings"]))

            text_summary.config(state=tk.NORMAL)  # disabled state prevents updates
            text_summary.delete("1.0", END)
            text_summary.insert(END, "SCORE: " + str(round(score, 1)) + "\n\n")
            text_summary.insert(END, "MOST USED DESCRIPTORS:\n" + reviews)
            text_summary.insert(END, "\nSOURCES:\n")
            for s in sources:
                text_summary.insert(END, s + "\n")
            status.config(text="Complete.")
            root.update()
            text_summary.config(state=tk.DISABLED)
        else:
            text_summary.delete("1.0", END)
            text_summary.insert(END, "SEARCH CANCELED")
            text_summary.update()
            status.config(text="Canceled.")
            status.update()

    entry.bind("<Return>", lambda event: root.after(0, update_results()))
    button_submit.bind("<ButtonRelease-1>", lambda event: root.after(0, update_results()))
    listbox.bind("<ButtonRelease-1>", handle_click)
    root.mainloop()


if __name__ == "__main__":
    init()
