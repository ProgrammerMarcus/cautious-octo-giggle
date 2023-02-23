import tkinter as tk
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

        # Clear the Listbox
        listbox.delete(0, tk.END)

        # Add the five closest related hits to the Listbox
        for hit in search_hits:
            listbox.insert(tk.END, hit["name"])

    entry.bind("<Return>", lambda event: root.after(0, update_results()))

    def handle_click(event):
        """

        :param event:
        :return:
        """
        # Get the selected item
        index = listbox.curselection()[0]
        product = listbox.get(index)
        print(f"Clicked product: {product}")

    listbox.bind("<ButtonRelease-1>", handle_click)
    root.mainloop()


if __name__ == "__main__":
    init()
