import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from PIL import Image, ImageTk

###############################################
# Custom dialog for entering a drink name with
# Minecraft color-code insertion buttons.
###############################################
class NameDialog:
    def __init__(self, parent, GoodOrBad):
        self.top = tk.Toplevel(parent)
        self.top.title("Enter Drink Name")
        self.top.grab_set()
        self.result = None

        tk.Label(self.top, text="Enter the bad variant drink name:" if GoodOrBad=="bad" else "Enter the bad variant drink name:").pack(pady=5) if GoodOrBad != "regular" else tk.Label(self.top, text="Enter the regular variant drink name").pack(pady=5)
        self.entry = tk.Entry(self.top, width=40)
        self.entry.pack(pady=5)

        # Frame to hold color code buttons.
        btn_frame = tk.Frame(self.top)
        btn_frame.pack(pady=5)

        # List of Minecraft color codes (code, description)
        self.color_codes = [
            ("&0", "#000000"),
            ("&1", "#0000AA"),
            ("&2", "#00AA00"),
            ("&3", "#00AAAA"),
            ("&4", "#AA0000"),
            ("&5", "#AA00AA"),
            ("&6", "#FFAA00"),
            ("&7", "#AAAAAA"),
            ("&8", "#555555"),
            ("&9", "#5555FF"),
            ("&a", "#55FF55"),
            ("&b", "#55FFFF"),
            ("&c", "#FF5555"),
            ("&d", "#FF55FF"),
            ("&e", "#FFFF55"),
            ("&f", "#FFFFFF"),
            ("&g", "#DDD605"),
            ("&h", "#E3D4D1"),
            ("&i", "#CECACA"),
            ("&j", "#443A3B"),
            ("&m", "#971607"),
            ("&n", "#B4684D"),
            ("&p", "#DEB12D"),
            ("&q", "#47A036"),
            ("&s", "#2CBAA8"),
            ("&t", "#21497B"),
            ("&u", "#9A5CC6")
        ]

        for code, color in self.color_codes:
            btn = tk.Button(btn_frame, text=code, fg=color, command=lambda c=code: self.insert_color_code(c))
            btn.pack(side="left", padx=2)

        btn = tk.Button(btn_frame, text="Custom", command=lambda: self.custom_color_code())
        btn.pack(side="left", padx=2)

        # OK and Cancel buttons.
        ok_btn = tk.Button(self.top, text="OK", command=self.on_ok)
        ok_btn.pack(pady=5)
        cancel_btn = tk.Button(self.top, text="Cancel", command=self.top.destroy)
        cancel_btn.pack(pady=5)

    def insert_color_code(self, code):
        # Insert the Minecraft color code at the current cursor position.
        self.entry.insert(tk.INSERT, code)

    def custom_color_code(self):
        grr, c = colorchooser.askcolor()
        self.insert_color_code("&" + c)

    def on_ok(self):
        self.result = self.entry.get()
        self.top.destroy()

