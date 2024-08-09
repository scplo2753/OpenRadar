import pygame
import os

import config
from radar import Radar

MOUSEDRAGBUTTON = 3
MOUSEBRAABUTTON = 1

class App:
    """
    The main application class for the OpenRadar program.
    """

    def __init__(self, *args, **kwargs):
        self._running = True
        self.mouseDragDown = False
        self.mouseBRAADown = False
        self._startPan = (0,0)
        self._startBraa = (0,0)
        
    def on_init(self):
        
        window_x, window_y = config.app_config.get("window", "location", tuple[int,int]) # type: ignore
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_x},{window_y}"
        
        pygame.init()
        
        pygame.display.set_caption('OpenRadar') #TODO: add icon
        
        self.size: tuple[int, int] = config.app_config.get("window", "size", tuple[int,int]) # type: ignore
        self._display_surf = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self._radar = Radar(self._display_surf)
       
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18) 
        self._running = True
 
    def on_event(self, event: pygame.event.Event):
        """
        Handles the various events triggered by the user.
        """
        #TODO Consider refactor
        
        if event.type == pygame.QUIT:
            self._running = False
            
        elif event.type == pygame.WINDOWMOVED:
            config.app_config.set("window", "location", (event.x, event.y))
            
        elif event.type == pygame.WINDOWRESIZED:
            self.size = self.width, self.height = event.x, event.y
            self._radar.resize(self.width, self.height)
            config.app_config.set("window", "size", self.size)
            
        elif event.type == pygame.MOUSEWHEEL:
            if event.y != 0:
                self._radar.zoom(pygame.mouse.get_pos(), event.y)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == MOUSEDRAGBUTTON:
                self.mouseDragDown = True
                self._startPan = event.pos
            elif event.button == MOUSEBRAABUTTON:
                self.mouseBRAADown = True
                self._startBraa = event.pos

        elif event.type == pygame.MOUSEMOTION:
            if self.mouseDragDown: # dragging
                difX = event.pos[0] - self._startPan[0]
                difY = event.pos[1] - self._startPan[1]
                self._radar.pan((difX,difY)) 
                self._startPan = event.pos
            if self.mouseBRAADown:
                self._radar.braa(True, self._startBraa, event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == MOUSEDRAGBUTTON:
                self.mouseDragDown = False
            elif event.button == MOUSEBRAABUTTON:
                self.mouseBRAADown = False
                self._radar.braa(False)
            
    def on_loop(self):
        """
        Performs any necessary updates or calculations for the application.
        """
        self._radar.on_loop()
        pass
    
    def on_render(self):
        """
        Renders the application by filling the display with a grey color, rendering the radar, and displaying the FPS counter.
        """
        self._display_surf.fill((50,50,50)) # Fill grey
        self._radar.on_render()
        self.fps_counter()
          
        pygame.display.flip()
    
    def on_cleanup(self):
        """
        Cleans up and quits the application.
        """
        pygame.quit()
 
    def on_execute(self):
        """
        This is the main Loop
        """
        if self.on_init() == False:
            self._running = False
 
        #TODO framerate limit
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick()
            
        self.on_cleanup()
        
    def fps_counter(self):
        """
        Displays the current FPS (frames per second) on the top left corner of the display.
        """
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"))
        self._display_surf.blit(fps_t,(0,0))
            
