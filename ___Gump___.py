def UpdateLootMasterGump(color):
    var controller = Gumps.CreateGump()
    controller.x = 300
    controller.y = 300
    Gumps.AddPage(controller, 0)
    Gumps.AddBackground(controller, 0, 0, 140, 45, 1755)
    Gumps.AddButton(controller, 10, 8, 2152, 2151, 500, 1, 0)
    Gumps.AddLabel(controller, 50, 12, int(color), "Lootmaster")
    Gumps.CloseGump(13659823)
    controller.serial = Player.Serial
    controller.gumpId = 13659823
    Gumps.SendGump(controller, 150, 150)