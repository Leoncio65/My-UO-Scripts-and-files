from Scripts.utilities.items import FindItem, FindNumberOfItems, MoveItem
from Scripts.glossary.colors import colors
import time
import threading

# You will need 2 FULL RUNIC ATLAS filled with mining recall locations. You also need 2 runes
# in the top layer of your backpack, One of these should be marked while standing next to your
# secured chest you have placed on the steps of your house. 

# As you start the script, it will have you select your firebeetle then your 2 mining atlas. 

# you will need to place the serial numbers for your secure chest and your 2 runes into the script. 
# Enter Chest Serial Number on line 417
# Enter Home Drop Off Rune Serial Number on line 457
# Enter Safe Place Rune (this is where you were mining when you need to drop off) on line 456


         
start_time = time.time()
Misc.SetSharedValue("script_start_time", start_time)
Misc.SetSharedValue("gump_loop_active", True)

def RuntimeGumpLoop():
    while Misc.ReadSharedValue("gump_loop_active"):
        UpdateStatusGump()
        time.sleep(3)

threading.Thread(target=RuntimeGumpLoop).start()

ore_chunk_ids = [0x19B9, 0x19B7, 0x19BA, 0x19B8]

ore_colors = [
    0,          # Iron
    0x0973,     # Dull Copper
    0x0966,     # Shadow Iron
    0x096d,     # Copper
    0x08a5,     # Golden
    0x0979,     # Agapite
    0x0972,     # Bronze
    0x089f,     # Verite
    0x08ab      # Valorite
]

# Snapshot containers for tracking cumulative gains
last_ingot_state = {}
last_gem_state = {}

def ResetCounters():
    ingots = [
        "iron", "dull_copper", "shadow_iron", "copper", "golden",
        "agapite", "bronze", "verite", "valorite"
    ]
    gems = [
        "sapphire", "ruby", "emerald", "diamond", "citrine", "amethyst",
        "star_sapphire", "tourmaline", "turquoise", "blue_diamond",
        "perfect_emerald", "ecru_citrine", "fire_ruby", "dark_sapphire",
        "crystalline_blackrock", "blackrock_piece", "amber"
    ]
    for ingot in ingots:
        Misc.SetSharedValue("ingot_" + ingot, 0)
    for gem in gems:
        Misc.SetSharedValue("gem_" + gem, 0)

def TrackIngotSmelts():
    ingot_ids = {
        0x1BF2: "iron", 0x1BF2: "dull_copper", 0x1BF2: "shadow_iron", 0x1BF2: "copper",
        0x1BF2: "golden", 0x1BF2: "agapite", 0x1BF2: "bronze", 0x1BF2: "verite", 0x1BF2: "valorite"
    }

    ingot_colors = {
        "iron": 0,
        "dull_copper": 0x973,
        "shadow_iron": 0x966,
        "copper": 0x96D,
        "golden": 0x8A5,
        "agapite": 0x979,
        "bronze": 0x972,
        "verite": 0x89F,
        "valorite": 0x8AB
    }

    global last_ingot_state
    current_ingot_state = {}

    for name, color in ingot_colors.items():
        ingots = Items.FindAllByID([0x1BF2], color, Player.Backpack.Serial, -1)
        total_amt = sum([ingot.Amount for ingot in ingots])
        current_ingot_state[name] = total_amt

        previous_amt = last_ingot_state.get(name, 0)
        smelted_amt = max(0, total_amt - previous_amt)

        Misc.SetSharedValue("ingot_" + name, Misc.ReadSharedValue("ingot_" + name) + smelted_amt)

    last_ingot_state = current_ingot_state
    
def SmeltOres():
    beetle = Mobiles.FindBySerial(Beetle())
    if beetle is None:
        Misc.SendMessage("No fire beetle found!", colors['red'])
        Misc.ScriptStop("Full Auto Mining With Firebeetle.py")
        return

    # Smelt everything visually
    ore_chunk_ids = [0x19B9, 0x19B7, 0x19BA, 0x19B8]
    ores = Items.FindAllByID(ore_chunk_ids, -1, Player.Backpack.Serial, -1)
    for ore in ores:
        Items.UseItem(ore)
        Target.WaitForTarget(4000, False)
        Target.TargetExecute(beetle)
        Misc.Pause(500)

    # After smelting, track new ingots
    TrackIngotSmelts()
    UpdateStatusGump()

