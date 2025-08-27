"""
Dashboard module for Bamboo Productivity app.
Handles the main menu and module selection interface.
"""

import os
import sys
from .pomodoro import Pomodoro
from .habits import Habits
from .tasks import Tasks
from .templates import Templates
from .settings import Settings
from .help import Help


class Dashboard:
    """
    Main dashboard for navigating between productivity modules.
    Provides keyboard-driven interface for module selection.
    """
    
    def __init__(self):
        """Initialize dashboard with available modules."""
        self.modules = [
            {'name': 'Pomodoro', 'class': Pomodoro, 'description': 'Focus timer with session tracking'},
            {'name': 'Habits', 'class': Habits, 'description': 'Daily habit tracking and streaks'},
            {'name': 'Tasks', 'class': Tasks, 'description': 'Task management with subtasks'},
            {'name': 'Templates', 'class': Templates, 'description': 'Manage habit templates'},
            {'name': 'Settings', 'class': Settings, 'description': 'App configuration and vault management'},
            {'name': 'Help', 'class': Help, 'description': 'Keybinds and usage instructions'}
        ]
        self.current_selection = 0
        self.running = True

    def run(self):
        """Main dashboard loop."""
        while self.running:
            self.display()
            self.handle_input()

    def display(self):
        """Display the dashboard with module selection."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           🎋 Bamboo Productivity     │")
        print("├─────────────────────────────────────┤")
        
        for i, module in enumerate(self.modules):
            prefix = "► " if i == self.current_selection else "  "
            print(f"│ {prefix}{module['name']:<12} - {module['description']:<20} │")
        
        print("├─────────────────────────────────────┤")
        print("│ ↑↓: Navigate  Enter: Select  Esc: Exit │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")  # Reset color

    def handle_input(self):
        """Handle keyboard input for navigation."""
        import termios
        import tty
        
        # Get single character input without Enter
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape sequence
                key += sys.stdin.read(2)
                if key == '\x1b[A':  # Up arrow
                    self.current_selection = (self.current_selection - 1) % len(self.modules)
                elif key == '\x1b[B':  # Down arrow
                    self.current_selection = (self.current_selection + 1) % len(self.modules)
                elif key == '\x1b':  # Esc alone
                    self.running = False
            elif key == '\r' or key == '\n':  # Enter
                self.select_module()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def select_module(self):
        """Launch the selected module."""
        selected_module = self.modules[self.current_selection]
        module_instance = selected_module['class']()
        module_instance.run()
