from Scripts.utilities.items import FindItem, FindNumberOfItems, MoveItem
from Scripts.glossary.colors import colors

#ore_chunk_ids = [
#    0x19B9,
#    0x19B7,
#    0x19BA,
#    0x19B8
#]

#ore_colors = [
    #0,
    #0x0973, # Dull Copper
    #0x0966, # Shadow Iron
    #0x096d, # Copper
    #0x08a5, # Golden
    #0x0979, # Agapite
    #0x0972, # Bronze
    #0x089f, # Verite
    #0x08ab # Valorite
#]

def ResetValues():
    Misc.RemoveSharedValue("book_1")
    Misc.RemoveSharedValue("book_2")
    Misc.RemoveSharedValue("current_book")
#    Misc.RemoveSharedValue("safe_place_rune")
#    Misc.RemoveSharedValue("store_ores_rune")
    Misc.RemoveSharedValue("recall_rune_index")
#    Misc.RemoveSharedValue("fire_beetle")

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
    rune = Misc.ReadSharedValue("book_" + index)
    if rune == 0:
        rune = Target.PromptTarget("Select runic atlas #" + index)
        Misc.SetSharedValue("book_" + index, rune)
    return rune

def CurrentBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 0:
        index = 1
        Misc.SetSharedValue("current_book", index)
    return index

def SetCurrentBook(index):
    Misc.SetSharedValue("current_book", index)
    
def SwitchBook():
    index = Misc.ReadSharedValue("current_book")
    if index == 1:
        index = 2
    else:
        index = 1
    Misc.SetSharedValue("current_book", index)    

def FlipPages(times):
    for i in range(times):
        Gumps.WaitForGump(498, 10000)
        Gumps.SendAction(498, 1150)  # Flip page
        Misc.Pause(800)
        Gumps.WaitForGump(498, 10000)

def RecallToMine(global_index):
    while Player.Mana < 11:
        Misc.Pause(1000)

    # Determine book and local rune index
    if global_index <= 48:
        book_index = 1
        local_index = global_index
    else:
        book_index = 2
        local_index = global_index - 48

    # Switch book if needed
    if CurrentBook() != book_index:
        SetCurrentBook(book_index)

    Items.UseItem(Book(CurrentBook()))
    Gumps.WaitForGump(498, 10000)

    # Flip to correct page
    flips = 0
    if local_index > 32:
        flips = 2
    elif local_index > 16:
        flips = 1
    FlipPages(flips)

    rune_button = 99 + local_index  # 100–147
    Gumps.SendAction(498, rune_button)
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
        0x08E7, # Stalagmites one
        0x08E8, # Flowstone One
        0x08E5, # Stalagmites Two
        0x08E4, # Stalagmites Three
        0x08E6, # Flowstone Two
        0x08E2, # Flowstone Three
        0x08E3, # Short Flowstone One
        0x08E1, # Stalagmites Four
        0x08E0, # Stalagmites Five
        0x08E9, # Stalagmites Six
        0x1726, # Small Jade Stone
        0x0DF8, # Large Jade Stone
        0x0F15, # Citrine
        0x0F10, # Emerald
        0x0F18, # Tourmaline
        0x0F26, # Diamond
        0x0F11, # Sapphire
        0x0F0F, # Star Sapphire
        0x0F13, # Ruby
        0x0F25, # Amber
        0x423A, # Sand
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
    CreatePickaxe()

    Spells.CastMagery("Mark")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(0x4055ABEA)
    Misc.Pause(3000)
    Spells.CastMagery("Recall")
    Target.WaitForTarget(5000, False)
    Target.TargetExecute(0x40AB5671)
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

#def Beetle():
#    beetle = Misc.ReadSharedValue('fire_beetle')
#    if beetle == 0:
#        beetle = Target.PromptTarget('Select your fire beetle')
#        if beetle:
#            Misc.SetSharedValue('fire_beetle', beetle)
#    return beetle

#def SmeltOres():
#    beetle = Mobiles.FindBySerial(Beetle())
#    if beetle == None:
#        Misc.SendMessage("No fire beetle found, alas!", colors['red'])
#        Misc.ScriptStop('Full Auto Mining With Firebeetle.py')
#        return
#
#    for ore_color in ore_colors:
#        ores = Items.FindAllByID(ore_chunk_ids, ore_color, Player.Backpack.Serial, -1)
#        if ores:
#            for ore in ores:
#                Items.UseItem(ore)
#                Target.WaitForTarget(4000, False)
#                Target.TargetExecute(beetle)
#                Misc.Pause(500)

def Mine():
    Journal.Clear()
    while (not Journal.SearchByName('There is no sand here to mine.', 'System') and
            not Journal.SearchByName('Target cannot be seen.', 'System') and
            not Journal.SearchByName('You can\'t mine there.', 'System')):
        if Player.Weight <= Player.MaxWeight:
            pickaxe = PreparePickaxe()
            Target.TargetResource(pickaxe, 1)
            Misc.Pause(1550)

            if Journal.SearchByType('Target cannot be seen.', 'Regular'):
                Journal.Clear()
                break

            Misc.Pause(500)
        else:
            Player.HeadMessage(colors['red'], '')

        if Player.Weight > Player.MaxWeight:
            Misc.SendMessage('', colors['cyan'])
#            SmeltOres()

            if Player.Weight + 176 >= Player.MaxWeight:
                RecallAndDump()

        # Wait a little bit so that the while loop doesn't consume as much CPU
        Misc.Pause(500)

    #Player.HeadMessage(colors['red'], 'No more ore to mine here!')

#ResetValues()
PrepareGumps()
#Beetle()
#SafePlaceRune()
#StoreOresRune()
Book(1)
Book(2)
#SmeltOres()
    
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