def TrackGems():
    gem_ids = {
        0x0F11: "sapphire", 0x0F13: "ruby", 0x0F10: "emerald", 0x0F26: "diamond",
        0x0F15: "citrine", 0x0F16: "amethyst", 0x0F0F: "star_sapphire", 0x0F18: "tourmaline",
        0x3193: "turquoise", 0x3198: "blue_diamond", 0x3194: "perfect_emerald",
        0x3195: "ecru_citrine", 0x3197: "fire_ruby", 0x3192: "dark_sapphire",
        0x5732: "crystalline_blackrock", 0x0F28: "blackrock_piece", 0x0F25: "amber",
    }

    global last_gem_state
    current_gem_state = {}

    for item in Player.Backpack.Contains:
        name = gem_ids.get(item.ItemID)
        if name:
            current_gem_state[name] = current_gem_state.get(name, 0) + item.Amount

    for name, current_amt in current_gem_state.items():
        previous_amt = last_gem_state.get(name, 0)
        mined_amt = max(0, current_amt - previous_amt)
        Misc.SetSharedValue("gem_" + name, Misc.ReadSharedValue("gem_" + name) + mined_amt)

    last_gem_state = current_gem_state

def UpdateStatusGump():
    atlas_index = Misc.ReadSharedValue("current_book")
    rune_index = Misc.ReadSharedValue("recall_rune_index")

    gump = Gumps.CreateGump(movable=True)
    Gumps.AddPage(gump, 0)
    Gumps.AddBackground(gump, 0, 0, 360, 480, 9270)  # Slightly narrowed width
    Gumps.AddAlphaRegion(gump, 0, 0, 360, 480)
    
    Gumps.AddBackground(gump, 0, 0, 360, 40, 9270)
    Gumps.AddLabel(gump, 120, 12, 2122, "FULL  AUTO  MINER")



    # 🌟 Header (bright yellow)
    Gumps.AddLabel(gump, 90, 40, 2122, f"📜 Atlas Book: {atlas_index}    📍 Rune: {rune_index}")

    # 🔩 Ingots section
    Gumps.AddLabel(gump, 15, 60, 1152, "🔩 Ingots:")
    ingots = [
        "iron", "dull_copper", "shadow_iron", "copper", "golden",
        "agapite", "bronze", "verite", "valorite"
    ]
    y_ingot = 80
    for ingot in ingots:
        val = Misc.ReadSharedValue("ingot_" + ingot)
        label = ingot.replace("_", " ").title()
        Gumps.AddLabel(gump, 15, y_ingot, 33, f"{label}: {val}")
        y_ingot += 20

    # 💎 Gems section
    Gumps.AddLabel(gump, 185, 60, 1152, "💎 Gems:")
    gems = [
        "sapphire", "ruby", "emerald", "diamond", "citrine", "amethyst",
        "star_sapphire", "tourmaline", "turquoise", "blue_diamond",
        "perfect_emerald", "ecru_citrine", "fire_ruby", "dark_sapphire",
        "crystalline_blackrock", "blackrock_piece", "amber"
    ]
    y_gem = 80
    for gem in gems:
        val = Misc.ReadSharedValue("gem_" + gem)
        label = gem.replace("_", " ").title()
        Gumps.AddLabel(gump, 185, y_gem, 33, f"{label}: {val}")
        y_gem += 20

    # 🧱 Granite section (beneath ingots)
    Gumps.AddLabel(gump, 15, y_ingot + 10, 1152, "🧱 Granite:")
    granite_types = [
        "iron", "dull_copper", "shadow_iron", "copper", "golden",
        "agapite", "bronze", "verite", "valorite"
    ]
    y_granite = y_ingot + 30
    for granite in granite_types:
        val = Misc.ReadSharedValue("granite_" + granite)
        label = granite.replace("_", " ").title()
        Gumps.AddLabel(gump, 15, y_granite, 33, f"{label}: {val}")
        y_granite += 20   

    # 🎯 Final SendGump with movable position
    Gumps.SendGump(999001, Player.Serial, 100, 100, gump.gumpDefinition, gump.gumpStrings)
    