###############################################################
# Treeview-based item selector for ingredients.
###############################################################
class ItemSelector(ttk.Frame):
    def __init__(self, parent, items, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.items = items
        self.select_callback = select_callback
        self.image_cache = {}

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(fill="x", padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Name",), show="tree")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.populate_tree(self.items)

    def populate_tree(self, items):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in items:
            name = item.get("name", "Unknown")
            item_id = item.get("id", "")
            #image = self.load_image_for_item(name)
            self.tree.insert("", "end", iid=item_id, text=name) #image=image)

    # def load_image_for_item(self, name):
    #     if name in self.image_cache:
    #         return self.image_cache[name]
    #     image_path = os.path.join("item_images", f"{name}.png")
    #     if os.path.exists(image_path):
    #         try:
    #             pil_img = Image.open(image_path)
    #             pil_img = pil_img.resize((32, 32), Image.ANTIALIAS)
    #             photo = ImageTk.PhotoImage(pil_img)
    #             self.image_cache[name] = photo
    #             return photo
    #         except Exception as e:
    #             print(f"Error loading image for {name}: {e}")
    #     return None

    def update_filter(self, *args):
        term = self.search_var.get().lower()
        filtered = [item for item in self.items if term in item.get("name", "").lower()]
        self.populate_tree(filtered)

    def on_item_double_click(self, event):
        selected_id = self.tree.focus()
        if not selected_id:
            return
        selected_item = next((item for item in self.items if item.get("id") == selected_id), None)
        if selected_item:
            self.select_callback(selected_item)

class PotionEffectSelector(ttk.Frame):
    def __init__(self, parent, select_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.select_callback = select_callback

        self.effects = [
            "ABSORPTION",
            "BAD_OMEN",
            "BLINDNESS",
            "CONDUIT_POWER",
            "DARKNESS",
            "DOLPHINS_GRACE",
            "FIRE_RESISTANCE",
            "GLOWING",
            "HASTE",
            "HEALTH_BOOST",
            "HERO_OF_THE_VILLAGE",
            "HUNGER",
            "INFESTED",
            "INSTANT_DAMAGE",
            "INSTANT_HEALTH",
            "INVISIBILITY",
            "JUMP_BOOST",
            "LEVITATION",
            "LUCK",
            "MINING_FATIGUE",
            "NAUSEA",
            "NIGHT_VISION",
            "OOZING",
            "POISON",
            "RAID_OMEN",
            "REGENERATION",
            "RESISTANCE",
            "SATURATION",
            "SLOW_FALLING",
            "SLOWNESS",
            "SPEED",
            "STRENGTH",
            "TRIAL_OMEN",
            "UNLUCK",
            "WATER_BREATHING",
            "WEAKNESS",
            "WEAVING",
            "WIND_CHARGED",
            "WITHER"
        ]

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_filter)
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(fill="x", padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Effect",), show="tree")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.populate_tree(self.effects)

    def load_image_for_item(self, effect):
        image_path = os.path.join(os.path.dirname(__file__), "effects", f"{effect.lower()}.png")
        if os.path.exists(image_path):
            try:
                pil_img = Image.open(image_path)
                photo = ImageTk.PhotoImage(pil_img)
                return photo
            except Exception as e:
                print(f"Error loading image for {effect}: {e}")

    def populate_tree(self, effects):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for effect in effects:
            image = self.load_image_for_item(effect)
            if image:
                self.tree.insert("", "end", iid=effect, text=effect, image=image)
            else:
                self.tree.insert("", "end", iid=effect, text=effect)

    def update_filter(self, *args):
        term = self.search_var.get().lower()
        filtered = [e for e in self.effects if term in e.lower()]
        self.populate_tree(filtered)

    def on_item_double_click(self, event):
        selected_id = self.tree.focus()
        if not selected_id:
            return
        effect = selected_id
        level = simpledialog.askstring("Effect Level", f"Enter the {effect} level (default 1) (eg 2 or 1-3 (1 for the worst version, 3 for the best):", initialvalue=1)
        if level is None:
            return
        duration = simpledialog.askstring("Effect Duration", f"Enter {effect}'s duration (in seconds) (eg 10 or 10-50 (10 for the worst version, 50 for the best)):", initialvalue=30)
        if duration is None:
            return
        self.select_callback(effect, level, duration)

###############################################################
# Main application class.
###############################################################
class BreweryRecipeGenerator():
    def __init__(self, master):
        self.master = master
        master.title("Brewery Recipe Generator")
        master.geometry("600x600")
        self.master.attributes("-topmost", True)

        header_path = os.path.join(os.path.dirname(__file__), '2FA', "ses.jpg")
        if os.path.exists(header_path):
            header_img = Image.open(header_path)
            header_photo = ImageTk.PhotoImage(header_img)
            header_label = tk.Label(master, image=header_photo)
            header_label.image = header_photo  # Keep a reference!
            header_label.pack(pady=5)

        new_drink_btn = tk.Button(master, text="New Drink Recipe", command=self.new_drink_recipe)
        new_drink_btn.pack(pady=10)

        new_cauldron_btn = tk.Button(master, text="New Cauldron Recipe", command=self.new_cauldron_recipe)
        new_cauldron_btn.pack(pady=10)

        self.ingredients = []

    def load_items_from_json(self, file_path, prefix):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                for idx, item in enumerate(data):
                    if "id" in item:
                        item["id"] = f"{prefix}_{item['id']}"
                    else:
                        item["id"] = f"{prefix}_{idx}"
                return data
        except Exception as e:
            messagebox.showerror("Error", f"Error loading {file_path}: {e}")
            return []

    def load_all_items(self):
        items = []
        items += self.load_items_from_json("items.json", "r1")
        items += self.load_items_from_json("blocks.json", "r2")
        return items

    def new_drink_recipe(self):
        # Use the custom NameDialog to get the drink name with color codes.
        name_dialog = NameDialog(self.master, "bad")
        self.master.wait_window(name_dialog.top)
        badname = name_dialog.result
        name_dialog = NameDialog(self.master, "regular")
        self.master.wait_window(name_dialog.top)
        name = name_dialog.result
        name_dialog = NameDialog(self.master, "good")
        self.master.wait_window(name_dialog.top)
        goodname = name_dialog.result
        if not name:
            messagebox.showerror("Nah", "I'd win.")
            return

        self.ingredients = []
        self.potion_effects = []
        self.lore_text_widgets = []
        self.command_text_widgets = []
        self.playercommand_text_widgets = []
        all_items = self.load_all_items()

        # Create a window for ingredient selection.
        selection_window = tk.Toplevel(self.master)
        selection_window.title("Select Ingredients")
        selection_window.geometry("400x600")

        notebook = ttk.Notebook(selection_window)
        notebook.pack(fill="both", expand=True)
        ingredient_frame = ttk.Frame(notebook)
        notebook.add(ingredient_frame, text="Ingredients")

        def on_item_selected(item):
            item_name = item.get("name", "Unknown")
            amount = simpledialog.askinteger("Amount", f"Enter the amount for {item_name}:")
            self.ingredients.append(f"  - {item_name}/{amount}")
            messagebox.showinfo("Ingredient Added", f"{item_name} ({amount}) added.")

        def add_custom_item():
            item = simpledialog.askstring("Item", f"Add a custom item in this format Brewery:ColorfulBrew/2")
            amount = simpledialog.askinteger("Amount", f"Enter the amount for {item}:")
            if item:
                self.ingredients.append(f"  - {item}/{amount}")
                messagebox.showinfo("Ingredient Added", f"{item} ({amount}) added.")

        item_selector = ItemSelector(selection_window, all_items, on_item_selected)
        item_selector.pack(fill="both", expand=True)

        potion_frame = ttk.Frame(notebook)
        notebook.add(potion_frame, text="Potion Effects")
        def on_potion_effect_selected(effect, level, duration):
            self.potion_effects.append(f"  - {effect}/{level}/{duration}")
            messagebox.showinfo("Potion Effect Added", f"{effect} (Level {level}, {duration}s) added.")
        potion_selector = PotionEffectSelector(potion_frame, on_potion_effect_selected)
        potion_selector.pack(fill="both", expand=True)

        # --------------------------
        # Lore Tab
        # --------------------------
        lore_frame = ttk.Frame(notebook)
        notebook.add(lore_frame, text="Lore")

        # Create a container frame to hold the text areas.
        lore_container = ttk.Frame(lore_frame)
        lore_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Function to add a new lore text area.
        text_widget = tk.Text(lore_container, height=4, width=40)
        text_widget.pack(pady=5)
        self.lore_text_widgets.append(text_widget)


        # Button to show lore instructions.
        def show_lore_instructions():
            instructions = (
                "Lore can follow this format:\n"
                "This text will always be present"
                "+ This text will be present if brew has bad quality"
                "++ This text will be present if brew has normal quality"
                "+++ This text will be present if brew has good quality"
            )
            messagebox.showinfo("Lore Formatting", instructions)

        lore_instructions_button = tk.Button(lore_frame, text="Lore Instructions", command=show_lore_instructions)
        lore_instructions_button.pack(pady=5)

        # --------------------------
        # Servercommand Tab
        # --------------------------
        command_frame = ttk.Frame(notebook)
        notebook.add(command_frame, text="ServerCommand")

        # Create a container frame to hold the text areas.
        command_container = ttk.Frame(command_frame)
        command_container.pack(fill="both", expand=True, padx=5, pady=5)

        command_widget = tk.Text(command_container, height=4, width=40)
        command_widget.pack(pady=5)
        self.command_text_widgets.append(command_widget)

        # Button to show lore instructions.
        def show_command_instructions():
            instructions = (
                "ServerCommands can follow this format:\n"
                "say This will execute no matter what!"
                "say This message will be delayed by 5 seconds! \5s"
                "+ kill %player% # This will execute if brew quality is bad"
                "++ heal %player% # This will execute if brew quality is normal"
                "+++ op %player% # This will execute if brew quality is good"
            )
            messagebox.showinfo("Lore Formatting", instructions)

        server_instructions_button = tk.Button(command_frame, text="Lore Instructions", command=show_command_instructions)
        server_instructions_button.pack(pady=5)

        # --------------------------
        # Playercommand Tab
        # --------------------------
        playercommand_frame = ttk.Frame(notebook)
        notebook.add(playercommand_frame, text="PlayerCommand")

        # Create a container frame to hold the text areas.
        playercommand_container = ttk.Frame(playercommand_frame)
        playercommand_container.pack(fill="both", expand=True, padx=5, pady=5)

        playercommand_widget = tk.Text(playercommand_container, height=4, width=40)
        playercommand_widget.pack(pady=5)
        self.playercommand_text_widgets.append(playercommand_widget)

        # Button to show lore instructions.
        def show_playercommand_instructions():
            instructions = (
                "PlayerCommands can follow this format:\n"
                "say This will execute no matter what!"
                "say This message will be delayed by 5 seconds! \5s"
                "+ msg Mom I'm sorry Ma"
                "++ home"
                "+++ kiss @e[type=Villager]"
            )
            messagebox.showinfo("Lore Formatting", instructions)

        player_instructions_button = tk.Button(playercommand_frame, text="Lore Instructions", command=show_playercommand_instructions)
        player_instructions_button.pack(pady=5)

        def finalize_recipe():
            recipe = f"  name: '{badname}/{name}/{goodname}'\n  ingredients:\n" + '\n'.join(self.ingredients)
            cooking_time = simpledialog.askinteger("Cooking Time", "Enter cooking time (in minutes):")
            if cooking_time:
                recipe += f"  cookingtime: {cooking_time}\n"
            distill_runs = simpledialog.askstring("Distill Runs", "Enter number of distillation runs:")
            if distill_runs:
                recipe += f"  distillruns: {distill_runs}\n"
            distill_time = simpledialog.askstring("Distill Time", "Enter distillation time (in minutes):") if distill_runs else ""
            if distill_time:
                recipe += f"  distilltime: {distill_time}\n"
            rgb, color = colorchooser.askcolor()
            if color:
                recipe += f"  color: '{color.removeprefix('#')}'\n"
            difficulty = simpledialog.askinteger("Difficulty", "Enter difficulty (1-10):")
            if difficulty:
                recipe += f"  difficulty: {difficulty}\n"
            alcohol = simpledialog.askinteger("Alcohol Content", "Enter alcohol percentage (0-100) (negative values will lessen the intoxication):")
            if alcohol and alcohol != 0:
                recipe += f"  alcohol: {alcohol}\n"
            wood = simpledialog.askstring("Wood Type", "Enter barrel's wood type (keep empty if ageable everywhere):")
            if wood:
                recipe += f"  wood: {wood}\n"
            age = simpledialog.askstring("Aging Time", "Enter aging time (in years):") if wood else ""
            if age:
                recipe += f"  age: {age}\n"
            if self.lore_text_widgets:
                entries = []
                for widget in self.lore_text_widgets:
                    lore = widget.get("1.0", "end").strip()
                    if lore:
                        lore = lore.split('\n')
                        for part in lore:
                            entries.append(f"  - {part}")
                recipe += f"  lore:\n" + '\n'.join(entries) + '\n'
            if self.command_text_widgets:
                entries = []
                for widget in self.command_text_widgets:
                    command = widget.get("1.0", "end").strip()
                    if command:
                        command = command.split('\n')
                        for grr in command:
                            entries.append(f"  - {grr}")
                recipe += f"  servercommands:\n" + '\n'.join(entries) + '\n'
            if self.playercommand_text_widgets:
                entries = []
                for widget in self.command_text_widgets:
                    command = widget.get("1.0", "end").strip()
                    if command:
                        command = command.split('\n')
                        for grr in command:
                            entries.append(f"  - {grr}")
                recipe += f"  playercommands:\n" + '\n'.join(entries) + '\n'
            drinkmessage = simpledialog.askstring("Drink Message", "Shows a message after drinking the brew")
            if drinkmessage:
                recipe += f"  drinkmessage: {drinkmessage}\n"
            drinktitle = simpledialog.askstring("Drink Title", "Shows a title after drinking the brew")
            if drinkmessage:
                recipe += f"  drinktitle: {drinktitle}\n"
            effects = simpledialog.askstring("Custom Effects", "Enter custom effects/their level/their duration (in this format(with /)) (if multiple effects, comma-separated with no spaces) (leave empty if none):")
            glint = messagebox.askyesno("Glint", "Do you want the brew to glow ? (enchantement effect)")
            if glint:
                recipe += "  glint: true\n"
            if effects:
                effects = effects.split(",")
                for effect in effects:
                    self.potion_effects.append(f"  - {effect}")
            if self.potion_effects:
                recipe += f"  effects:\n" + '\n'.join(self.potion_effects)

            # Display the final recipe in a new window.
            recipe_window = tk.Toplevel(self.master)
            recipe_window.title("New Drink Recipe")
            recipe_window.geometry("400x500")
            text_widget = tk.Text(recipe_window, wrap="word", height=20, width=50)
            text_widget.insert("1.0", recipe)
            text_widget.config(state="disabled")
            text_widget.pack(pady=10)

            def copy_to_clipboard():
                self.master.clipboard_clear()
                self.master.clipboard_append(recipe)
                self.master.update()
                messagebox.showinfo("Copied", "Recipe copied to clipboard!")

            copy_button = tk.Button(recipe_window, text="Copy to Clipboard", command=copy_to_clipboard)
            copy_button.pack(pady=5)
            close_button = tk.Button(recipe_window, text="Close", command=recipe_window.destroy)
            close_button.pack(pady=5)
            selection_window.destroy()

        server_customitem_button = tk.Button(selection_window, text="Add Custom items for ingredient", command=add_custom_item)
        server_customitem_button.pack(pady=5)
        finalize_button = tk.Button(selection_window, text="Finalize Recipe", command=finalize_recipe)
        finalize_button.pack(pady=5)

    def new_cauldron_recipe(self):
        messagebox.showinfo("Feature Not Implemented", "New cauldron recipe feature is coming soon!")

###############################################################
# Run the application.
###############################################################
if __name__ == "__main__":
    root = tk.Tk()
    app = BreweryRecipeGenerator(root)
    root.mainloop()