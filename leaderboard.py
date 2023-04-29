import json
import pygame

from ui_manager import UIManager
from button import Button
from typing import List

class Score:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        
class Leaderboard:
    def __init__(self, game_manager):
        self.file_name = './assets/text_files/highscores.json'
        self.scores = []
        self.__game_manager = game_manager
        self.__ui_manager = UIManager()
        
    @property
    def game_manager(self):
        return self.__game_manager
    
    @property
    def ui_manager(self):
        return self.__ui_manager

    def load_scores(self):
        with open(self.file_name, 'r') as f:
            # Load leaderboard data from JSON file
            scores_json = json.load(f)
            scores = []
            
            for score in scores_json:
                scores.append(Score(score['name'], score['score']))
                
            return scores

    def save_scores(self):
        with open(self.file_name, 'w') as f:
            scores_json = []
            
            for score in self.scores:
                scores_json.append({'name': score.name, 'score': score.score})
                
            # Save updated leaderboard data back to JSON file
            json.dump(scores_json, f)

    def add_score(self, name, score):
        self.scores.append(Score(name, score))
        self.scores = self.sort_scores()
        self.save_scores()

    def sort_scores(self):
        # Sort leaderboard data in descending order by score and get top 10 scores
        return sorted(self.scores, key=lambda score: score.score, reverse=True)[:10]
    
    def setup_view_leaderboard_ui(self):
        
        # Load leaderboard data from file
        scores = self.load_scores()
        
        # Assign button position
        button_padding = 10
        button_x = self.game_manager.screen.get_width() - 200 - button_padding
        button_y = self.game_manager.screen.get_height() - 50 - button_padding

        # Add Back button in bottom right corner
        back_button = Button(self.game_manager.screen,
                            "Back",
                            button_x,
                            button_y)
            
        while not self.game_manager.game_over and not self.game_manager.quit_game:
    
          for event in pygame.event.get():

            # If the player clicks on cross icon in toolbar
            # Or if the player clicks on the quit button
            if event.type == pygame.QUIT:
                self.game_manager.quit_game = True
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.is_clicked(event):
                pass

            if not self.game_manager.game_over and not self.game_manager.quit_game:
              # Change background color
              self.game_manager.screen.fill((255, 255, 255))

              self.draw_box(scores)

              # Render "Back" button on the screen
              back_button.draw()

              pygame.display.update()

    
    def draw_box(self, scores: List[Score]):
        # Calculate the position of the box
        box_width = 850
        box_height = 500
        
        box_x = (self.game_manager.screen.get_width() - box_width) // 2
        box_y = ((self.game_manager.screen.get_height() - box_height) // 2) + 50

        # Display "Leaderboard" title
        title_font = pygame.font.Font("./assets/fonts/SuperMario256.ttf", 72)
        
        self.ui_manager.render_font(
            title_font, 
            box_x + 175, 
            box_y - 120, 
            "Leaderboard", 
            (255, 201, 60))

        # Create a surface for the leaderboard box
        box_surface = pygame.Surface((box_width, box_height))
        box_surface.set_alpha(200)  # Set the surface transparency
        box_surface.fill((150, 150, 150))  # Set the surface color

        # Display the headers
        header_font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 48)
        name_header_text = header_font.render("Name", True, (0, 0, 0))
        score_header_text = header_font.render("Score", True, (0, 0, 0))
        
        self.game_manager.screen.blit(name_header_text, (box_x + 195, box_y + 35))
        self.game_manager.screen.blit(score_header_text, (box_x + 480, box_y + 35))

        # Display the scores in the box
        font = pygame.font.Font("./assets/fonts/NiceSugar.ttf", 30)
        text_color = (0, 0, 0)
        text_x = box_x + box_width // 2
        text_y = box_y + 100
        line_spacing = 35

        # Display the leaderboard data
        for i, score in enumerate(scores):
            name_text = font.render(score.name, True, text_color)
            score_text = font.render(str(score.score), True, text_color)
            self.game_manager.screen.blit(name_text, (text_x - 215, text_y + i * line_spacing))
            self.game_manager.screen.blit(score_text, (text_x + 75, text_y + i * line_spacing))

        # Blit the box surface onto the screen
        self.game_manager.screen.blit(box_surface, (box_x, box_y))
        
    
# leaderboard = Leaderboard()
# leaderboard.add_score("Ashwin", 1000) // call this when the game is over and need to check how player can enter his name to the function
# sorted_scores = leaderboard.load_scores()
# for i, score in enumerate(sorted_scores):
#     print(f"{i+1}. {score.name} - {score.score}")
