from tkinter import *
import tkinter as tk
from tkinter import messagebox as msb
import os
import random

root = Tk()
root.geometry("144x144") # Wysokość i szerokość okna    

class board:

    boardWidth = 9
    boardHeight = 9
    bombAmount = 10
    flagsStanded = 0 

    vBoard = [[None]]       # definiuję vBoard czyli virtualną macierz buttonów, w celu napełnienia jej bombami i napełniania w niej pól obok odpowiednią liczbą, ktora wskazuje ile jest bomb obok niej
    bBoard = []             # definiuję bBoard czyli dwuwymiarową listę która w późniejszym etapie napełnana jest buttonami
    cBoard = []             # definiuję cBoard czyli dwuwymiarową tablicę w której zawarte będą informacje, czy button jest juz klikniety
    fBoard = []             # defuniuję fBoard czyli dwuwymiarowa listę, w której przechowujemy informacje, czy w danym miejscu stoi flaga

    button_toClick = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_toClick.png") # definiuję buttony, przypisuje nazwy do scieżek
    button_empty = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_empty.png")
    button_bombGray = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_bombGray.png")
    button_1 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_1.png")
    button_2 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_2.png")
    button_3 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_3.png")
    button_4 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_4.png")
    button_5 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_5.png")
    button_6 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_6.png")
    button_7 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_7.png")
    button_8 = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_8.png")
    button_flag = PhotoImage(file = r"C:\Users\Memek\source\repos\Minesweeper\button_flag.png")


    def __init__(self, master, boardWidth, boardHeight, bombAmount):

        self.master = master
        master.title("Minesweeper")

        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.bombAmount = bombAmount     
        
        board.vBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)] # napełniamy wszystkie tablice zerami
        board.cBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.rcBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.fBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.bombBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]


    def draw(self):            
          
        for x in range(board.boardHeight): # poniższe pętle tworzą dwuwymiarową listę oraz napełniają ją buttonami
            board.bBoard.append([])
            for y in range(board.boardWidth):
                board.bBoard[x].append(Button(root))
                btn = board.bBoard[x][y]
                btn.grid(column = y, row = x) # buttony są ustawiane na gridzie
                btn.config(height = 10, width = 10, image = board.button_toClick, relief = FLAT) # ustawiamy parametry buttonów
                btn["command"] = lambda btn=btn: board.click(btn) # przypisujemy funkcję click() do kazdego z buttonow
                btn.bind("<Button-3>", lambda x, btn=btn: board.rightClick(btn)) # bindujemy funkcję rightClick() do kazdego z przycisków w ten sposób,
                                                                                 # że wywołuje sie przy kliknieciu na przycisk prawym przyciskiem myszki

    def bombsFill(self): # ta funkcja napełnia vBord bombami, kompletnie randomowo

        bombsLeft = board.bombAmount # pobieramy ilosc bomb ze zmiennej zdefiniowanej wcześniej w klasie

        while bombsLeft != 0: 
            x = random.randint(0,8)
            y = random.randint(0,8) 
            if board.vBoard[x][y] != "bomb":
                board.vBoard[x][y] = "bomb"   
                board.bombBoard[x][y] = 1
                bombsLeft -= 1

           
    def checkNumbers(self): # ta funkcja napełnia pola w tablicy vBoard liczbą odzwierciedlającą ilość bomb, które leżą obok tych pól

         for x in range(board.boardHeight):
            for y in range(board.boardWidth):
                if board.vBoard[x][y] == "bomb":

                    if x > 0:
                        if board.vBoard[x-1][y] != "bomb":
                           board.vBoard[x-1][y] += 1
                    if x < 8:
                        if board.vBoard[x+1][y] != "bomb":
                           board.vBoard[x+1][y] += 1
                    if y > 0:
                        if board.vBoard[x][y-1] != "bomb":
                           board.vBoard[x][y-1] += 1
                    if y < 8:
                        if board.vBoard[x][y+1] != "bomb":
                           board.vBoard[x][y+1] += 1

                    if x < 8 and y < 8:
                        if board.vBoard[x+1][y+1] != "bomb":
                           board.vBoard[x+1][y+1] += 1
                    if x > 0 and y < 8:
                        if board.vBoard[x-1][y+1] != "bomb":
                           board.vBoard[x-1][y+1] += 1
                    if x > 0 and y > 0:
                        if board.vBoard[x-1][y-1] != "bomb":
                           board.vBoard[x-1][y-1] += 1
                    if x < 8 and y > 0:
                        if board.vBoard[x+1][y-1] != "bomb":
                           board.vBoard[x+1][y-1] += 1
    
    def click(button): # funkcja która wywołuje się po kliknieciu LPM na button. W zależności od tego jaka wartość znajduję sie w odpowiadającym
                       # polu w vBoard, to taka grafika buttonu zostanie przypisana. Kliknięte buttony również dostają 'command' = 0 czyli po ich kliknieciu nie dzieje sie od teraz nic

        board.rcBoard[board.buttonX(button)][board.buttonY(button)] = 1 # wrzucamy do rcBoard wartość 1, żeby nie mozna bylo na ten button kliknac prawym przyciskiem i postawić flagi
   
        if board.vBoard[board.buttonX(button)][board.buttonY(button)] == "bomb":
            button["image"] = board.button_bombGray
            button['command'] = 0
            board.restart()
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 1:
            button["image"] = board.button_1
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 2:
            button["image"] = board.button_2
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 3:
            button["image"] = board.button_3
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 4:
            button["image"] = board.button_4
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 5:
            button["image"] = board.button_5
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 6:
            button["image"] = board.button_6
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 7:
            button["image"] = board.button_7
            button['command'] = 0
        elif board.vBoard[board.buttonX(button)][board.buttonY(button)] == 8:
            button["image"] = board.button_8
            button['command'] = 0
        else:
            button["image"] = board.button_empty   
            button['command'] = 0

            board.cBoard[board.buttonX(button)][board.buttonY(button)] = 1 # tutaj oznaczamy ze button jest juz klikniety

            board.checkAutoClick(board.buttonX(button),board.buttonY(button)) # wywołujemy autoClick() czyli funkcje ktora sprawdza czy obok nie ma bomb, by wywołać autoClick()

        
    def checkAutoClick(x,y): # check auto click ma sprawdzac czy nie ma bomby i wywolywac autoclick

        if x < 8:
            if board.vBoard[x+1][y] != "bomb":
                board.autoClick(x+1,y)
        if y > 0:
            if board.vBoard[x][y-1] != "bomb":
                board.autoClick(x,y-1)
        if x > 0:
            if board.vBoard[x-1][y] != "bomb":
                board.autoClick(x-1,y)
        if y < 8:
            if board.vBoard[x][y+1] != "bomb":
                board.autoClick(x,y+1)
                

    def autoClick(x,y): # funkcja która wysołuje się, gdy klikniemy na puste pole. Zgodnie z zasadami minesweepera pokazuje wszystkie pola sąsiadujące, o ile nie
                        # są bombami, lub nie ma na nich flagi. Funkcja rekurencyjnie wywołuje samą siebie, dopóki nie napotka flag bomb. Zatrzymuje sie na polach z liczbami

        button = board.bBoard[x][y]

        if board.rcBoard[x][y] == 2: # jeżeli dla rcBoard mamy 2 czyli postawioną flage nie wywołujemy autoclick
            pass

        else:
             board.rcBoard[x][y] = 1             

             if board.vBoard[x][y] == 1:
                 button["image"] = board.button_1
                 button['command'] = 0
             elif board.vBoard[x][y] == 2:
                 button["image"] = board.button_2
                 button['command'] = 0
             elif board.vBoard[x][y] == 3:
                 button["image"] = board.button_3
                 button['command'] = 0
             elif board.vBoard[x][y] == 4:
                 button["image"] = board.button_4
                 button['command'] = 0
             elif board.vBoard[x][y] == 5:
                 button["image"] = board.button_5
                 button['command'] = 0
             elif board.vBoard[x][y] == 6:
                 button["image"] = board.button_6
                 button['command'] = 0
             elif board.vBoard[x][y] == 7:
                 button["image"] = board.button_7
                 button['command'] = 0
             elif board.vBoard[x][y] == 8:
                 button["image"] = board.button_8
                 button['command'] = 0
             else:
                 button["image"] = board.button_empty   
                 button['command'] = 0

                 board.cBoard[x][y] = 1 # oznaczamy ze button jest klikniety
                 board.rcBoard[x][y] = 1 # wrzucamy do rcBoard wartość 1, żeby nie mozna bylo na ten button kliknac prawym przyciskiem i postawić flagi
   
                                                        # ponizsze linijki sprawdzaja czy plansza sie nie konczy: || X-sy są w pionie, Y-ki w poziomie (wiem, dziwnie)

                 if x < 8:                              #   O O O      # S - tam gdzie aktualnie wywołuje się funkcja
                     if board.cBoard[x+1][y] != 1:      #   O S O      # X - tam gdzie sprawdzamy czy moze sie wywołać
                         board.autoClick(x+1, y)        #   O X O

                 if x > 0:                              #   O X O
                     if board.cBoard[x-1][y] != 1:      #   O S O
                         board.autoClick(x-1, y)        #   O O O

                 if y < 8:                              #   O O O
                     if board.cBoard[x][y+1] != 1:      #   O S X
                         board.autoClick(x, y+1)        #   O O O

                 if y > 0:                              #   O O O
                     if board.cBoard[x][y-1] != 1:      #   X S O
                         board.autoClick(x, y-1)        #   O O O


                 if x < 8 and y < 8:                    #   O O O
                     if board.cBoard[x+1][y+1] != 1:    #   O S O
                         board.autoClick(x+1, y+1)      #   O O X

                 if x < 8 and y > 0:                    #   O O X
                     if board.cBoard[x+1][y-1] != 1:    #   O S O
                         board.autoClick(x+1, y-1)      #   O O O

                 if x > 0 and y > 0:                    #   X O O
                     if board.cBoard[x-1][y-1] != 1:    #   O S O
                         board.autoClick(x-1, y-1)      #   O O O

                 if x > 0 and y < 8:                    #   O O O
                     if board.cBoard[x-1][y+1] != 1:    #   O S O
                         board.autoClick(x-1, y+1)      #   X O O


    def rightClick(button): # wywołuje się po kliknieciu PPM
                                                                               # sprawdza czy mozna kliknac w button prawym przyciskiem
                                                                               # 0 - nieklikniety     # 1 - nie mozna kliknac(odkryte)    # 2 - juz ma flage
        if board.rcBoard[board.buttonX(button)][board.buttonY(button)] == 0:   # jeśli nie ma flagi to ją stawiamy

            button["image"] = board.button_flag
            button['command'] = 0
            board.rcBoard[board.buttonX(button)][board.buttonY(button)] = 2
            board.flagsStanded += 1 # inkrementujemy liczbe postawionych flag
            board.fBoard[board.buttonX(button)][board.buttonY(button)] = 1
            print(board.flagsStanded)

        elif board.rcBoard[board.buttonX(button)][board.buttonY(button)] == 1: # jak juz ma flage to ją zdejmujemy i zmniejszamy ilosc flag
            board.fBoard[board.buttonX(button)][board.buttonY(button)] = 0
            board.flagsStanded -= 1
            pass

        else:                                                                  # jak juz ma flage to ją zdejmujemy i zmniejszamy ilosc flag, nadajemy z powrotem command = click()
            button["image"] = board.button_toClick
            button["command"] = lambda button=button: board.click(button)
            board.rcBoard[board.buttonX(button)][board.buttonY(button)] = 0     
            board.fBoard[board.buttonX(button)][board.buttonY(button)] = 0
            board.flagsStanded -= 1

        board.flagCheck()

    def buttonX(button): # zwraca wartość x buttona
        return button.grid_info()['row']

    def buttonY(button): # zwraca wartość y buttona
        return button.grid_info()['column']

    def flagCheck(): # sprawdza ilość flag na mapie. Jeśli oznaczymy wszystkie - wygrywamy
        if board.flagsStanded > 9:
            if board.bombBoard == board.fBoard:
                msb.showinfo("Info", "Wygrałeś! Gratulacje.") # wywołanie okna dialogowego
            
    def restart():

        msb.showinfo("Info", "Przegrałeś! Trafiłeś na bombę!") # wywołanie okna dialogowego

        board.vBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)] # napełniamy wszystkie tablice zerami
        board.cBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.rcBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.fBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]
        board.bombBoard = [[0 for x in range(board.boardHeight)] for y in range(board.boardWidth)]

        board.bombsFill(None)
        board.draw(None)
        board.checkNumbers(None)


minesweeper = board(root, 1,1,1)
minesweeper.draw()
minesweeper.bombsFill()
minesweeper.checkNumbers()
root.mainloop()
