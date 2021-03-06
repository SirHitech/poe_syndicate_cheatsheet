import tkinter
from tkinter import messagebox
import os
from PIL import ImageTk, Image

SAVE_FILE = './save.txt'
SYNDICATE_PATH = './assets/members'
LOCATION_PATH = './assets/locations'
ENCOUNTER_PATH = './assets/encounters'
BACKGROUND_COLOUR = '#222222'
FRAME_COLOUR = '#333333'
FOREGROUND_COLOUR = '#D9D9D9'
ENCOUNTERS_TEXT = [["1/2/3 Weapons with Veiled mods", "1/2/3 Armours with Veiled mods", "Add 1-2 Veiled mods to Rare Item", "Metamorph Scarab"],
                   ['1 Timeworn Unique', 'Harbinger and Horizon Orbs', 'Sextants', 'Sulphite Scarab'],
                   ['1/2/3 Unique Weapons', '1/2/3 Unique Armours', '1/2/3 Unique Jewellery', 'Reliquary Scarab'],
                   ['1 Full Stack of Div. Cards', 'Random Div. Cards', 'Swap your Div. Card for a random one', 'Divination Scarab'],
                   ['8/12/16 Timed Craft', '10/15/20 Timed Craft', '10/15/20 Timed Craft', '10/15/20 Timed Craft'],
                   ['Random Items', 'Magic/Rare/ Unique Strongbox', 'Random Items with Quality', 'Ambush Scarab'],
                   ['24/26/28 Quality to Weapon', '24/26/28 Quality to Armour', '22/24/26 Quality to Flask', '25/30/35 Quality to Map'],
                   ['Breach Splinters', 'Abyss Jewels', 'T1/T2/T3 Upgrade Breachstone', 'Breach Scarab'],
                   ['Quality Currency', 'Currency Shards', 'Perandus Coins and Cadiro', 'Perandus Scarab'],
                   ['1/2/3 Talismans', '1/2/3 Rares with Aspect mods', 'Tier 1/2/3 Corrupt Amulet to Talisman', 'Bestiary Scarab'],
                   ['Random Essences', 'Map Fragments', 'Fossils', 'Elder\nScarab'],
                   ['Silver Coins', 'Random Currency', 'Blessed/ Divine/Exalt on an Item', 'Torment Scarab'],
                   ['Currency - Timed Take One', 'Unique - Timed Take One', 'Veiled Rare - Timed Take One', 'Div. Card - Timed Take One'],
                   ['Normal Maps', 'Rare Maps', 'Unique Maps', 'Cartography Scarab'],
                   ['Items - Timed Take One', 'Glove/Boot/Helms with Lab Enchant', '20/70/200M XP to a Gem', 'Harbinger Scarab'],
                   ['Legion Splinters', 'Legion Chests', 'Incubators', 'Legion Scarab'],
                   ['Gems with Random Quality', 'Socket Currency', '1/1-2/1-3 White Sockets on an Item', 'Shaper Scarab']]
STATUS_COLOURS = [BACKGROUND_COLOUR, '#0a5511', '#54550a', '#590404']


class Cell(tkinter.Label):
    def __init__(self, master, current_colour=0, **kwargs):
        super(Cell, self).__init__(master, foreground=FOREGROUND_COLOUR, **kwargs)
        self.current_colour = current_colour
        self.set_background_colour()
        self.bind('<Button-1>', self.click_event)

    def click_event(self, event):
        self.current_colour = (self.current_colour + 1)%len(STATUS_COLOURS)
        self.set_background_colour()

    def set_background_colour(self):
        self.configure(background=STATUS_COLOURS[self.current_colour])


def list_files(path):
    return next(os.walk(path))[2]


def list_folders(path):
    return next(os.walk(path))[1]


def check_file(path):
    return os.path.isfile(path)


def on_closing(main_window, syndicate_labels, location_labels, encounter_labels):
    if messagebox.askyesno("Save and Quit", "Do you want to save before quiting?"):
        save_data_colours(syndicate_labels, location_labels, encounter_labels)

    main_window.destroy()


def save_data_colours(syndicate_labels, location_labels, encounter_labels):
    save_data = open(SAVE_FILE, 'w')
    for i in syndicate_labels:
        save_data.write(str(i.current_colour) + ' ')

    save_data.write('\n')
    for i in location_labels:
        save_data.write(str(i.current_colour) + ' ')

    save_data.write('\n')
    for i in encounter_labels:
        for j in i:
            save_data.write(str(j.current_colour) + ' ')

        save_data.write('\n')

    save_data.close()


