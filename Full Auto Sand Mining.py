from Scripts.utilities.items import FindItem, FindNumberOfItems, MoveItem
from Scripts.glossary.colors import colors
import time

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

# 🏁 Startup Sequence
PrepareGumps()
Book(1)
Book(2)

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
        Mine()
        Misc.Pause(350)

finally:
    Misc.SetSharedValue("gump_loop_active", False)