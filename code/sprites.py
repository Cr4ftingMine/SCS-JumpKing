from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # self.image.fill("red")  # sichtbar zum Debuggen
        # self.image.set_alpha(0)  # unsichtbar im Spiel
        self.rect = self.image.get_frect(topleft=pos)

class SlopeSprite(pygame.sprite.Sprite):
    def __init__(self,pos, image: pygame.Surface, *groups):
        super().__init__(*groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)
        self.heights = self.build_heightmap_from_alpha(self.image)
        

    def build_heightmap_from_alpha(self, surf: pygame.Surface):
        w, h = surf.get_size()
        alpha = pygame.surfarray.pixels_alpha(surf)
        heights = [h] * w
        for x in range(w):
            col = alpha[x]
            for y in range(h):
                if col[y] > 0:
                    heights[x] = y 
                    break
        del alpha
        return heights
    
    def y_on(self, x_world):
        x_local = int(max(0, min(self.rect.w - 1, x_world - self.rect.left)))
        y_local = self.heights[x_local]
        return self.rect.top + y_local
    
class SlipperySprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_frect(topleft=pos)

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image: pygame.Surface, name, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.smoothscale(image,(48,48))
        self.rect = self.image.get_frect(center=pos)
        self.name = name
        self.unique_id = None # set by Tiled
    
    def on_pickup(self,player):
        player.inventory.append(self)

    def use(self,player):
        pass

class TeleportStone(Item):
    def __init__(self, pos, target_pos=None, image: pygame.Surface = None, *groups):
        super().__init__(pos, image, "Teleportstein", *groups)
        self.target_pos = target_pos

    def use(self, player):
        print("Hier soll Magie passieren")
        player.hitbox.y -= 1000
        player.rect.midbottom = player.hitbox.midbottom

class JumpBoost(Item):
    def __init__(self, pos, image: pygame.Surface = None, *groups):
        super().__init__(pos, image, "JumpBoost", *groups)
        self.jump_boost_amount = 500
        self.jump_boost_duration = 5

    def use(self, player):
        print("Jump Boost")
        player.max_jump_power = player.max_jump_power + self.jump_boost_amount
        player.jump_boost_timer = self.jump_boost_duration
        print(f"Jump Boost aktiviert: {player.max_jump_power} für {self.jump_boost_duration} Sekunden!")

class Slowfall(Item):
    def __init__(self, pos, image: pygame.Surface = None, *groups):
        super().__init__(pos, image, "Slowfall", *groups)
        self.slowfall_factor = 0.35
        self.slowfall_duration = 5
    
    def use(self, player):
        print("Slowfall")
        player.slowfall_factor = self.slowfall_factor
        player.slowfall_timer = self.slowfall_duration
        print(f"Slowfall aktiviert: {self.slowfall_factor} für {self.slowfall_duration} Sekunden!")

class DoubleJump(Item):
    def __init__(self, pos, image: pygame.Surface = None, *groups):
        super().__init__(pos, image, "DoubleJump", *groups)

    def use(self, player):
        print("Double Jump")

class WallGrip(Item):
    def __init__(self, pos, image: pygame.Surface = None, *groups):
        super().__init__(pos, image, "WallGrip", *groups)
    
    def use(self, player):
        print("Wall Grip")

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, pos, image: pygame.Surface, group_all, *groups):
        super().__init__(*groups)
        self.image_red = image.convert_alpha()
        self.image_green = pygame.image.load(join("images", "tiles", "checkpoint_green.png")).convert_alpha()
        self.image = self.image_red
        self.rect = self.image.get_frect(topleft=pos)

        self.group_all = group_all
        self.active = False

    def set_active(self, is_active=True):
        if is_active:
            # Deactivate all other checkpoints
            for checkpoint in self.group_all:
                checkpoint.active = False
                checkpoint.image = checkpoint.image_red

        # Activate selected checkpoint
        self.active = is_active
        self.image = self.image_green if is_active else self.image_red
        
    def get_spawnpoint(self):
        return self.rect.midbottom

class ActionBlock(pygame.sprite.Sprite):
    def __init__(self, pos, image: pygame.Surface, *groups):
        super().__init__(*groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)

class DisappearingBlock(ActionBlock):
    def __init__(self, pos, image: pygame.Surface, collision_group = None, start_visible = True, *groups):
        super().__init__(pos, image, *groups)
        self.visible_image = self.image
        self.invisible_image = pygame.Surface(self.visible_image.get_size(), pygame.SRCALPHA)
        self.collision_group = collision_group
        self.visible = start_visible

        self.set_visible(self.visible)

    def set_visible(self, is_visible: bool):
        self.visible = is_visible
        self.image = self.visible_image if is_visible else self.invisible_image

        if is_visible:
            self.collision_group.add(self)
        else:
            self.collision_group.remove(self)

class Lever(ActionBlock):
    def __init__(self, pos, image: pygame.Surface, target_group: None, *groups):
        super().__init__(pos, image, *groups)
        self.image_off = self.image
        self.image_on = pygame.image.load(join("images", "tiles", "lever_right.png")).convert_alpha()
        self.target_group = target_group
        self.state_on = False

    def interact(self):
        self.state_on = not self.state_on
        self.image = self.image_on if self.state_on else self.image_off
        for block in self.target_group:
            if hasattr(block, "set_visible"):
                block.set_visible(not self.state_on)

class Key (ActionBlock):
    pass

class EndDoor (ActionBlock):
    pass