if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.title('Syndicate Cheatsheet Generator')
    main_window.configure(background=BACKGROUND_COLOUR)
    main_frame = tkinter.Frame(main_window, background=BACKGROUND_COLOUR)
    canvas = tkinter.Canvas(main_frame, borderwidth=0, background=BACKGROUND_COLOUR)

    grid_frame = tkinter.Frame(canvas, background=FRAME_COLOUR)
    grid_hsb = tkinter.Scrollbar(main_frame, orient=tkinter.HORIZONTAL, command=canvas.xview)
    grid_vsb = tkinter.Scrollbar(main_frame, orient=tkinter.VERTICAL, command=canvas.yview)
    canvas.configure(xscrollcommand=grid_hsb.set, yscrollcommand=grid_vsb.set)
    grid_hsb.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    grid_vsb.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
    canvas.create_window(0, 0, window=grid_frame, anchor=tkinter.NW)

    # Empty label for origin
    origin_label = tkinter.Label(grid_frame, background=BACKGROUND_COLOUR)
    origin_label.grid(row=0, column=0, sticky=tkinter.NSEW, padx=(0, 1), pady=(0, 1))

    # Checks if save data exists and loads
    save_colours = []
    if check_file(SAVE_FILE):
        save_data = open(SAVE_FILE, 'r')
        with open(SAVE_FILE, 'r') as save_data:
            save_colours = [[int(x) for x in line.split()] for line in save_data]

    # Syndicate labels
    syndicate_members = list_files(SYNDICATE_PATH)
    syndicate_members.sort()
    syndicate_images = []
    syndicate_labels = []
    for i, syndicate_member in enumerate(syndicate_members):
        syndicate_name = syndicate_member.split('.')[0].replace('_', ' ')
        syndicate_images.append(ImageTk.PhotoImage(Image.open(os.path.join(SYNDICATE_PATH, syndicate_member)).resize((90, 90))))
        syndicate_labels.append(Cell(grid_frame, current_colour=save_colours[0][i] if save_colours else 0,
                                     image=syndicate_images[-1], text=syndicate_name, compound=tkinter.TOP,
                                     font=(None, 14)))
        syndicate_labels[-1].grid(row=0, column=i + 1, padx=1, pady=1)

    # Location labels
    location_list = list_files(LOCATION_PATH)
    location_list.sort()
    location_images = []
    location_labels = []
    for i, location_name in enumerate(location_list):
        location_images.append(ImageTk.PhotoImage(Image.open(os.path.join(LOCATION_PATH, location_name)).resize((45, 90))))
        location_labels.append(Cell(grid_frame, current_colour=save_colours[1][i] if save_colours else 0,
                                    image=location_images[-1]))
        location_labels[-1].grid(row=i+1, column=0, padx=1, pady=1, sticky=tkinter.NSEW)

    # Encounters
    encounter_images = [[None]*len(location_list) for i in range(len(syndicate_members))]
    encounter_labels = [[None]*len(location_list) for i in range(len(syndicate_members))]
    syndicate_encounters = list_folders(ENCOUNTER_PATH)
    syndicate_encounters.sort()
    for i, syndicate_encounter in enumerate(syndicate_encounters):
        location_encounters = list_files(os.path.join(ENCOUNTER_PATH, syndicate_encounter))
        location_encounters.sort()
        for j, location_encounter in enumerate(location_encounters):
            encounter_images[i][j] = Image.open(os.path.join(ENCOUNTER_PATH, syndicate_encounter, location_encounter))
            encounter_images[i][j] = ImageTk.PhotoImage(encounter_images[i][j].resize((int(encounter_images[i][j].width*0.9), int(encounter_images[i][j].height*0.9))))
            encounter_labels[i][j] = Cell(grid_frame, current_colour=save_colours[2 + i][j] if save_colours else 0,
                                          image=encounter_images[i][j], text=ENCOUNTERS_TEXT[i][j],
                                          font=(None, 12), wraplength=90, compound=tkinter.TOP)
            encounter_labels[i][j].grid(row=j+1, column=i+1, padx=1, pady=1, sticky=tkinter.NSEW)

    main_frame.pack(fill=tkinter.BOTH, expand=True)
    main_window.update()
    canvas.configure(scrollregion=canvas.bbox(tkinter.ALL))

    main_window.geometry(str(grid_frame.winfo_width()) + 'x' + str(grid_frame.winfo_height()))
    main_window.protocol('WM_DELETE_WINDOW', lambda: on_closing(main_window, syndicate_labels, location_labels, encounter_labels))
    main_window.bind('<Control-s>', lambda e: save_data_colours(syndicate_labels, location_labels, encounter_labels))
    main_window.mainloop()


