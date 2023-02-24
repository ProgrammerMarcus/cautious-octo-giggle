import tkinter as tk
from tkinter import messagebox
import pricespy


def init():
    root = tk.Tk()
    root.title("Review Scrapper")

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    label_input = tk.Label(root, text="Enter product model:")
    label_input.config(font=("helvetica", 12))
    canvas.create_window(400, 270, window=label_input)

    entry = tk.Entry(root)
    entry.config(font=("arial", 12))
    canvas.create_window(400, 300, window=entry, width=200, height=30)

    urls = []

    listbox = tk.Listbox(root)
    canvas.create_window(400, 400, window=listbox, width=250, height=150)

    def update_results():
        """
        Gets the product in the input field and sends it
        to the scrappers to get a list of the top 5 resulting search hits.
        :param event: <Return> key pressed.
        """
        value = entry.get()
        search_hits = pricespy.get_search(value)  # List of dictionaries containing url and model name.

        # Clear the Listbox and url list
        listbox.delete(0, tk.END)
        urls.clear()

        # Add the five closest related hits to the Listbox
        for hit in search_hits:
            urls.append(hit["url"])
            listbox.insert(tk.END, hit["name"])

    entry.bind("<Return>", lambda event: root.after(0, update_results()))

    def handle_click(event):
        """
        Gets clicked product model from `listbox`,
        calls `confirm_search` to confirm that the user
        want to search for the selected product model.
        :param event:
        :return:
        """
        index = listbox.curselection()[0]
        product = listbox.get(index)
        url = urls[index]

        # Ask if the user wants to search for the selected product model
        confirm_search(product, url)

    def confirm_search(product: str, url: str):
        """
        Confirmation box..
        Search for product if...
        """
        confirmed = messagebox.askyesno("Confirmation", "Do you want to search for: " + product)
        if confirmed:
            reviews = pricespy.get_list(url, 10)
            print(reviews)
        else:
            print("Cancelled")

    listbox.bind("<ButtonRelease-1>", handle_click)
    root.mainloop()


if __name__ == "__main__":
    init()
