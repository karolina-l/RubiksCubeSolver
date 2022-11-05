class Cube:

    def __init__(
            self,
            n=3,
            colors = ['r', 'g', 'b', 'w', 'o', 'y'],
            state = None
    ):
        if state is None:
            self.n = n
            self.colors = colors
            self.reset()
        else:
            self.n = int((len(state)/6)**(0.5))
            self.colors = []
            self.cube = [[[]]]
            for i, s in enumerate(state):
                if s not in self.colors:
                    self.colors.append(s)
                self.cube[-1][-1].append(s)
                if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                    self.cube[-1].append([])
# wtf xd
                elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                    self.cube.append([[]])

    def reset(self):
        self.cube = [[[c for x in range(self.n)] for y in range(self.n)] for c in self.colors]

    def solved(self):
        for side in self.cube:
            hold = []
            check = True
            for row in side:
                if len(set(row)) == 1:
                    hold.append(row[0])
                else:
                    check = False
                    break
            if check == False:
                break
            if len(set(hold)) > 1:
                check = False
                break
        return check

    def stringify(self):
        return ''.join([i for r in self.cube for s in r for i in s])

    def show(self):
        spacing = f'{" " * (len(str(self.cube[0][0])) + 1)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join(' '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')

    def horizontal_twist(self, row, direction):
        if direction == 0: # lewo
            self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],
                                                                                          self.cube[3][row],
                                                                                          self.cube[4][row],
                                                                                          self.cube[1][row])
        elif direction == 1: # prawo
            self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],
                                                                                          self.cube[1][row],
                                                                                          self.cube[2][row],
                                                                                          self.cube[3][row])
        else:
            print(f"Direction error. Values must be 0 or 1.")
            return

        if direction == 0: # lewo
            if row == 0:
                self.cube[0] = [list(x) for x in zip(*reversed(self.cube[0]))] #transpozycja GÓRA
            elif row == len(self.cube[0]) - 1:
                self.cube[5] = [list(x) for x in zip(*reversed(self.cube[5]))] # transpozycja DÓŁ
        elif direction == 1:
            if row == 0:
                self.cube[0] = [list(x) for x in zip(*self.cube[0])][::-1] # transpozycja GÓRA
            elif row == len(self.cube[0]) - 1:
                self.cube[5] = [list(x) for x in zip(*self.cube[5])][::-1] # transpozycja DÓŁ
        else:
            print(f"Row error. Values must be between 0 - 2")
            return

    def vertical_twist(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0:  # dół
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i - 1][-column - 1],\
                    self.cube[5][i][column] = (self.cube[4][-i - 1][-column - 1],
                                               self.cube[0][i][column],
                                               self.cube[5][i][column],
                                               self.cube[2][i][column])
                elif direction == 1: # góra
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i - 1][-column - 1],\
                    self.cube[5][i][column] = (self.cube[2][i][column],
                                               self.cube[5][i][column],
                                               self.cube[0][i][column],
                                               self.cube[4][-i - 1][-column - 1])
                else:
                    print(f"Direction error. Values must be 0 or 1.")
                    return
            if direction == 0: # dół
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*self.cube[1])][::-1] # transpozycja LEWA
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*self.cube[3])][::-1] # transpozycja PRAWA
            elif direction == 1: # góra
                if column == 0:
                    self.cube[1] = [list(x) for x in zip(*reversed(self.cube[1]))] # transpozycja LEWA
                elif column == len(self.cube[0]) - 1:
                    self.cube[3] = [list(x) for x in zip(*reversed(self.cube[3]))] # transpozycja PRAWA
            else:
                print(f"Column error. Values must be between 0 - 2")
                return

    def side_twist(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: # dół
                    self.cube[0][column][i], self.cube[1][-i - 1][column], self.cube[3][i][-column - 1], \
                    self.cube[5][-column - 1][-1 - i] = (self.cube[3][i][-column - 1],
                                                         self.cube[0][column][i],
                                                         self.cube[5][-column - 1][-1 - i],
                                                         self.cube[1][-i - 1][column])
                elif direction == 1:  # góra
                    self.cube[0][column][i], self.cube[1][-i - 1][column], self.cube[3][i][-column - 1], \
                    self.cube[5][-column - 1][-1 - i] = (self.cube[1][-i - 1][column],
                                                         self.cube[5][-column - 1][-1 - i],
                                                         self.cube[0][column][i],
                                                         self.cube[3][i][-column - 1])
                else:
                    print(f"Direction error. Values must be 0 or 1.")
                    return
            if direction == 0:  # dół
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*reversed(self.cube[4]))]  # transpozycja tył
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*reversed(self.cube[2]))]  # transpozycja przód
            elif direction == 1:  # góra
                if column == 0:
                    self.cube[4] = [list(x) for x in zip(*self.cube[4])][::-1]  # transpozycja tył
                elif column == len(self.cube[0]) - 1:
                    self.cube[2] = [list(x) for x in zip(*self.cube[2])][::-1]  # transpozycja przód
            else:
                print(f"Column error. Values must be between 0 - 2")
                return