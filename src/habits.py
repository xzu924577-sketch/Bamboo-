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
        # Load settings and vault path
        from .settings import Settings
        self.settings = Settings()
        
        self.current_date = datetime.now().date()
        self.selected_habit = None
        self.habit_list = []
        self.current_selection = 0
        self.running = True
        self.view_mode = 'list'  # 'list', 'log_habit', 'create_habit'
        
        # Navigation state
        self.menu_items = [
            "Log selected habit",
            "Create new habit", 
            "View habit statistics",
            "Manage templates",
            "Back to dashboard"
        ]

    def run(self):
        """Main Habits module loop."""
        self.load_habits()
        while self.running:
            if self.view_mode == 'list':
                self.display_habits_list()
                self.handle_list_input()
            elif self.view_mode == 'log_habit':
                self.log_selected_habit()
            elif self.view_mode == 'create_habit':
                self.create_new_habit()
            else:
                self.view_mode = 'list'

    def display_menu(self):
        """Display habits main menu (alias for display_habits_list)."""
        self.display_habits_list()

    def display_habits_list(self):
        """Display the main habits list with date and completion status."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           📝 Habit Tracker           │")
        print("├─────────────────────────────────────┤")
        print(f"│ Date: {self.current_date.strftime('%Y-%m-%d')} ({self._get_day_name()})     │")
        print("├─────────────────────────────────────┤")
        
        if not self.habit_list:
            print("│                                     │")
            print("│  No habits found.                   │")
            print("│  Press C to create your first habit │")
            print("│                                     │")
        else:
            print("│ Habit                    Done  Streak│")
            print("├─────────────────────────────────────┤")
            
            for i, habit in enumerate(self.habit_list):
                prefix = "► " if i == self.current_selection else "  "
                is_completed = self._is_habit_completed_today(habit)
                completion_icon = "✓" if is_completed else "○"
                current_streak = self.calculate_streak(habit)
                
                # Truncate habit name if too long
                habit_display = habit[:20] if len(habit) <= 20 else habit[:17] + "..."
                
                print(f"│{prefix}{habit_display:<21} [{completion_icon}]  {current_streak:>3} │")
        
        print("├─────────────────────────────────────┤")
        print("│ Enter: Log habit  C: Create habit   │")
        print("│ Space: Quick toggle completion      │")
        print("│ D: Jump to date   R: Today          │")
        print("│ N: Previous day   M: Next day       │")
        print("│ S: Statistics     Esc: Back         │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def _get_day_name(self):
        """Get the day name for current date."""
        today = datetime.now().date()
        if self.current_date == today:
            return "Today"
        elif self.current_date == today - timedelta(days=1):
            return "Yesterday"
        elif self.current_date == today + timedelta(days=1):
            return "Tomorrow"
        else:
            return self.current_date.strftime("%A")

    def handle_list_input(self):
        """Handle keyboard input for habits list navigation."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape sequence or single escape
                try:
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':  # Up arrow
                        if self.habit_list:
                            self.current_selection = (self.current_selection - 1) % len(self.habit_list)
                    elif key == '\x1b[B':  # Down arrow
                        if self.habit_list:
                            self.current_selection = (self.current_selection + 1) % len(self.habit_list)
                except:
                    # Single Esc - go back
                    self.running = False
            elif key == '\r' or key == '\n':  # Enter - log selected habit
                if self.habit_list:
                    self.selected_habit = self.habit_list[self.current_selection]
                    self.view_mode = 'log_habit'
            elif key == ' ':  # Space - quick toggle completion
                if self.habit_list:
                    self._quick_toggle_habit(self.habit_list[self.current_selection])
            elif key.lower() == 'c':  # Create new habit
                self.view_mode = 'create_habit'
            elif key.lower() == 'd':  # Jump to date
                self._jump_to_date()
            elif key.lower() == 'r':  # Return to today
                self.current_date = datetime.now().date()
                self.current_selection = 0
            elif key.lower() == 'n':  # Previous day
                self.current_date -= timedelta(days=1)
            elif key.lower() == 'm':  # Next day
                self.current_date += timedelta(days=1)
            elif key.lower() == 's':  # Statistics
                self._show_statistics()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def load_habits(self):
        """Load list of available habits from vault."""
        vault_path = self.get_vault_path()
        if not vault_path:
            self.habit_list = []
            return
        
        habits_dir = Path(vault_path) / "Habits"
        if not habits_dir.exists():
            habits_dir.mkdir(exist_ok=True)
            self.habit_list = []
            return
        
        # Get all habit directories
        self.habit_list = []
        for item in habits_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                self.habit_list.append(item.name)
        
        self.habit_list.sort()  # Alphabetical order

    def get_vault_path(self):
        """Get the current vault path from settings."""
        vault_path = self.settings.get_vault_path()
        
        # If no vault path found, try to load config
        if not vault_path:
            config = self.settings.load_config()
            vault_path = config.get('vault_path')
        
        return vault_path

    def _is_habit_completed_today(self, habit_name):
        """Check if habit has been logged for current date."""
        habit_file = self._get_habit_file_path(habit_name, self.current_date)
        return habit_file.exists() if habit_file else False

    def _get_habit_file_path(self, habit_name, date):
        """Get the file path for a habit on a specific date."""
        vault_path = self.get_vault_path()
        if not vault_path:
            return None
        
        habits_dir = Path(vault_path) / "Habits" / habit_name
        filename = f"{habit_name}-{date.strftime('%Y-%m-%d')}.md"
        return habits_dir / filename

    def _quick_toggle_habit(self, habit_name):
        """Quick toggle habit completion (simple yes/no log)."""
        habit_file = self._get_habit_file_path(habit_name, self.current_date)
        
        if habit_file and habit_file.exists():
            # Already logged - show message
            self._show_message("Habit already logged today!\nPress Enter to edit or Space to continue.")
            return
        
        # Create simple completion log
        if habit_file:
            habit_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""# Habit: {habit_name}
