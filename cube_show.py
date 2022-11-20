def cubeOrder(cube):
    cube_duplicate = 6 * [None]
    cube_duplicate[0] = cube[0]
    cube_duplicate[1] = cube[2]
    cube_duplicate[2] = cube[1]
    cube_duplicate[3] = cube[5]
    cube_duplicate[4] = cube[4]
    cube_duplicate[5] = cube[3]

    return cube_duplicate