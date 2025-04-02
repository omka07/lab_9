import pygame
import math
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (200, 200, 200)

# Tool modes
PEN = 0
SQUARE = 1
RIGHT_TRIANGLE = 2
EQUILATERAL_TRIANGLE = 3
RHOMBUS = 4

class PaintApp:
    def __init__(self):
        """Initialize the paint application"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Advanced Paint")
        
        self.clock = pygame.time.Clock()
        self.drawing = False
        self.last_pos = None
        self.color = BLACK
        self.brush_size = 3
        self.mode = PEN
        self.start_pos = None
        
        # Create drawing surface
        self.canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.canvas.fill(WHITE)
        
        # Available colors
        self.colors = [
            (RED, (10, 10)),
            (GREEN, (50, 10)),
            (BLUE, (90, 10)),
            (YELLOW, (130, 10)),
            (PURPLE, (170, 10)),
            (BLACK, (210, 10))
        ]
        
        # Tool buttons
        self.tools = [
            ("Pen", (250, 10), PEN),
            ("Square", (300, 10), SQUARE),
            ("R-Tri", (350, 10), RIGHT_TRIANGLE),
            ("E-Tri", (400, 10), EQUILATERAL_TRIANGLE),
            ("Rhombus", (450, 10), RHOMBUS)
        ]
        
        # Brush size buttons
        self.sizes = [
            ("Small", (550, 10), 3),
            ("Med", (600, 10), 5),
            ("Large", (650, 10), 8)
        ]

    def draw_ui(self):
        """Draw the user interface elements"""
        # Draw color palette
        for color, pos in self.colors:
            pygame.draw.rect(self.screen, color, (*pos, 30, 30))
            if color == self.color:
                pygame.draw.rect(self.screen, BLACK, (*pos, 30, 30), 2)
        
        # Draw tool buttons
        for text, pos, mode in self.tools:
            color = BLUE if self.mode == mode else GRAY
            pygame.draw.rect(self.screen, color, (*pos, 50, 30))
            text_surf = pygame.font.SysFont(None, 20).render(text, True, BLACK)
            self.screen.blit(text_surf, (pos[0] + 5, pos[1] + 5))
        
        # Draw brush size buttons
        for text, pos, size in self.sizes:
            color = BLUE if self.brush_size == size else GRAY
            pygame.draw.rect(self.screen, color, (*pos, 50, 30))
            text_surf = pygame.font.SysFont(None, 20).render(text, True, BLACK)
            self.screen.blit(text_surf, (pos[0] + 5, pos[1] + 5))
        
        # Draw clear button
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 100, 10, 80, 30))
        text_surf = pygame.font.SysFont(None, 20).render("Clear", True, WHITE)
        self.screen.blit(text_surf, (WINDOW_WIDTH - 90, 15))

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check if clicking on color palette
                    for color, pos in self.colors:
                        if pygame.Rect(*pos, 30, 30).collidepoint(event.pos):
                            self.color = color
                            return
                    
                    # Check if clicking on tool buttons
                    for _, pos, mode in self.tools:
                        if pygame.Rect(*pos, 50, 30).collidepoint(event.pos):
                            self.mode = mode
                            return
                    
                    # Check if clicking on size buttons
                    for _, pos, size in self.sizes:
                        if pygame.Rect(*pos, 50, 30).collidepoint(event.pos):
                            self.brush_size = size
                            return
                    
                    # Check if clicking clear button
                    if pygame.Rect(WINDOW_WIDTH - 100, 10, 80, 30).collidepoint(event.pos):
                        self.canvas.fill(WHITE)
                        return
                    
                    # Start drawing
                    self.drawing = True
                    self.last_pos = event.pos
                    self.start_pos = event.pos
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    if self.drawing and self.start_pos:
                        if self.mode == PEN:
                            self.draw_line(self.last_pos, event.pos)
                        else:
                            # Draw the final shape
                            self.draw_shape(self.start_pos, event.pos, True)
                    self.drawing = False
                    self.start_pos = None
            
            elif event.type == MOUSEMOTION and self.drawing:
                if self.mode == PEN:
                    self.draw_line(self.last_pos, event.pos)
                    self.last_pos = event.pos
                elif self.mode in [SQUARE, RIGHT_TRIANGLE, EQUILATERAL_TRIANGLE, RHOMBUS]:
                    # Redraw canvas to remove previous temporary shape
                    temp_canvas = self.canvas.copy()
                    self.draw_shape(self.start_pos, event.pos)
                    self.canvas.blit(temp_canvas, (0, 0))
                    self.draw_shape(self.start_pos, event.pos)

    def draw_line(self, start, end):
        """Draw a line between two points"""
        pygame.draw.line(self.canvas, self.color, start, end, self.brush_size)
        # Draw circles at the ends for smoother lines
        pygame.draw.circle(self.canvas, self.color, start, self.brush_size // 2)
        pygame.draw.circle(self.canvas, self.color, end, self.brush_size // 2)

    def draw_shape(self, start, end, final=False):
        """Draw the selected shape"""
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Determine top-left corner for rectangle-based shapes
        rect_x = min(x1, x2)
        rect_y = min(y1, y2)
        
        if self.mode == SQUARE:
            size = min(width, height)
            if final:
                pygame.draw.rect(self.canvas, self.color, 
                               (rect_x, rect_y, size, size), self.brush_size)
            else:
                # Draw temporary square
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(temp_surf, (*self.color, 128), (rect_x, rect_y, size, size), self.brush_size)
                self.screen.blit(temp_surf, (0, 0))
        
        elif self.mode == RIGHT_TRIANGLE:
            points = [(x1, y1), (x1, y2), (x2, y2)]
            if final:
                pygame.draw.polygon(self.canvas, self.color, points, self.brush_size)
            else:
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(temp_surf, (*self.color, 128), points, self.brush_size)
                self.screen.blit(temp_surf, (0, 0))
        
        elif self.mode == EQUILATERAL_TRIANGLE:
            height = math.sqrt(3) / 2 * width
            center_x = (x1 + x2) / 2
            points = [
                (center_x, y1),
                (x1, y1 + height),
                (x2, y1 + height)
            ]
            if final:
                pygame.draw.polygon(self.canvas, self.color, points, self.brush_size)
            else:
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(temp_surf, (*self.color, 128), points, self.brush_size)
                self.screen.blit(temp_surf, (0, 0))
        
        elif self.mode == RHOMBUS:
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            points = [
                (center_x, y1),
                (x2, center_y),
                (center_x, y2),
                (x1, center_y)
            ]
            if final:
                pygame.draw.polygon(self.canvas, self.color, points, self.brush_size)
            else:
                temp_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(temp_surf, (*self.color, 128), points, self.brush_size)
                self.screen.blit(temp_surf, (0, 0))

    def run(self):
        """Main application loop"""
        while True:
            self.screen.fill(WHITE)
            self.screen.blit(self.canvas, (0, 0))
            
            self.handle_events()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    app = PaintApp()
    app.run()