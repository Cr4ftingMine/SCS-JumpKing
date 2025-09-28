from settings import *
from pytmx.util_pygame import load_pygame

from sprites import *

# Tiled Map handling
class TiledMap:
    def __init__(self, filename, enable_extensions):
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width * TILE_SIZE
        self.height = self.tmx_data.height * TILE_SIZE
        self.layers = {layer.name: layer for layer in self.tmx_data.visible_layers}
        self.enable_extensions = enable_extensions

        #print(f"width: {self.width}, height: {self.height}")
        #print(self.layers)

        # Sprite Groups for different types of sprites
        self.collision_sprites = pygame.sprite.Group()
        self.slope_sprites = pygame.sprite.Group()
        self.slippery_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.checkpoint_sprites = pygame.sprite.Group()
        self.actionblock_sprites = pygame.sprite.Group()
        self.starcoin_sprites = pygame.sprite.Group()

        
        offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64
        for layer in self.tmx_data.visible_layers: # Loop through all layers in the Tiled map
            if hasattr(layer, 'tiles'):
                for x, y, gid in layer:
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props:
                        pos = (x * TILE_SIZE, y * TILE_SIZE + offset_y)
                        size = (TILE_SIZE, TILE_SIZE)
                        if props.get("collidable"):
                            CollisionSprite(pos, size, self.collision_sprites)
                        if props.get("slippery"):
                            SlipperySprite(pos, size, self.slippery_sprites)
                        if props.get("slope"):
                            slope_image = self.tmx_data.get_tile_image_by_gid(gid)
                            SlopeSprite(pos, slope_image, self.slope_sprites)
                        if props.get("starcoin"):
                            cx = pos[0] + TILE_SIZE / 2
                            cy = pos[1] + TILE_SIZE / 2
                            starcoin_image = self.tmx_data.get_tile_image_by_gid(gid)
                            StarCoin((cx, cy), starcoin_image, self.starcoin_sprites)
                        if props.get("enddoor"):
                            enddoor_image = self.tmx_data.get_tile_image_by_gid(gid)
                            EndDoor(pos, enddoor_image, self.actionblock_sprites)
                            
                        # EXTENSIONS
                        if enable_extensions:
                            #Checkpoints
                            if props.get("checkpoint"):
                                cp_image = self.tmx_data.get_tile_image_by_gid(gid)
                                Checkpoint(pos, cp_image, self.checkpoint_sprites, self.checkpoint_sprites)

                            #Actionblocks
                            action_blocktype = props.get("action_block")
                            action_image = self.tmx_data.get_tile_image_by_gid(gid)
                            match action_blocktype:
                                case "disappearing_block":
                                    DisappearingBlock(pos, action_image, self.collision_sprites, True, self.actionblock_sprites)
                                case "lever":
                                    Lever(pos, action_image, self.actionblock_sprites, self.actionblock_sprites)
                                case _:
                                    pass

                            # Items
                            item_type = props.get("item")
                            if item_type:
                                # Items are positioned by their center (Item.rect uses center)
                                cx = pos[0] + TILE_SIZE / 2
                                cy = pos[1] + TILE_SIZE / 2
                                #print(f"cx: {cx}, x: {x * TILE_SIZE} - cy: {cy}, y:{y * TILE_SIZE}")
                                item_image = self.tmx_data.get_tile_image_by_gid(gid)
                            
                                match item_type:
                                    case "Teleportstone":
                                        TeleportStone((cx, cy), None, item_image, self.item_sprites)
                                    case "JumpBoost":
                                        JumpBoost((cx, cy), item_image, self.item_sprites)
                                    case "Slowfall":
                                        Slowfall((cx, cy), item_image, self.item_sprites)
                                    case _:
                                        print("Unbekanntes Item: ", item_type)

        # Debug output
        # print("Slopes: ", len(self.slope_sprites))
        # print("Eisflächen: ", len(self.slippery_sprites))
        # print("Checkpoints: ", len(self.checkpoint_sprites))
        # print("ActionBlock: ", len(self.actionblock_sprites))
        # print("StarCoin: ", len(self.starcoin_sprites))

        #Map-Border
        left_wall_x = -TILE_SIZE
        right_wall_x = self.width
        wall_y = offset_y
        wall_height = 2 * self.height

        CollisionSprite((left_wall_x, wall_y), (TILE_SIZE, wall_height), self.collision_sprites)
        CollisionSprite((right_wall_x, wall_y), (TILE_SIZE, wall_height), self.collision_sprites)
        #print(f"Loaded {len(self.collidable_rects)} collidable tiles.")

    # Draw the map onto a surface 
    def draw(self, surface, camera):
        offset_y = -149 * TILE_SIZE + WINDOW_HEIGHT - 64
        
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'tiles') and layer.name != "Items" and layer.name != "Checkpoint" and layer.name != "ActionBlock" and layer.name != "StarCoin": # Items in extra Layer
                for x, y, image in layer.tiles():
                    if image:
                        world_x = x * TILE_SIZE
                        world_y = y * TILE_SIZE + offset_y
                        screen_x = world_x
                        screen_y = world_y + camera.offset.y
                        surface.blit(image, (screen_x, screen_y))