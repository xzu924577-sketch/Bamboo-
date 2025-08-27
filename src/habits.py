"""
Habits module for Bamboo Productivity app.
Handles daily habit tracking, streaks, and template-based logging.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


class Habits:
    """
    Daily habit tracking with streak calculation and template support.
    Each habit gets its own folder with daily markdown logs.
    """
    
    def __init__(self):
        """Initialize Habits module."""
        self.current_date = datetime.now().date()
        self.selected_habit = None
        self.habit_list = []
        self.current_selection = 0
        self.running = True

    def run(self):
        """Main Habits module loop."""
        self.load_habits()
        while self.running:
            self.display_menu()
            self.handle_input()

    def display_menu(self):
        """Display habits main menu with habit list."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           📝 Habit Tracker           │")
        print("├─────────────────────────────────────┤")
        print(f"│ Date: {self.current_date.strftime('%Y-%m-%d')}             │")
        print("├─────────────────────────────────────┤")
        
        if not self.habit_list:
            print("│  No habits found. Create one first! │")
        else:
            for i, habit in enumerate(self.habit_list):
                prefix = "► " if i == self.current_selection else "  "
                streak = self.calculate_streak(habit)
                print(f"│ {prefix}{habit:<15} [Streak: {streak:>3}]    │")
        
        print("├─────────────────────────────────────┤")
        print("│ Enter: Log habit  C: Create habit   │")
        print("│ D: Jump to date   R: Today          │")
        print("│ N: Previous day   M: Next day       │")
        print("│ Esc: Back to dashboard              │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def handle_input(self):
        """Handle keyboard input for habits navigation."""
        # Placeholder for input handling
        pass

    def load_habits(self):
        """Load list of available habits from vault."""
        # Placeholder for loading habits from vault
        pass

    def create_habit(self):
        """Create a new habit with template selection."""
        # Placeholder for habit creation
        pass

    def log_habit(self, habit_name):
        """
        Log entry for selected habit on current date.
        
        Args:
            habit_name (str): Name of the habit to log
        """
        # Placeholder for habit logging
        pass

    def display_habit_form(self, habit_name, template_data):
        """
        Display form for logging habit data.
        
        Args:
            habit_name (str): Name of the habit
            template_data (dict): Template structure for the habit
        """
        # Placeholder for habit form display
        pass

    def save_habit_log(self, habit_name, log_data):
        """
        Save habit log to markdown file.
        
        Args:
            habit_name (str): Name of the habit
            log_data (dict): Log entry data
        """
        # Placeholder for saving habit log
        pass

    def calculate_streak(self, habit_name):
        """
        Calculate current streak for a habit.
        
        Args:
            habit_name (str): Name of the habit
            
        Returns:
            int: Current streak count
        """
        # Placeholder for streak calculation
        return 0

    def get_habit_stats(self, habit_name):
        """
        Get statistics for a habit (current streak, best streak, etc.).
        
        Args:
            habit_name (str): Name of the habit
            
        Returns:
            dict: Habit statistics
        """
        # Placeholder for habit statistics
        return {
            'current_streak': 0,
            'best_streak': 0,
            'total_entries': 0,
            'last_logged': None
        }

    def jump_to_date(self):
        """Allow user to jump to a specific date."""
        # Placeholder for date jumping
        pass

    def navigate_date(self, direction):
        """
        Navigate to previous or next day.
        
        Args:
            direction (str): 'prev' or 'next'
        """
        if direction == 'prev':
            self.current_date -= timedelta(days=1)
        elif direction == 'next':
            self.current_date += timedelta(days=1)

    def get_vault_path(self):
        """Get the current vault path from settings."""
        # Placeholder for vault path retrieval
        pass

    def create_habit_filename(self, habit_name, date):
        """
        Create filename for habit log.
        
        Args:
            habit_name (str): Name of the habit
            date (datetime.date): Date of the log
            
        Returns:
            str: Formatted filename
        """
        return f"{habit_name}-{date.strftime('%Y-%m-%d')}.md"