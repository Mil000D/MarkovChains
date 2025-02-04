"""
Rock, Paper, Scissors Game with Markov Chains

This module contains the implementation of a Rock, Paper, Scissors game
using tkinter GUI and Markov chains for AI decision-making.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import dataclasses
from typing import Callable
import numpy as np


def check_result(player_selection: str, ai_selection: str) -> int:
    """
    Determine the result of a round of Rock-Paper-Scissors game.

    Args:
        player_selection (str): The player's selection ("Rock", "Paper", or "Scissors").
        ai_selection (str): The AI's selection ("Rock", "Paper", or "Scissors").

    Returns:
        int: Result of the round; 1 if the player wins, -1 if the AI wins, 0 if it's a tie.
    """
    possible_results = {
        ("Rock", "Scissors"): 1,
        ("Paper", "Rock"): 1,
        ("Scissors", "Paper"): 1,
        ("Rock", "Paper"): -1,
        ("Paper", "Scissors"): -1,
        ("Scissors", "Rock"): -1,
    }
    if (player_selection, ai_selection) in possible_results:
        result = possible_results[(player_selection, ai_selection)]
        return result
    return 0


def get_index(selection: str) -> int:
    """
    Get the index of the selection in the states array.

    Args:
        selection (str): The selection ("Rock", "Paper", or "Scissors").

    Returns:
        int: The index of the selection in the states array.
    """
    match selection:
        case "Rock":
            return 0
        case "Paper":
            return 1
        case "Scissors":
            return 2
        case _:
            return -1


@dataclasses.dataclass
class ButtonManager:
    """
    Manage the creation and functionality of buttons in the GUI.

    Attributes:
        play_game_func (Callable): The function to call when a button is clicked.
        button_frame (tk.Frame): The frame containing the buttons.
        rock_button (ttk.Button): The button for selecting Rock.
        paper_button (ttk.Button): The button for selecting Paper.
        scissors_button (ttk.Button): The button for selecting Scissors.
    """
    def __init__(self, root: tk.Tk, play_game_func: Callable) -> None:
        self.play_game_func = play_game_func
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        self.rock_button = self.create_button("Rock")
        self.paper_button = self.create_button("Paper")
        self.scissors_button = self.create_button("Scissors")

    def create_button(self, player_selection: str) -> ttk.Button:
        """
        Create and configure a button for a player selection.

        Args:
            player_selection (str): The player's selection ("Rock", "Paper", or "Scissors").

        Returns:
            ttk.Button: The created button.
        """
        button = ttk.Button(self.button_frame, text=player_selection,
                            command=lambda: self.play_game_func(player_selection),
                            width=10, padding=5)
        button.pack(side="left", padx=5, pady=5)
        button.configure(style="TButton")
        return button


@dataclasses.dataclass
class TopLabelManager:
    """
    Manage the top labels in the GUI.

    Attributes:
        round_label (tk.Label): Label displaying the current round number.
        ai_score_label (tk.Label): Label displaying the AI's score.
        player_score_label (tk.Label): Label displaying the player's score.
        label (tk.Label): Label prompting the player to select a move.
    """
    def __init__(self, root: tk.Tk, round_label: tk.Label,
                 ai_score_label: tk.Label, player_score_label: tk.Label) -> None:
        self.round_label = round_label
        self.round_label.pack()

        self.ai_score_label = ai_score_label
        self.ai_score_label.grid(row=0, column=0)
        self.player_score_label = player_score_label
        self.player_score_label.grid(row=0, column=1)

        self.label = tk.Label(root, text="Select your move:", font=("Arial", 16))
        self.label.pack()


@dataclasses.dataclass
class BottomLabelManager:
    """
    Manage the bottom labels in the GUI.

    Attributes:
        ai_selection_label (tk.Label): Label displaying the AI's selection.
        round_result_label (tk.Label): Label displaying the result of the round.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.ai_selection_label = tk.Label(root)
        self.ai_selection_label.pack()

        self.round_result_label = tk.Label(root, font=("Arial", 30))
        self.round_result_label.pack()