Date: {self.current_date.strftime('%Y-%m-%d')}
Time: {datetime.now().strftime('%H:%M')}

## Completion
- Completed: Yes

## Notes
- Quick completion logged
"""
            
            try:
                with open(habit_file, 'w') as f:
                    f.write(content)
                self._show_message(f"✓ {habit_name} marked complete!")
            except Exception as e:
                self._show_message(f"Error saving habit: {e}")

    def _show_message(self, message, wait_time=1.5):
        """Show a temporary message to user."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│              Message                │")
        print("├─────────────────────────────────────┤")
        
        lines = message.split('\n')
        for line in lines:
            print(f"│ {line[:35]:<35} │")
        
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        if wait_time > 0:
            time.sleep(wait_time)
        else:
            # Wait for keypress
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def create_new_habit(self):
        """Create a new habit with name input."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│           📝 Create Habit            │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter a name for your new habit:    │")
        print("│                                     │")
        print("│ Examples:                           │")
        print("│ • Read 30 Pages                     │")
        print("│ • Meditate                          │")
        print("│ • Exercise                          │")
        print("│ • Drink Water                       │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            habit_name = input("Habit name: ").strip()
            
            if not habit_name:
                self._show_message("❌ Habit name cannot be empty")
                self.view_mode = 'list'
                return
            
            if habit_name in self.habit_list:
                self._show_message(f"❌ Habit '{habit_name}' already exists")
                self.view_mode = 'list'
                return
            
            # Create habit directory
            vault_path = self.get_vault_path()
            if vault_path:
                habit_dir = Path(vault_path) / "Habits" / habit_name
                habit_dir.mkdir(parents=True, exist_ok=True)
                
                # Add to habit list
                self.habit_list.append(habit_name)
                self.habit_list.sort()
                
                # Set selection to new habit
                self.current_selection = self.habit_list.index(habit_name)
                
                self._show_message(f"✓ Created habit: {habit_name}")
            else:
                self._show_message("❌ No vault configured")
            
            self.view_mode = 'list'
            
        except (KeyboardInterrupt, EOFError):
            self.view_mode = 'list'

    def log_selected_habit(self):
        """Log the selected habit with detailed form."""
        if not self.selected_habit:
            self.view_mode = 'list'
            return
        
        # Check if already logged
        habit_file = self._get_habit_file_path(self.selected_habit, self.current_date)
        if habit_file and habit_file.exists():
            self._edit_existing_log()
        else:
            self._create_new_log()

    def _create_new_log(self):
        """Create a new habit log entry."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print(f"│ 📝 Log: {self.selected_habit[:25]:<25} │")
        print("├─────────────────────────────────────┤")
        print(f"│ Date: {self.current_date.strftime('%Y-%m-%d')}                │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Creating detailed log entry...      │")
        print("│                                     │")
        print("│ For now, creating simple completion │")
        print("│ Template support coming soon!       │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        # For now, create a simple log
        habit_file = self._get_habit_file_path(self.selected_habit, self.current_date)
        if habit_file:
            habit_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""# Habit: {self.selected_habit}
Date: {self.current_date.strftime('%Y-%m-%d')}
Time: {datetime.now().strftime('%H:%M')}

## Completion
- Completed: Yes

## Duration
- Time spent: [Enter duration]

## Quality/Rating
- Rating (1-10): [Enter rating]

## Notes
- [Add any notes about today's session]

## Reflection
- How did it feel?
- What went well?
- What could be improved?
"""
            
            try:
                with open(habit_file, 'w') as f:
                    f.write(content)
                self._show_message(f"✓ {self.selected_habit} logged!")
            except Exception as e:
                self._show_message(f"Error: {e}")
        
        self.view_mode = 'list'

    def _edit_existing_log(self):
        """Show that habit is already logged."""
        self._show_message(f"{self.selected_habit} already logged today!\nTemplate editing coming soon...", wait_time=0)
        self.view_mode = 'list'

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
        if not habit_name:
            return 0
        
        vault_path = self.get_vault_path()
        if not vault_path:
            return 0
        
        habit_dir = Path(vault_path) / "Habits" / habit_name
        if not habit_dir.exists():
            return 0
        
        # Start from today and count backward
        current_date = datetime.now().date()
        streak = 0
        
        # Check up to 365 days back (reasonable limit)
        for i in range(365):
            check_date = current_date - timedelta(days=i)
            habit_file = habit_dir / f"{habit_name}-{check_date.strftime('%Y-%m-%d')}.md"
            
            if habit_file.exists():
                streak += 1
            else:
                # Streak broken
                break
        
        return streak

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

    def _jump_to_date(self):
        """Allow user to jump to a specific date."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│            📅 Jump to Date           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter date (YYYY-MM-DD):            │")
        print("│ Or press Enter for today            │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            date_str = input("Date: ").strip()
            
            if not date_str:
                self.current_date = datetime.now().date()
            else:
                try:
                    self.current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    self._show_message("❌ Invalid date format\nUse YYYY-MM-DD")
                    return
            
            self.current_selection = 0  # Reset selection
            
        except (KeyboardInterrupt, EOFError):
            pass

    def _show_statistics(self):
        """Display habit statistics."""
        if not self.habit_list:
            self._show_message("No habits to show statistics for", wait_time=0)
            return
        
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│           📊 Habit Statistics        │")
        print("├─────────────────────────────────────┤")
        print("│ Habit                Current  Best  │")
        print("├─────────────────────────────────────┤")
        
        for habit in self.habit_list:
            current_streak = self.calculate_streak(habit)
            best_streak = self._calculate_best_streak(habit)
            habit_display = habit[:20] if len(habit) <= 20 else habit[:17] + "..."
            
            print(f"│ {habit_display:<20} {current_streak:>7} {best_streak:>5} │")
        
        print("├─────────────────────────────────────┤")
        print("│ Press any key to continue...        │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        # Wait for keypress
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _calculate_best_streak(self, habit_name):
        """Calculate the best (longest) streak for a habit."""
        vault_path = self.get_vault_path()
        if not vault_path:
            return 0
        
        habit_dir = Path(vault_path) / "Habits" / habit_name
        if not habit_dir.exists():
            return 0
        
        # Get all log files and sort by date
        log_files = []
        for file in habit_dir.glob(f"{habit_name}-*.md"):
            try:
                date_str = file.stem.split('-')[-3:]  # Get YYYY-MM-DD parts
                date_str = '-'.join(date_str)
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                log_files.append(log_date)
            except:
                continue
        
        if not log_files:
            return 0
        
        log_files.sort()
        
        # Find longest consecutive streak
        best_streak = 0
        current_streak = 1
        
        for i in range(1, len(log_files)):
            if log_files[i] == log_files[i-1] + timedelta(days=1):
                current_streak += 1
            else:
                best_streak = max(best_streak, current_streak)
                current_streak = 1
        
        best_streak = max(best_streak, current_streak)
        return best_streak

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