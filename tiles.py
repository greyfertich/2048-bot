x_coords = [1231, 1335, 1450, 1580]
y_coords = [445, 557, 688, 808]

TILE_COORDINATES = [(x,y) for y in y_coords for x in x_coords]

def getTileFromColor(color):
    tiles = {
        (205, 186, 168, 255): 0,
        (233, 220, 205, 255): 2,
        (234, 218.5, 194, 255): 4,
        (246, 168, 115, 255): 8,
        (251, 139,  94, 255): 16,
        (254, 113,  89, 255): 32,
        (255,  84,  59, 255): 64,
        (237, 201, 111, 255): 128,
        (237, 198,  97, 255): 256,
        (238, 194,  83, 255): 512,
        (238, 190,  71, 255): 1024,
        (238.5, 187,  60.5, 255): 2048,
        ( 53,  51,  44, 255): 4096
    }
    closestTile = 0
    distance = float('inf')
    for tile in tiles:
        dis = (color[0]-tile[0])**2 + (color[1]-tile[1])**2 + (color[2]-tile[2])**2
        if dis < distance:
            closestTile = tiles[tile]
            distance = dis
    return closestTile
