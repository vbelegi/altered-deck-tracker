import time
import customtkinter
from utils import (deckSaveInDatabase, getDeckNames, getDeckCodeByName, deckListFormater, getCardNameById
, drawChance,checkHero)
import get_card_images
import get_cards_data
import crop_card_images

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("./custom_theme.json")

# Initialize main window
root = customtkinter.CTk()
root.geometry("300x300")
root.resizable(width=False, height=False)
root.title("Alien Ältered Deck Tracker")
default_font = customtkinter.CTkFont(family="arial", size=12)
title_font = customtkinter.CTkFont(family="arial", size=24)


# Class for the "Load Deck" window
class DeckAddWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x600")
        self.resizable(width=False, height=False)
        self.title("Load Deck")
        master.iconify()  # Minimize the main window

        # Close action
        def close_window():
            self.destroy()
            master.deiconify()

        # Save deck action
        def save_deck():
            deck = textdeck.get("0.0", "end-1c")
            name = name_entry.get()
            deckSaveInDatabase(name, deck)
            close_window()

        # Widgets
        frame = customtkinter.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=20, padx=30, fill="both", expand=True)

        label = customtkinter.CTkLabel(frame, text="Deck Load", font=title_font)
        label.pack(pady=12, padx=0, fill="x")

        name_entry = customtkinter.CTkEntry(frame, placeholder_text="Deck Name")
        name_entry.pack(pady=12, padx=0, fill="x")

        textdeck = customtkinter.CTkTextbox(frame, width=200, height=300, scrollbar_button_color="#bcbcbc",
                                            scrollbar_button_hover_color="#5b5b5b", activate_scrollbars=True)
        textdeck.pack(pady=12, padx=0, fill="x")
        textdeck.insert("0.0", "Place deck info")

        save_button = customtkinter.CTkButton(frame, text="Save Deck", command=save_deck, font=default_font)
        save_button.pack(pady=12, padx=0, fill="x")

        close_button = customtkinter.CTkButton(frame, text="Close", command=close_window, font=default_font)
        close_button.pack(pady=12, padx=0, fill="x")