@dataclasses.dataclass
class WindowStyleManager:
    """
    Manage the style and appearance of the GUI window.

    Attributes:
        window_width (int): The width of the window.
        window_height (int): The height of the window.
    """
    def __init__(self, root: tk.Tk,
                 window_width: int = 500, window_height: int = 250) -> None:
        root.title("Rock, Paper, Scissors Game")
        self.window_width = window_width
        self.window_height = window_height
        self.style = ttk.Style(root)
        self.style.configure("TButton", font=("Arial", 16))
        self.center_window(root)

    def center_window(self, root: tk.Tk) -> None:
        """
        Center the window on the screen.

        Args:
            root (tk.Tk): The root window.
        """
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_axis = (screen_width // 2) - (self.window_width // 2)
        y_axis = (screen_height // 2) - (self.window_height // 2)

        root.geometry(f"{self.window_width}x{self.window_height}+{x_axis}+{y_axis}")


@dataclasses.dataclass
class GUIManager:
    """
    Manage the overall GUI components.

    Attributes:
        root (tk.Tk): The root window.
        top_label_manager (TopLabelManager): Manager for top labels.
        play_game_func (Callable): Function to play the game.
        button_manager (ButtonManager): Manager for buttons.
        bottom_label_manager (BottomLabelManager): Manager for bottom labels.
    """
    def __init__(self, root: tk.Tk, top_label_manager: TopLabelManager,
                 play_game_func: Callable) -> None:
        self.play_game_func = play_game_func
        self.root = root
        self.window_style_manager = WindowStyleManager(self.root)

        self.top_label_manager = top_label_manager

        self.button_manager = ButtonManager(self.root, self.play_game_func)

        self.bottom_label_manager = BottomLabelManager(self.root)


@dataclasses.dataclass
class PointsManager:
    """
    Manage points scored in the game.

    Attributes:
        all_ai_points (np.ndarray): Array storing points scored by AI.
        all_player_points (np.ndarray): Array storing points scored by the player.
    """
    def __init__(self, all_ai_points: np.ndarray, all_player_points: np.ndarray) -> None:
        self.all_ai_points = all_ai_points
        self.all_player_points = all_player_points


@dataclasses.dataclass
class TransitionManager:
    """
    Manage transitions between game states.

    Attributes:
        transition_matrix (np.ndarray): Matrix representing transition probabilities.
        transition_adjustment (float): Adjustment factor for transition probabilities.
    """
    def __init__(self) -> None:
        self.transition_matrix = np.array([[1 / 3, 1 / 3, 1 / 3],
                                           [1 / 3, 1 / 3, 1 / 3],
                                           [1 / 3, 1 / 3, 1 / 3]])
        self.transition_adjustment = 0.05

    def learn(self, previous_index: int, current_index: int) -> None:
        """
        Update transition probabilities based on the previous and current indices.

        Args:
            previous_index (int): Index representing the previous state.
            current_index (int): Index representing the current state.
        """
        i, j, k = ((current_index + 1) % 3, (current_index + 2) % 3, current_index)
        if (self.transition_matrix[previous_index][k] - self.transition_adjustment / 2 >= 0 and
                self.transition_matrix[previous_index][j] - self.transition_adjustment / 2 >= 0 and
                self.transition_matrix[previous_index][i] + self.transition_adjustment <= 1):
            self.transition_matrix[previous_index][k] -= self.transition_adjustment / 2
            self.transition_matrix[previous_index][j] -= self.transition_adjustment / 2
            self.transition_matrix[previous_index][i] += self.transition_adjustment


@dataclasses.dataclass
class GameManager:
    """
   Manage the game state.

   Attributes:
       num_of_games (int): Number of games played.
       num_round (int): Current round number.
   """
    def __init__(self, number_of_games: int) -> None:
        self.num_of_games = number_of_games
        self.num_round = 0


class RockPaperScissorsGame:
    """
    Main class to control the Rock, Paper, Scissors game.

    Attributes:
        states (np.ndarray): Array representing game states ("Rock", "Paper", "Scissors").
        transition_manager (TransitionManager): Manager for state transitions.
        game_manager (GameManager): Manager for the game state.
        points_manager (PointsManager): Manager for points scored.
        previous_user_selection (str): Previous user selection.
        gui_manager (GUIManager): Manager for GUI components.
    """
    def __init__(self, number_of_games: int = 30) -> None:
        self.states = np.array(["Rock", "Paper", "Scissors"])
        self.transition_manager = TransitionManager()
        self.game_manager = GameManager(number_of_games)
        self.points_manager = PointsManager(np.zeros(self.game_manager.num_of_games, dtype=int),
                                            np.zeros(self.game_manager.num_of_games, dtype=int))
        self.previous_user_selection = ""

        root = tk.Tk()
        score_frame = tk.Frame(root)
        score_frame.pack()
        round_label = tk.Label(root,
                               text=f"Round: {self.game_manager.num_round + 1}"
                                    f"/{self.game_manager.num_of_games}", font=("Arial", 16))
        ai_score_label = tk.Label(score_frame,
                                  text=f"AI's score: "
                                       f"{np.sum(self.points_manager.all_ai_points)}",
                                  font=("Arial", 16))
        player_score_label = tk.Label(score_frame,
                                      text=f"Player's score:"
                                           f" {np.sum(self.points_manager.all_player_points)}",
                                      font=("Arial", 16))
        self.top_label_manager = TopLabelManager(root,
                                                 round_label, ai_score_label, player_score_label)
        self.gui_manager = GUIManager(root, self.top_label_manager, self.play_game)

    def play_game(self, current_player_selection: str) -> None:
        """
        Play a round of the game.

        Args:
            current_player_selection (str): The player's current selection.
        """
        self.play_round(current_player_selection)
        self.update_scores()
        self.handle_end_game()

    def play_round(self, current_player_selection: str) -> None:
        """
        Play a round of the game.

        Args:
            current_player_selection (str): The player's current selection.
        """
        if self.game_manager.num_round == self.game_manager.num_of_games:
            self.reset_game()
        elif self.game_manager.num_round == 0:
            self.previous_user_selection = current_player_selection
            ai_selection = np.random.choice(self.states,
                                            p=self.transition_manager.transition_matrix[0])
            text = f"AI chose: {ai_selection}"
            self.gui_manager.bottom_label_manager.ai_selection_label.config(text=text,
                                                                            font=("Arial", 16))
            self.handle_results(current_player_selection, ai_selection)
            self.game_manager.num_round += 1
        else:
            previous_user_selection_index = get_index(self.previous_user_selection)
            current_user_selection_index = get_index(current_player_selection)
            probability = self.transition_manager.transition_matrix[previous_user_selection_index]
            ai_selection = np.random.choice(self.states,
                                            p=probability)
            text = f"AI chose: {ai_selection}"
            self.gui_manager.bottom_label_manager.ai_selection_label.config(text=text,
                                                                            font=("Arial", 16))
            self.transition_manager.learn(previous_user_selection_index,
                                          current_user_selection_index)
            self.handle_results(current_player_selection, ai_selection)
            self.previous_user_selection = current_player_selection
            self.game_manager.num_round += 1

    def handle_results(self, current_player_selection: str, ai_selection: str) -> None:
        """
        Handle the results of a round.

        Args:
            current_player_selection (str): The player's current selection.
            ai_selection (str): The AI's current selection.
        """
        result = check_result(current_player_selection, ai_selection)
        round_result = "You won!" if result == 1 else "You lost!" if result == -1 else "It's a tie!"
        self.gui_manager.bottom_label_manager.round_result_label.config(text=round_result)
        self.points_manager.all_player_points[self.game_manager.num_round] = result
        self.points_manager.all_ai_points[self.game_manager.num_round] = -result

    def handle_end_game(self) -> None:
        """
        Handle the end of the game.
        """
        max_score = np.max([np.sum(self.points_manager.all_ai_points),
                            np.sum(self.points_manager.all_player_points)])
        num_rounds_won = np.count_nonzero(self.points_manager.all_player_points == 1)
        num_rounds_lost = np.count_nonzero(self.points_manager.all_player_points == -1)
        num_rounds_tied = self.game_manager.num_round - num_rounds_lost - num_rounds_won

        if self.game_manager.num_round == self.game_manager.num_of_games:
            all_ai_points_sum = np.sum(self.points_manager.all_ai_points)
            all_player_points_sum = np.sum(self.points_manager.all_player_points)
            if all_ai_points_sum == all_player_points_sum:
                message = f"Tie \n" \
                          f"Player won {num_rounds_won} rounds, AI won {num_rounds_lost} rounds," \
                          f" and {num_rounds_tied} rounds were tied."
            else:
                winner = "AI" if all_ai_points_sum == max_score else "Player"
                message = f"{winner} wins with a score of {max_score} \n" \
                          f"Player won {num_rounds_won} rounds, AI won {num_rounds_lost} rounds," \
                          f" and {num_rounds_tied} rounds were tied."
            messagebox.askokcancel("Game Over", message)
        elif max_score == 10:
            winner = "AI" if np.sum(self.points_manager.all_ai_points) == max_score else "Player"
            messagebox.askokcancel("Game Over", f"{winner} wins with a score of {max_score}\n"
                                                f"Player won {num_rounds_won} rounds,"
                                                f" AI won {num_rounds_lost} rounds,"
                                                f" and {num_rounds_tied} rounds were tied.")
            play_again = messagebox.askyesno("Play Again", "Do you want to play again?")

            if play_again:
                self.reset_game()
            else:
                self.gui_manager.root.destroy()

    def reset_game(self) -> None:
        """
        Reset the game state.
        """
        self.game_manager.num_round = 0
        self.points_manager = PointsManager(np.zeros(self.game_manager.num_of_games, dtype=int),
                                            np.zeros(self.game_manager.num_of_games, dtype=int))
        self.previous_user_selection = ""
        self.gui_manager.top_label_manager.round_label.config(
            text=f"Round: {self.game_manager.num_round + 1}/{self.game_manager.num_of_games}")
        self.gui_manager.top_label_manager.ai_score_label.config(
            text=f"AI's score: {np.sum(self.points_manager.all_ai_points)}")
        self.gui_manager.top_label_manager.player_score_label.config(
            text=f"Player's score: {np.sum(self.points_manager.all_player_points)}")
        self.gui_manager.bottom_label_manager.ai_selection_label.config(text="")
        self.gui_manager.bottom_label_manager.round_result_label.config(text="")

    def update_scores(self) -> None:
        """
        Update the scores displayed in the GUI.
        """
        n_round = self.game_manager.num_round + 1 if self.game_manager.num_round + 1 <= 30 else 30
        n_games = self.game_manager.num_of_games
        self.gui_manager.top_label_manager.round_label.config(text=f"Round: {n_round}/"
                                                                   f"{n_games}")
        self.gui_manager.top_label_manager.ai_score_label.config(
            text=f"AI's score: {np.sum(self.points_manager.all_ai_points)}")
        self.gui_manager.top_label_manager.player_score_label.config(
            text=f"Player's score: {np.sum(self.points_manager.all_player_points)}")

    def start_game(self) -> None:
        """
        Start the game.
        """
        self.gui_manager.root.mainloop()


game = RockPaperScissorsGame()
game.start_game()
