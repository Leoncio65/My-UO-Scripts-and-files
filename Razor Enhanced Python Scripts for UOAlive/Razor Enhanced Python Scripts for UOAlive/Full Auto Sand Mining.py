from Scripts.utilities.items import FindItem, FindNumberOfItems, MoveItem
from Scripts.glossary.colors import colors

# DO NOT USE AFK!!!!!!!!!!!!!!!!
# Have 2 TinkerTools, 2 Pickaxe and about 100 iron ingots or as many as you need to stay out 
# as Sand does not weigh that much in the top layer of your backpack.
# You will need 2 FULL RUNIC ATLAS filled with mining recall locations. You also need 2 runes
# in the top layer of your backpack, One of these should be marked while standing next to your
# secured chest you have placed on the steps of your house. 

# As you start the script, it will have you select your 2 mining atlas. 

# you will need to place the serial numbers for your secure chest and your 2 runes into the script. 
# Enter Chest Serial Number on line 158
# Enter Home Drop Off Rune Serial Number on line 166
# Enter Safe Place Rune (this is where you were mining when you need to drop off) on line 165

Misc.SetSharedValue("sand_amount", 0)

def ResetCounters():
    Misc.SetSharedValue("sand_amount", 0)

def TrackSand():
    sand_items = Items.FindAllByID([0x423A], -1, Player.Backpack.Serial, -1)
    current_amt = sum([item.Amount for item in sand_items])
    Misc.SetSharedValue("sand_amount", current_amt)

def UpdateStatusGump():
    atlas_index = Misc.ReadSharedValue("current_book")
    rune_index = Misc.ReadSharedValue("recall_rune_index")
    sand_amt = Misc.ReadSharedValue("sand_amount")

    gump = Gumps.CreateGump(movable=True)
    Gumps.AddPage(gump, 0)
    Gumps.AddBackground(gump, 0, 0, 240, 120, 9270)
    Gumps.AddAlphaRegion(gump, 0, 0, 240, 120)
    Gumps.AddLabel(gump, 60, 12, 2122, "🏖️ Sand Miner")
    Gumps.AddLabel(gump, 20, 40, 2122, f"📘 Atlas: {atlas_index}    📍 Rune: {rune_index}")
    Gumps.AddLabel(gump, 20, 70, 33, f"🧱 Sand: {sand_amt}")
    Gumps.SendGump(999003, Player.Serial, 100, 100, gump.gumpDefinition, gump.gumpStrings)

def CreatePickaxe():
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    if not tinkertools:
        Misc.SendMessage("No tinker tools!", colors['red'])
        Stop()
    Items.UseItem(tinkertools)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 323)
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 1)
    Gumps.WaitForGump(gumpid, 10000)
    Misc.Pause(1500)
    Gumps.SendAction(gumpid, 0)
    return FindItem(0x0E86, Player.Backpack)

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

def PrepareGumps():
    global gumpid, gumpid2
    tinkertools = FindItem(0x1EB8, Player.Backpack)
    Items.UseItem(tinkertools)
    Misc.Pause(500)
    gumpid = Gumps.CurrentGump()
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 41)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 63)
    gumpid2 = Gumps.CurrentGump()
    Gumps.WaitForGump(gumpid2, 10000)
    Gumps.SendAction(gumpid2, 0)
    Gumps.WaitForGump(gumpid, 10000)
    Gumps.SendAction(gumpid, 0)

def PreparePickaxe():
    pickaxe = FindItem(0x0E86, Player.Backpack)
    if Items.BackpackCount(0x1EB8, 0) == 1:
        CreateTinkerTools()
    if Items.BackpackCount(0x0E86, 0) == 1:
        pickaxe = CreatePickaxe()
    return pickaxe

def Book(index):
    index = str(index)
    rune = Misc.ReadSharedValue("book_" + index)
    if rune == 0:
        rune = Target.PromptTarget("Select runic atlas #" + index + " with sand spots.")
        Misc.SetSharedValue("book_" + index, rune)
    return rune

def CurrentBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 0:
        index = 1
        Misc.SetSharedValue("current_book", index)
    return index

def SwitchBook():
    index = Misc.ReadSharedValue("current_book")
    index = 2 if index == 1 else 1
    Misc.SetSharedValue("current_book", index)

def FlipPage():
    Gumps.WaitForGump(498, 10000)
    Gumps.SendAction(498, 1150)
    Gumps.WaitForGump(498, 10000)

def RecallToMine(index):
    while Player.Mana < 11:
        Misc.Pause(1000)

    Items.UseItem(Book(CurrentBook()))
    Gumps.WaitForGump(498, 10000)

    if index > 32:
        FlipPage(); FlipPage()
    elif index > 16:
        FlipPage()

    Gumps.SendAction(498, 99 + index)
    Gumps.WaitForGump(498, 10000)
    Gumps.SendAction(498, 4)
    Misc.Pause(2500)

def Mine():
    Journal.Clear()
    while not any(Journal.SearchByName(t, "System") for t in [
        "There is no sand here to mine.",
        "Target cannot be seen.",
        "You can't mine there."
    ]):
        if Player.Weight + 50 <= Player.MaxWeight:
            pickaxe = PreparePickaxe()
            Target.TargetResource(pickaxe, 1)
            Misc.Pause(300)
            if Journal.SearchByType("Target cannot be seen.", "Regular"):
                Journal.Clear()
                break
            Misc.Pause(500)
            TrackSand()
            UpdateStatusGump()
        else:
            Misc.SendMessage("Too heavy to continue mining.", colors["red"])
            break
        Misc.Pause(500)
        
def DepositSand():
    chest_serial = 0x4015307F  # <-- Replace with your actual container serial
    sand_items = Items.FindAllByID([0x423A], -1, Player.Backpack.Serial, -1)
    for sand in sand_items:
        Items.Move(sand, chest_serial, 0)
        Misc.Pause(500)

def RecallAndDump():
    safe_rune = 0x592E75FD  # <-- Rune to return to mining spot
    drop_rune = 0x419A7E00  # <-- Rune for secure chest

    # 🪄 Mark safe spot for return
    Spells.CastMagery("Mark")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(safe_rune)
    Misc.Pause(3000)

    # 🔁 Recall to drop point
    Spells.CastMagery("Recall")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(drop_rune)
    Misc.Pause(5000)

    DepositSand()
    Misc.Pause(1000)

    # 🔁 Recall back to safe spot
    Spells.CastMagery("Recall")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(safe_rune)
    Misc.Pause(1500)

# 🏁 Startup Sequence
PrepareGumps()
Book(1)
Book(2)

while Player.Hits > 0:
    index = Misc.ReadSharedValue("recall_rune_index")

    if index == 0 or index > 48:
        index = 1
        SwitchBook()  # Flip to the other book after finishing all 48 runes
    else:
        index += 1
        
    Misc.SetSharedValue("recall_rune_index", index)
    Misc.Pause(500)
    RecallToMine(index)
    Mine()
    Misc.Pause(250)