# Class for the "Deck List" window
class DeckOpenWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x700")
        self.maxsize(width=400, height=1800)
        self.resizable(width=False, height=True)
        self.minsize(width=400, height=700)
        self.title("Deck List")
        master.iconify()  # Minimize the main window

        # Close action
        def close_window():
            self.destroy()
            master.deiconify()

        # Function to handle changes in CTkOptionMenu
        def on_quantity_change(changed_row, total_cards, quantity_menus, draw_chance_labels):
            # Recalculate draw chance for all rows
            for row_index, (quantity_menu, draw_chance_label) in enumerate(zip(quantity_menus, draw_chance_labels)):
                if row_index == changed_row:
                    # Special case: subtract 1 from total cards and max_value for the changed row
                    current_value = int(quantity_menu.get())
                    new_values = [str(i) for i in range(0, current_value + 1)]
                    quantity_menu.configure(values=new_values)

                    # Update the draw chance for the changed row
                    updated_chance = drawChance(total_cards - 1, current_value - 1)
                    draw_chance_label.configure(text=updated_chance)
                else:
                    # Recalculate draw chance for other rows
                    max_value = int(quantity_menu.get())
                    updated_chance = drawChance(total_cards - 1, max_value)
                    draw_chance_label.configure(text=updated_chance)

        # Update deck list
        def update_deck_list(selected_deck):
            # Clear previous content
            for widget in deck_scrollable_frame.winfo_children():
                widget.destroy()

            # Prepare deck data
            deck_list = deckListFormater(getDeckCodeByName(selected_deck))
            total_cards_deck = sum(deck_list.values())

            # Create storage for widgets
            quantity_menus = []
            draw_chance_labels = []

            # Create widgets dynamically for each card
            for row_counter, (card_id, max_value) in enumerate(deck_list.items()):
                card_name = getCardNameById(card_id)

                # Create quantity option menu
                quantity_values = [str(i) for i in range(0, max_value)]

                if checkHero(card_name):
                    hero_label.configure(text=f"Hero: {card_name}")
                    hero_label.pack(pady=10, padx=30, fill="x")
                else:
                    quantity_menu = customtkinter.CTkOptionMenu(
                        deck_scrollable_frame,
                        values=quantity_values,
                        width=5
                    )
                    quantity_menu.set(str(max_value))
                    quantity_menu.grid(row=row_counter, column=0, padx=5, pady=5)
                    quantity_menus.append(quantity_menu)

                    # Create card name label
                    card_name_label = customtkinter.CTkLabel(deck_scrollable_frame, text=card_name, anchor="w")
                    card_name_label.grid(row=row_counter, column=1, padx=5, pady=5)

                    # Create draw chance label
                    draw_chance_label = customtkinter.CTkLabel(
                        deck_scrollable_frame,
                        text=drawChance(total_cards_deck, max_value),
                        anchor="w"
                    )
                    draw_chance_label.grid(row=row_counter, column=2, padx=5, pady=5)
                    draw_chance_labels.append(draw_chance_label)

                    # Bind the on_quantity_change function to the option menu
                    quantity_menu.configure(
                        command=lambda value, idx=row_counter:
                        on_quantity_change(idx, total_cards_deck, quantity_menus, draw_chance_labels)
                    )

        # Widgets
        deck_select_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        deck_select_frame.pack(pady=20, padx=30, fill="x")

        deck_select = customtkinter.CTkOptionMenu(deck_select_frame, values=getDeckNames(), command=update_deck_list)
        deck_select.pack(pady=5, padx=0,fill="x")

        close_button = customtkinter.CTkButton(deck_select_frame, text="Close", command=close_window, font=default_font)
        close_button.pack(pady=5, padx=0, fill="x")

        hero_label = customtkinter.CTkLabel(deck_select_frame,text="",font=default_font)

        deck_canva = customtkinter.CTkCanvas(self, bg="gray", highlightcolor="gray", highlightthickness=0)
        deck_canva.pack(pady=0, padx=30, fill="both", expand=True)

        deck_scroll = customtkinter.CTkScrollbar(deck_canva, orientation="vertical", command=deck_canva.yview)
        deck_scroll.pack(side="right", fill="y")
        deck_canva.configure(yscrollcommand=deck_scroll.set)

        deck_scrollable_frame = customtkinter.CTkFrame(deck_canva, fg_color="transparent")
        deck_canva.create_window((0, 0), window=deck_scrollable_frame, anchor="nw")

        # Ensure scrollable region updates dynamically
        def update_scroll_region(event=None):
            deck_canva.configure(scrollregion=deck_canva.bbox("all"))

        deck_scrollable_frame.bind("<Configure>", update_scroll_region)

class CreditsWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x300")
        self.resizable(width=False, height=False)
        self.title("Credits")
        master.iconify()

        # Close action
        def close_window():
            self.destroy()
            master.deiconify()

        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=30, fill="both", expand=True)

        me_label = customtkinter.CTkLabel(frame, font=default_font, text="Author: Vinicius Belegi - MrAlienBR")
        me_label.pack(pady=5, padx=0, fill="x")

        nothig_label = customtkinter.CTkLabel(frame, font=default_font,
                                              text="------------------------------------------------------------------")
        nothig_label.pack(pady=5, padx=0, fill="x")


        testers_label = customtkinter.CTkLabel(frame, font=default_font, text="Official Testers 1: Pedroguinha")
        testers_label.pack(pady=5, padx=0, fill="x")

        testers_label = customtkinter.CTkLabel(frame, font=default_font, text="Official Testers 2: Igorzinzin")
        testers_label.pack(pady=5, padx=0, fill="x")

        nothig_label = customtkinter.CTkLabel(frame, font=default_font,
                                              text="------------------------------------------------------------------")
        nothig_label.pack(pady=5, padx=0, fill="x")

        thanks_label = customtkinter.CTkLabel(frame, font=default_font
                                              , text="Thanks for all support by\nAltered Programming Community")
        thanks_label.pack(pady=5, padx=0, fill="x")

        close_button = customtkinter.CTkButton(frame, text="Close", command=close_window, font=default_font, anchor="s")
        close_button.pack(pady=5, padx=0, fill="x", anchor="s")

class DownloadsWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("300x120")
        self.resizable(width=False, height=False)
        self.title("Download Files")
        master.iconify()

        def close_window():
            self.destroy()
            master.deiconify()

        def startdownload():
            w_download = customtkinter.CTkToplevel(self)
            #self.iconify()
            w_download.geometry("300x120")
            w_download.resizable(width=False, height=False)
            w_download.title("Downloading Files...")
            frame = customtkinter.CTkFrame(master=w_download)
            frame.pack(pady=20, padx=30, fill="both", expand=True)
            label = customtkinter.CTkLabel(master=frame, text="This window will close \nautomatically at download end")
            label.pack(pady=5, padx=0, fill="x")
            progressbar = customtkinter.CTkProgressBar(frame)
            progressbar.set(0)
            progressbar.pack(pady=5, padx=5, fill="x")
            progress_desc = customtkinter.CTkLabel(master=frame, text="Starting Downloads...")
            progress_desc.pack(pady=5, padx=0, fill="x")
            #time.sleep(10)
            progressbar.set(0.1)
            progress_desc.configure(text="Downloading Cards Data...")
            #get_cards_data.main()
            progressbar.set(0.33)
            #time.sleep(10)
            progressbar.set(0.4)
            progress_desc.configure(text="Downloading Cards Images...")
            #get_card_images.main()
            progressbar.set(0.66)
            #time.sleep(10)
            progressbar.set(0.7)
            progress_desc.configure(text="Generate Cards Portrait...")
            #crop_card_images.main()
            progressbar.set(0.99)
            time.sleep(10)
            progressbar.set(1)
            time.sleep(10)
            #self.deiconify

        frame = customtkinter.CTkFrame(master=self)
        frame.pack(pady=20, padx=30, fill="both", expand=True)

        #btn_start_download = customtkinter.CTkButton(master=frame, text="Start Download",
        #                                       command=startdownload, font=default_font)
        btn_start_download = customtkinter.CTkButton(master=frame, text="(WIP) Start Download"
                                                     , font=default_font)
        btn_start_download.pack(pady=5, padx=0, fill="x")

        close_button = customtkinter.CTkButton(frame, text="Close", command=close_window, font=default_font, anchor="s")
        close_button.pack(pady=5, padx=0, fill="x", anchor="s")

# Main Window
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=30, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Alien Tracker", font=title_font)
label.pack(pady=12, padx=0, fill="x")

btn_add_deck = customtkinter.CTkButton(master=frame, text="Load Deck",
                                       command=lambda: DeckAddWindow(root), font=default_font)
btn_add_deck.pack(pady=12, padx=10, fill="x")

btn_open_deck = customtkinter.CTkButton(master=frame, text="Open Deck",
                                        command=lambda: DeckOpenWindow(root), font=default_font)
btn_open_deck.pack(pady=12, padx=10, fill="x")

btn_download_files = customtkinter.CTkButton(master=frame, text="Download Files",
                                        command=lambda: DownloadsWindow(root), font=default_font)
btn_download_files.pack(pady=12, padx=10, fill="x")

btn_credits = customtkinter.CTkButton(master=frame, text="Credits",
                                        command=lambda: CreditsWindow(root), font=default_font)
btn_credits.pack(pady=12, padx=10, fill="x")

root.mainloop()
