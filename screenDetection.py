import pygetwindow as gw

def screenDetect():
    deer_tab = gw.getActiveWindow()
    prev_tab = None
    i = 1
    counter = 0

    while True:
        curr_tab = gw.getActiveWindow()
        if curr_tab == deer_tab:
            i = 0
        else:
            if curr_tab != deer_tab and prev_tab != curr_tab and i == 0:
                print("Tab switched!")
                i = 1
                counter += 1
                if counter == 5:
                    return False
        prev_tab = curr_tab