def Mine():
    Journal.Clear()
    while not any(Journal.SearchByName(t, "System") for t in [
        "There is no metal here to mine.",
        "Target cannot be seen.",
        "You can't mine there."
    ]):
        if Player.Weight <= Player.MaxWeight:
            pickaxe = PreparePickaxe()
            Target.TargetResource(pickaxe, 0)
            Misc.Pause(300)
            if Journal.SearchByType("Target cannot be seen.", "Regular"):
                Journal.Clear()
                break
            Misc.Pause(500)
            TrackGems()
        else:
            Player.HeadMessage(colors["red"], "")

        if Player.Weight > Player.MaxWeight:
            Misc.SendMessage("", colors["cyan"])
            SmeltOres()
            if Player.Weight + 176 >= Player.MaxWeight:
                RecallAndDump()

        Misc.Pause(500)

def ResetValues():
    Misc.RemoveSharedValue("book_1")
    Misc.RemoveSharedValue("book_2")
    Misc.RemoveSharedValue("current_book")
    Misc.RemoveSharedValue("recall_rune_index")
    Misc.RemoveSharedValue("fire_beetle")

def CreatePickaxe():
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    if tinkertools == None:
        #Misc.SendMessage("No tinker tools found!", colors['red'])
        Stop()

    #Player.HeadMessage(colors['yellow'], 'Creating new pickaxe...')
    Items.UseItem(tinkertools)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 323)
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 1)
    Gumps.WaitForGump(gumpid, 10000)
    Misc.Pause(1500)
    Gumps.SendAction(gumpid, 0)
    pickaxe = FindItem(0x0E86, Player.Backpack)
    Misc.Pause(500)
    return pickaxe

def PrepareGumps():
    global gumpid
    global gumpid2
    
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    Items.UseItem(tinkertools)
    Misc.Pause(500)
    gumpid = Gumps.CurrentGump( )
    #if you want to share it with other scripts
    #Misc.SetSharedValue("gumpid",Gumps.CurrentGump( ))
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 41)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 63)
    gumpid2 = Gumps.CurrentGump( )
    #if you want to share it with other scripts
    #Misc.SetSharedValue("gumpid2",Gumps.CurrentGump( ))
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 0)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 0)

def CreateTinkerTools():
        tinkertools = FindItem(0x1EB8, Player.Backpack)
        Items.UseItem(tinkertools)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 41)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 63)
        Gumps.WaitForGump(gumpid2, 10000)
        Gumps.SendAction(gumpid2, 1)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 0)
        Misc.Pause(500)
 
 
def Book(index):
    index = str(index)
    rune = Misc.ReadSharedValue("book_"+ index)
    if rune == 0:
        rune = Target.PromptTarget("Select runic atlas #"+ index +" with mining spots.")
        Misc.SetSharedValue("book_"+ index, rune)
    return rune

def CurrentBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 0:
        index = 1
        Misc.SetSharedValue("current_book", index)
    return index
    
def SwitchBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 1:
        index = 2
    else:
        index = 1
    Misc.SetSharedValue("current_book", index)
     
def CreatePickaxe():
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    if tinkertools == None:
        #Misc.SendMessage("No tinker tools found!", colors['red'])
        Stop()

    #Player.HeadMessage(colors['yellow'], 'Creating new pickaxe...')
    Items.UseItem(tinkertools)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 323)
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 1)
    Gumps.WaitForGump(gumpid, 10000)
    Misc.Pause(1500)
    Gumps.SendAction(gumpid, 0)
    pickaxe = FindItem(0x0E86, Player.Backpack)
    Misc.Pause(500)
    return pickaxe

def PrepareGumps():
    global gumpid
    global gumpid2
    
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    Items.UseItem(tinkertools)
    Misc.Pause(500)
    gumpid = Gumps.CurrentGump( )
    #if you want to share it with other scripts
    #Misc.SetSharedValue("gumpid",Gumps.CurrentGump( ))
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 41)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 63)
    gumpid2 = Gumps.CurrentGump( )
    #if you want to share it with other scripts
    #Misc.SetSharedValue("gumpid2",Gumps.CurrentGump( ))
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 0)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 0)

def CreateTinkerTools():
        tinkertools = FindItem(0x1EB8, Player.Backpack)
        Items.UseItem(tinkertools)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 41)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 63)
        Gumps.WaitForGump(gumpid2, 10000)
        Gumps.SendAction(gumpid2, 1)
        Gumps.WaitForGump(gumpid, 10000)
        Gumps.SendAction(gumpid, 0)
        Misc.Pause(500)
 
 
