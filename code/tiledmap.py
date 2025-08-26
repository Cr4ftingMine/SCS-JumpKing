from settings import *
from pytmx.util_pygame import load_pygame
from sprites import CollisionSprite

class TiledMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width * TILE_SIZE
        self.height = self.tmx_data.height * TILE_SIZE
        self.layers = {layer.name: layer for layer in self.tmx_data.visible_layers}
        print(f"width: {self.width}, height: {self.height}")

        self.collision_sprites = pygame.sprite.Group()

        offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, gid in layer:
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props and props.get("collidable"):
                        pos = (x * TILE_SIZE, y * TILE_SIZE + offset_y)
                        size = (TILE_SIZE, TILE_SIZE)
                        #print(f"x: {x}, y: {y}, pos: {pos}, offset_y: {offset_y}")
                        CollisionSprite(pos, size, self.collision_sprites)

        #Map-Border
        left_wall_x = -TILE_SIZE
        right_wall_x = self.width
        wall_y = offset_y
        wall_height = self.height 

        CollisionSprite((left_wall_x, wall_y), (TILE_SIZE, wall_height), self.collision_sprites)
        CollisionSprite((right_wall_x, wall_y), (TILE_SIZE, wall_height), self.collision_sprites)


        #print(f"Loaded {len(self.collidable_rects)} collidable tiles.")



    # def draw(self, surface):
    #     #TODO: Kamera einbauen
    #     offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64

    #     for layer in self.tmx_data.visible_layers:
    #         if hasattr(layer, 'tiles'):
    #             for x, y, image in layer.tiles():
    #                 if image:
    #                     screen_x = x * TILE_SIZE
    #                     screen_y = y * TILE_SIZE + offset_y
    #                     surface.blit(image, (screen_x, screen_y))

    def draw(self, surface, camera):
        offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64
        
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, image in layer.tiles():
                    if image:
                        world_x = x * TILE_SIZE
                        world_y = y * TILE_SIZE + offset_y
                        screen_x = world_x
                        screen_y = world_y + camera.offset.y
                        surface.blit(image, (screen_x, screen_y))


    def update(self, dt):
        # Update the map state if necessary
        pass