TILES = {
    (200, 185, 173, 255): 0,
    (236, 224, 214, 255): 2,
    (236, 220, 195, 255): 4,
    (246, 168, 115, 255): 8,
    (251, 139,  94, 255): 16,
    (254, 113,  89, 255): 32,
    (255,  84,  59, 255): 64,
    (237, 201, 111, 255): 128,
    (237, 198,  97, 255): 256,
    (238, 194,  83, 255): 512,
    (238, 190,  71, 255): 1024,
    (239, 187,  60, 255): 2048
}

x_coords = [1231, 1335, 1450, 1580]
y_coords = [445, 557, 688, 808]

TILE_COORDINATES = [(x,y) for y in y_coords for x in x_coords]