def Book(index):
    index = str(index)
    rune = Misc.ReadSharedValue("book_"+ index)
    if rune == 0:
        rune = Target.PromptTarget("Select runic atlas #"+ index +" with mining spots.")
        Misc.SetSharedValue("book_"+ index, rune)
    return rune

def CurrentBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 0:
        index = 1
        Misc.SetSharedValue("current_book", index)
    return index
    
def SwitchBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 1:
        index = 2
    else:
        index = 1
    Misc.SetSharedValue("current_book", index)
     
def FlipPage():
    Gumps.WaitForGump(498, 10000)
    Gumps.SendAction(498, 1150)  # Page flip button
    Gumps.WaitForGump(498, 10000)

def RecallToMine(index):
    while Player.Mana < 11:
        Misc.Pause(1000)

    Items.UseItem(Book(CurrentBook()))
    Gumps.WaitForGump(498, 10000)
    
    # Flip to the correct page based on index
    if index > 32:  # Third page (runes 33-48)
        FlipPage()
        FlipPage()
    elif index > 16:  # Second page (runes 17-32)
        FlipPage()
    
    Gumps.SendAction(498, 99 + index)  # Buttons 100-147 for runes 1-48
    Gumps.WaitForGump(498, 10000)
    Gumps.SendAction(498, 4)
    Misc.Pause(2500)

def DepositItems():
    chest = 0x4015307F
    Misc.Pause(1000)

    moveItemList = [
        0x1BF2, # Ingots
        0x0973, # Dull Copper
        0x0966, # Shadow Iron
        0x096d, # Copper
        0x08a5, # Golden
        0x0979, # Agapite
        0x0972, # Bronze
        0x089f, # Verite
        0x08ab, # Valorite
        0x3192, # Dark Sapphire
        0x3197, # Fire Ruby
        0x3195, # Ecru Citrine
        0x3198, # Blue Diamond
        0x3194, # Perfect Emerald
        0x3193, # Turquoise
        0x0F28, # Small Piece of Blackrock
        0x5732, # Crystalline Blackrock
        0x1779, # High quality Granite
        0x0F15, # Citrine
        0x0F10, # Emerald
        0x0F18, # Tourmaline
        0x0F26, # Diamond
        0x0F11, # Sapphire
        0x0F0F, # Star Sapphire
        0x0F13, # Ruby
        0x0F25, # Amber
        0x0F16  # Amethyst
     ]
    
    for item in Player.Backpack.Contains:
        if item.ItemID in moveItemList:
            Items.Move(item, chest, 0)
            Misc.Pause(1000)

def RecallAndDump():
    SafePlaceRune = 0x4055ABEA
    StoreOresRune = 0x40AB5671
    #Player.HeadMessage(colors['green'], "Time to drop off some weight!")
    #CreatePickaxe()

    Spells.CastMagery("Mark")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(SafePlaceRune)
    Misc.Pause(3000)
    Spells.CastMagery("Recall")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(StoreOresRune)
    Misc.Pause(5000)

    DepositItems()
    Misc.Pause(1000)

    Spells.CastMagery("Recall")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(SafePlaceRune)
    Misc.Pause(1000)

def PreparePickaxe():
    pickaxe = FindItem(0x0E86, Player.Backpack)
    tinkertools = FindItem(0x1EB8, Player.Backpack)

    if Items.BackpackCount(0x1EB8, 0) == 1:
        tinkertools = CreateTinkerTools()

    if Items.BackpackCount(0x0E86, 0) == 1:
        pickaxe = CreatePickaxe()

    return pickaxe

def Beetle():
    beetle = Misc.ReadSharedValue('fire_beetle')
    if beetle == 0:
        beetle = Target.PromptTarget('Select your fire beetle')
        if beetle:
            Misc.SetSharedValue('fire_beetle', beetle)
    return beetle

# 🏁 Startup routine
ResetCounters()
PrepareGumps()
Beetle()
Book(1)
Book(2)
SmeltOres()

try:
    while Player.Hits > 0:
        index = Misc.ReadSharedValue("recall_rune_index")
        if index == 0 or index == 48:
            index = 1
            SwitchBook()
        else:
            index += 1

        Misc.SetSharedValue("recall_rune_index", index)
        Misc.Pause(500)
        RecallToMine(index)
        UpdateStatusGump()
        Mine()
        Misc.Pause(350)

finally:
    Misc.SetSharedValue("gump_loop_active", False)