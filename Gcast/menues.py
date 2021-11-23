def game_start():
    global game_st,W,H
    global rend,bill,slaves,map
    global kw, ks, ka, kd, shift
    global Tx,Ty

    rend,bill,map,slaves,Tx,Ty = 0,0,0,0,0,0
    rend, bill, map, slaves = start()

    kw, ks, ka, kd, shift = False, False, False, False, False
    pygame.mouse.set_visible(False)
    game_st = 1
    if not rend.is_alive():
        rend.start()
    
def game_finish():
    global finished
    finished = True
    
def game_resume():
    global game_paused
    game_paused = game_reset_mode(game_paused)
def game_return():
    global game_st
    game_st = 0
    rend.stop()
    rend.join()
    screen.fill(bl)
    
def game_reset_mode(paused):
    global game_st
    if paused == False:
        game_st = 2
        pygame.mouse.set_visible(True)
        rend.pause()
    if paused == True:
        game_st = 1
        pygame.mouse.set_visible(False)
        rend.resume()
    #pygame.mouse.set_pos((W//2,H//2))
    return not paused
