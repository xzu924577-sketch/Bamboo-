"""
Help module for Bamboo Productivity app.
Displays keybinds, usage instructions, and app overview.
"""

import os
import sys


class Help:
    """
    Help and documentation display for Bamboo Productivity.
    Shows keybinds, module descriptions, and usage instructions.
    """
    
    def __init__(self):
        """Initialize Help module."""
        self.running = True
        self.current_page = 0
        self.pages = [
            self.overview_page,
            self.keybinds_page,
            self.modules_page,
            self.vault_page
        ]

    def run(self):
        """Main Help module loop."""
        while self.running:
            self.display_current_page()
            self.handle_input()

    def display_current_page(self):
        """Display the current help page."""
        os.system('clear')
        print("\033[32m")  # Green tint
        
        if self.current_page < len(self.pages):
            self.pages[self.current_page]()
        
        print("\033[0m")

    def overview_page(self):
        """Display app overview and purpose."""
        print("╭─────────────────────────────────────╮")
        print("│        🎋 Bamboo Productivity        │")
        print("│             Overview                │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Bamboo Productivity is a terminal-  │")
        print("│ based app for managing habits,      │")
        print("│ tasks, and Pomodoro focus sessions. │")
        print("│                                     │")
        print("│ Key Features:                       │")
        print("│ • Keyboard-only interface           │")
        print("│ • Markdown file storage             │")
        print("│ • Habit streak tracking             │")
        print("│ • Unlimited Pomodoro cycles         │")
        print("│ • Task management with subtasks     │")
        print("│ • Template-based habit logging      │")
        print("│ • Vault system for data organization│")
        print("│                                     │")
        print("│ Supported Platforms:                │")
        print("│ • Linux terminals                   │")
        print("│ • Android Termux                    │")
        print("│                                     │")
        print("├─────────────────────────────────────┤")
        print("│ ←→: Pages  Esc: Back to dashboard    │")
        print("╰─────────────────────────────────────╯")

    def keybinds_page(self):
        """Display comprehensive keybinds."""
        print("╭─────────────────────────────────────╮")
        print("│         🎋 Keybinds Reference        │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Global Navigation:                  │")
        print("│ ↑ ↓     Move selection/cursor       │")
        print("│ ← →     Navigate pages/back         │")
        print("│ Enter   Select/Open/Start           │")
        print("│ Esc     Back/Cancel                 │")
        print("│ Ctrl+C  Exit application            │")
        print("│                                     │")
        print("│ Date Navigation:                    │")
        print("│ D       Jump to specific date       │")
        print("│ R       Go to today                 │")
        print("│ N       Previous day                │")
        print("│ M       Next day                    │")
        print("│                                     │")
        print("│ Editing:                            │")
        print("│ Space   Toggle completion           │")
        print("│ Ctrl+S  Save current changes        │")
        print("│ Ctrl+Enter  Add new task line       │")
        print("│ Tab     Indent/Create subtask       │")
        print("│ Shift+Tab   Unindent task           │")
        print("│                                     │")
        print("├─────────────────────────────────────┤")
        print("│ ←→: Pages  Esc: Back to dashboard    │")
        print("╰─────────────────────────────────────╯")

    def modules_page(self):
        """Display module descriptions and usage."""
        print("╭─────────────────────────────────────╮")
        print("│         🎋 Modules Overview          │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ 📝 Habits:                          │")
        print("│ • Daily habit tracking              │")
        print("│ • Streak calculation                │")
        print("│ • Template-based logging            │")
        print("│ • Multiple field types              │")
        print("│                                     │")
        print("│ 🍅 Pomodoro:                        │")
        print("│ • Focus timer sessions              │")
        print("│ • Unlimited cycles                  │")
        print("│ • Session statistics                │")
        print("│ • Markdown logging                  │")
        print("│                                     │")
        print("│ ✅ Tasks:                           │")
        print("│ • Daily task management             │")
        print("│ • Subtask support                   │")
        print("│ • Completion tracking               │")
        print("│ • Date-based organization           │")
        print("│                                     │")
        print("│ 📋 Templates:                       │")
        print("│ • Create habit templates            │")
        print("│ • Define custom fields              │")
        print("│ • External editing support          │")
        print("│                                     │")
        print("├─────────────────────────────────────┤")
        print("│ ←→: Pages  Esc: Back to dashboard    │")
        print("╰─────────────────────────────────────╯")

    def vault_page(self):
        """Display vault system information."""
        print("╭─────────────────────────────────────╮")
        print("│         🎋 Vault System              │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Vault Structure:                    │")
        print("│ VaultRoot/                          │")
        print("│ ├─ Pomodoro/                        │")
        print("│ │  └─ Session_Name_YYYY-MM-DD.md    │")
        print("│ ├─ Habits/                          │")
        print("│ │  └─ HabitName/                     │")
        print("│ │     └─ HabitName-YYYY-MM-DD.md    │")
        print("│ ├─ Tasks/                           │")
        print("│ │  └─ Task_YYYY-MM-DD.md            │")
        print("│ └─ Templates/                       │")
        print("│    └─ Habits/                       │")
        print("│       └─ TemplateName.template.md   │")
        print("│                                     │")
        print("│ Features:                           │")
        print("│ • Multiple vault support            │")
        print("│ • External file editing             │")
        print("│ • Automatic directory creation      │")
        print("│ • Configuration per vault           │")
        print("│ • Data portability                  │")
        print("│                                     │")
        print("├─────────────────────────────────────┤")
        print("│ ←→: Pages  Esc: Back to dashboard    │")
        print("╰─────────────────────────────────────╯")

    def handle_input(self):
        """Handle keyboard input for help navigation."""
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
                if key == '\x1b[D':  # Left arrow
                    self.current_page = max(0, self.current_page - 1)
                elif key == '\x1b[C':  # Right arrow
                    self.current_page = min(len(self.pages) - 1, self.current_page + 1)
                elif key == '\x1b':  # Esc alone
                    self.running = False
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_quick_help(self):
        """
        Get quick help text for embedding in other modules.
        
        Returns:
            str: Quick help text
        """
        return """
Quick Help:
↑↓: Navigate  Enter: Select  Esc: Back
D: Jump to date  R: Today  N: Prev  M: Next
Space: Toggle  Ctrl+S: Save  Tab: Indent
        """.strip()

    def get_module_help(self, module_name):
        """
        Get specific help for a module.
        
        Args:
            module_name (str): Name of the module
            
        Returns:
            str: Module-specific help text
        """
        help_texts = {
            'habits': """
Habits Module Help:
• Enter: Log habit for current date
• Space: Quick toggle completion
• D: Jump to specific date
• R: Return to today
• N: Previous day, M: Next day
• C: Create new habit
• T: Manage templates
            """.strip(),
            
            'pomodoro': """
Pomodoro Module Help:
• Enter: Start new session
• Space: Pause/Resume timer
• Esc: Stop current session
• S: View session statistics
• H: View session history
• Session logs saved automatically
            """.strip(),
            
            'tasks': """
Tasks Module Help:
• Enter: Edit tasks for current date
• Ctrl+Enter: Add new task
• Tab: Create subtask (indent)
• Shift+Tab: Unindent task
• Space: Toggle task completion
• D: Jump to date, R: Today
            """.strip(),
            
            'templates': """
Templates Module Help:
• Enter: Edit selected template
• C: Create new template
• D: Delete template
• A: Add field to template
• T: Change field type
• External editing supported
            """.strip()
        }
        
        return help_texts.get(module_name.lower(), "No specific help available for this module.")