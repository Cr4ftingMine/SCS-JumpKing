from settings import *
from pytmx.util_pygame import load_pygame
from sprites import CollisionSprite, SlopeSprite, Item, TeleportStone, JumpBoost, Slowfall, DoubleJump, WallGrip, Checkpoint

class TiledMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width * TILE_SIZE
        self.height = self.tmx_data.height * TILE_SIZE
        self.layers = {layer.name: layer for layer in self.tmx_data.visible_layers}
        print(f"width: {self.width}, height: {self.height}")
        print(self.layers)

        self.collision_sprites = pygame.sprite.Group()
        self.slope_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.checkpoint_sprites = pygame.sprite.Group()


        offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles'):
                for x, y, gid in layer:
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props:
                        pos = (x * TILE_SIZE, y * TILE_SIZE + offset_y)
                        if props.get("collidable"):
                            #pos = (x * TILE_SIZE, y * TILE_SIZE + offset_y)
                            size = (TILE_SIZE, TILE_SIZE)
                            #print(f"x: {x}, y: {y}, pos: {pos}, offset_y: {offset_y}")
                            CollisionSprite(pos, size, self.collision_sprites)
                        if props.get("slope"):
                            image = self.tmx_data.get_tile_image_by_gid(gid)
                            #pos = (x * TILE_SIZE, y * TILE_SIZE + offset_y)
                            SlopeSprite(pos, image, self.slope_sprites)
                        if props.get("checkpoint"):
                            cp_image = self.tmx_data.get_tile_image_by_gid(gid)
                            Checkpoint(pos, cp_image, self.checkpoint_sprites, self.checkpoint_sprites)


                        item_type = props.get("item")
                        if item_type:
                            # Items are positioned by their center (Item.rect uses center) #!TODO: Erklärung
                            cx = pos[0] + TILE_SIZE / 2
                            cy = pos[1] + TILE_SIZE / 2
                            #print(f"cx: {cx}, x: {x * TILE_SIZE} - cy: {cy}, y:{y * TILE_SIZE}")
                            item_image = self.tmx_data.get_tile_image_by_gid(gid)

                            if item_type == "Teleportstone":
                                TeleportStone((cx, cy), None, item_image, self.item_sprites)

                            if item_type == "JumpBoost":
                                JumpBoost((cx, cy), item_image, self.item_sprites)
                            
                            if item_type == "Slowfall":
                                Slowfall((cx, cy), item_image, self.item_sprites)

                            if item_type == "DoubleJump":
                                DoubleJump((cx, cy), item_image, self.item_sprites)
                            
                            if item_type == "WallGrip":
                                WallGrip((cx, cy), item_image, self.item_sprites)
                        

                            

        print("Slopes: ", len(self.slope_sprites))
        print("Checkpoints: ", len(self.checkpoint_sprites))

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
            if hasattr(layer, 'tiles') and layer.name != "Items" and layer.name != "Checkpoint": # Items in extra Layer
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