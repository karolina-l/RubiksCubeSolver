def cubeOrder(cube):
    cube_duplicate = 6 * [None]
    cube_duplicate[0] = cube[0]
    cube_duplicate[1] = cube[2]
    cube_duplicate[2] = cube[1]
    cube_duplicate[3] = cube[5]
    cube_duplicate[4] = cube[4]
    cube_duplicate[5] = cube[3]

    return cube_duplicate

def flatten(l):
    return [item for sublist in l for item in sublist]

def showC(cube, window):
    rows = [None] * 3
    k = 0
    for row in range(0,7,3):
        tile_ctr = 0
        long_row = []
        for side in range(1,5):
            long_row.append(cube[side][row:row+3])
        long_row = flatten(long_row)
        rows[k] = long_row
        k += 1
    for j in range(3):
        tile_ctr = 0
        for i in range(12):
            if rows[j][tile_ctr] == 'r':
                window[f'C{j}{i}'].update(button_color='red')
            elif rows[j][tile_ctr] == 'g':
                window[f'C{j}{i}'].update(button_color='green')
            elif rows[j][tile_ctr] == 'b':
                window[f'C{j}{i}'].update(button_color='blue')
            elif rows[j][tile_ctr] == 'o':
                window[f'C{j}{i}'].update(button_color='orange')
            elif rows[j][tile_ctr] == 'w':
                window[f'C{j}{i}'].update(button_color='white')
            elif rows[j][tile_ctr] == 'y':
                window[f'C{j}{i}'].update(button_color='yellow')
            tile_ctr += 1


def showUD(face, ud_sig, window):
    tile_ctr = 0
    for j in range(3):
        for i in range(3):
            if face[tile_ctr] == 'r':
                window[f'{ud_sig}{j}{i}'].update(button_color='red')
            elif face[tile_ctr] == 'g':
                window[f'{ud_sig}{j}{i}'].update(button_color='green')
            elif face[tile_ctr] == 'b':
                window[f'{ud_sig}{j}{i}'].update(button_color='blue')
            elif face[tile_ctr] == 'o':
                window[f'{ud_sig}{j}{i}'].update(button_color='orange')
            elif face[tile_ctr] == 'w':
                window[f'{ud_sig}{j}{i}'].update(button_color='white')
            elif face[tile_ctr] == 'y':
                window[f'{ud_sig}{j}{i}'].update(button_color='yellow')
            tile_ctr += 1