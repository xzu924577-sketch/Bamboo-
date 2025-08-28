"""
Tasks module for Bamboo Productivity app.
Handles task management with subtasks, completion tracking, and markdown storage.
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path


class Tasks:
    """
    Task management with subtask support and markdown storage.
    Supports creating, editing, and organizing tasks with completion tracking.
    """
    
    def __init__(self):
        """Initialize Tasks module."""
        # Load settings and vault path
        from .settings import Settings
        self.settings = Settings()
        
        self.current_date = datetime.now().date()
        self.tasks = []
        self.current_selection = 0
        self.running = True
        self.edit_mode = False
        self.cursor_pos = 0  # For text editing
        
        # Task structure: {'text': str, 'completed': bool, 'indent_level': int}
        self.tasks = []

    def run(self):
        """Main Tasks module loop."""
        self.load_tasks()
        while self.running:
            if self.edit_mode:
                self.display_edit_view()
                self.handle_edit_input()
            else:
                self.display_view_mode()
                self.handle_view_input()

    def display_menu(self):
        """Display tasks main menu (alias for display_view_mode)."""
        self.display_view_mode()

    def display_view_mode(self):
        """Display tasks in view mode."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           ✅ Task Manager            │")
        print("├─────────────────────────────────────┤")
        print(f"│ Date: {self.current_date.strftime('%Y-%m-%d')} ({self._get_day_name()})     │")
        print("├─────────────────────────────────────┤")
        
        if not self.tasks:
            print("│                                     │")
            print("│  No tasks for this date.            │")
            print("│  Press E to start editing.          │")
            print("│                                     │")
        else:
            # Show task count
            completed_count = sum(1 for task in self.tasks if task.get('completed', False))
            total_count = len(self.tasks)
            print(f"│ Tasks: {completed_count}/{total_count} completed              │")
            print("├─────────────────────────────────────┤")
            
            # Display tasks (show up to 8 tasks to fit in terminal)
            display_tasks = self.tasks[:8] if len(self.tasks) > 8 else self.tasks
            for i, task in enumerate(display_tasks):
                prefix = "► " if i == self.current_selection else "  "
                status = "✓" if task.get('completed', False) else "○"
                indent = "  " * task.get('indent_level', 0)
                task_text = task.get('text', '')
                
                # Adjust text length based on indentation
                max_text_len = 30 - len(indent)
                if len(task_text) > max_text_len:
                    task_text = task_text[:max_text_len-3] + "..."
                
                print(f"│{prefix}{status} {indent}{task_text:<{30-len(indent)}} │")
            
            if len(self.tasks) > 8:
                print(f"│  ... and {len(self.tasks) - 8} more tasks          │")
        
        print("├─────────────────────────────────────┤")
        print("│ E: Edit  Space: Toggle  D: Jump date│")
        print("│ R: Today  N: Prev day  M: Next day  │")
        print("│ Esc: Back to dashboard              │")
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

    def display_edit_view(self):
        """Display tasks in edit mode."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│         ✏️  Task Editor              │")
        print("├─────────────────────────────────────┤")
        print(f"│ Date: {self.current_date.strftime('%Y-%m-%d')} ({self._get_day_name()})     │")
        print("├─────────────────────────────────────┤")
        
        if not self.tasks:
            print("│                                     │")
            print("│  No tasks yet.                     │")
            print("│  Press Ctrl+Enter to add first task│")
            print("│                                     │")
        else:
            # Display tasks in markdown format
            for i, task in enumerate(self.tasks):
                prefix = "► " if i == self.current_selection else "  "
                status = "[x]" if task.get('completed', False) else "[ ]"
                indent = "    " * task.get('indent_level', 0)  # 4 spaces per indent level
                task_text = task.get('text', '')
                
                # Truncate long task text to fit display
                max_text_len = 25 - len(indent)
                if len(task_text) > max_text_len:
                    task_text = task_text[:max_text_len-3] + "..."
                
                print(f"│{prefix}- {status} {indent}{task_text:<{25-len(indent)}} │")
        
        print("├─────────────────────────────────────┤")
        print("│ Ctrl+Enter: New task  Space: Toggle │")
        print("│ Tab: Indent  Shift+Tab: Unindent    │")
        print("│ Enter: Edit text  Del: Delete       │")
        print("│ Ctrl+S: Save  Esc: View mode        │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def handle_view_input(self):
        """Handle keyboard input in view mode."""
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
                        if self.tasks:
                            self.current_selection = (self.current_selection - 1) % len(self.tasks)
                    elif key == '\x1b[B':  # Down arrow
                        if self.tasks:
                            self.current_selection = (self.current_selection + 1) % len(self.tasks)
                except:
                    # Single Esc - go back
                    self.running = False
            elif key == ' ':  # Space - toggle task completion
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self.toggle_task_completion(self.current_selection)
                    self.save_tasks()
            elif key.lower() == 'e':  # Enter edit mode
                self.edit_mode = True
            elif key.lower() == 'd':  # Jump to date
                self._jump_to_date()
            elif key.lower() == 'r':  # Return to today
                self.current_date = datetime.now().date()
                self.current_selection = 0
                self.load_tasks()
            elif key.lower() == 'n':  # Previous day
                self.current_date -= timedelta(days=1)
                self.current_selection = 0
                self.load_tasks()
            elif key.lower() == 'm':  # Next day
                self.current_date += timedelta(days=1)
                self.current_selection = 0
                self.load_tasks()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def handle_edit_input(self):
        """Handle keyboard input in edit mode."""
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
                        if self.tasks:
                            self.current_selection = (self.current_selection - 1) % len(self.tasks)
                    elif key == '\x1b[B':  # Down arrow
                        if self.tasks:
                            self.current_selection = (self.current_selection + 1) % len(self.tasks)
                except:
                    # Single Esc - go back to view mode
                    self.edit_mode = False
            elif key == ' ':  # Space - toggle completion
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self.toggle_task_completion(self.current_selection)
            elif key == '\t':  # Tab - indent task
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self.indent_task(self.current_selection)
            elif key == '\x1b[Z':  # Shift+Tab - unindent task
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self.unindent_task(self.current_selection)
            elif key == '\r' or key == '\n':  # Enter - edit task text
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self._edit_task_text()
            elif key == '\x7f':  # Backspace/Delete - delete task
                if self.tasks and 0 <= self.current_selection < len(self.tasks):
                    self.delete_task(self.current_selection)
            elif key == '\x03':  # Ctrl+C
                self.running = False
            elif ord(key) == 10:  # Ctrl+Enter - add new task
                self._add_new_task()
            elif ord(key) == 19:  # Ctrl+S - save
                self.save_tasks()
                self._show_message("✓ Tasks saved!")
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _show_message(self, message, wait_time=1.0):
        """Show a temporary message to user."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│              Message                │")
        print("├─────────────────────────────────────┤")
        print(f"│ {message[:35]:<35} │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        if wait_time > 0:
            time.sleep(wait_time)

    def load_tasks(self):
        """Load tasks from markdown file for current date."""
        vault_path = self.get_vault_path()
        if not vault_path:
            self.tasks = []
            return
        
        tasks_dir = Path(vault_path) / "Tasks"
        tasks_dir.mkdir(exist_ok=True)
        
        filename = self.create_task_filename(self.current_date)
        filepath = tasks_dir / filename
        
        if not filepath.exists():
            self.tasks = []
            return
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            self.tasks = self.parse_markdown_tasks(content)
            
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

    def get_vault_path(self):
        """Get the current vault path from settings."""
        vault_path = self.settings.get_vault_path()
        
        # If no vault path found, try to load config
        if not vault_path:
            config = self.settings.load_config()
            vault_path = config.get('vault_path')
        
        return vault_path

    def save_tasks(self):
        """Save tasks to markdown file."""
        vault_path = self.get_vault_path()
        if not vault_path:
            return
        
        tasks_dir = Path(vault_path) / "Tasks"
        tasks_dir.mkdir(exist_ok=True)
        
        filename = self.create_task_filename(self.current_date)
        filepath = tasks_dir / filename
        
        content = self.format_tasks_to_markdown()
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def _add_new_task(self):
        """Add a new task with user input."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│            ➕ Add Task               │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter task description:             │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            task_text = input("Task: ").strip()
            
            if task_text:
                new_task = {
                    'text': task_text,
                    'completed': False,
                    'indent_level': 0
                }
                self.tasks.append(new_task)
                self.current_selection = len(self.tasks) - 1
                self._show_message(f"✓ Added task: {task_text[:20]}...")
            
        except (KeyboardInterrupt, EOFError):
            pass

    def _edit_task_text(self):
        """Edit the text of the selected task."""
        if not self.tasks or not (0 <= self.current_selection < len(self.tasks)):
            return
        
        current_task = self.tasks[self.current_selection]
        
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│            ✏️ Edit Task              │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print(f"│ Current: {current_task['text'][:25]:<25} │")
        print("│                                     │")
        print("│ Enter new text:                     │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            new_text = input("Task: ").strip()
            
            if new_text:
                current_task['text'] = new_text
                self._show_message(f"✓ Updated task")
            
        except (KeyboardInterrupt, EOFError):
            pass

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
            
            self.current_selection = 0
            self.load_tasks()
            
        except (KeyboardInterrupt, EOFError):
            pass

    def create_task(self):
        """Create a new task."""
        # Placeholder for task creation
        pass

    def edit_task_text(self, task_index):
        """
        Edit text of selected task.
        
        Args:
            task_index (int): Index of task to edit
        """
        # Placeholder for task text editing
        pass

    def toggle_task_completion(self, task_index):
        """
        Toggle completion status of a task.
        
        Args:
            task_index (int): Index of task to toggle
        """
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = not self.tasks[task_index].get('completed', False)

    def indent_task(self, task_index):
        """
        Increase indentation level of a task (make it a subtask).
        
        Args:
            task_index (int): Index of task to indent
        """
        if 0 <= task_index < len(self.tasks):
            current_level = self.tasks[task_index].get('indent_level', 0)
            self.tasks[task_index]['indent_level'] = min(current_level + 1, 3)

    def unindent_task(self, task_index):
        """
        Decrease indentation level of a task.
        
        Args:
            task_index (int): Index of task to unindent
        """
        if 0 <= task_index < len(self.tasks):
            current_level = self.tasks[task_index].get('indent_level', 0)
            self.tasks[task_index]['indent_level'] = max(current_level - 1, 0)

    def delete_task(self, task_index):
        """
        Delete a task.
        
        Args:
            task_index (int): Index of task to delete
        """
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]
            if self.current_selection >= len(self.tasks) and self.tasks:
                self.current_selection = len(self.tasks) - 1

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

    def create_task_filename(self, date):
        """
        Create filename for task file.
        
        Args:
            date (datetime.date): Date for the tasks
            
        Returns:
            str: Formatted filename
        """
        return f"Task_{date.strftime('%Y-%m-%d')}.md"

    def parse_markdown_tasks(self, content):
        """
        Parse markdown content into task objects.
        
        Args:
            content (str): Markdown file content
            
        Returns:
            list: List of task dictionaries
        """
        tasks = []
        lines = content.split('\n')
        
        for line in lines:
            # Skip empty lines and headers
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            # Look for task lines (- [ ] or - [x])
            if '- [' in line and ']' in line:
                # Calculate indent level (count leading spaces before -)
                indent_level = 0
                for char in line:
                    if char == ' ':
                        indent_level += 1
                    elif char == '-':
                        break
                
                # Convert to indent levels (4 spaces = 1 level)
                indent_level = indent_level // 4
                
                # Extract completion status
                completed = '[x]' in line.lower() or '[X]' in line
                
                # Extract task text (everything after the checkbox)
                checkbox_end = line.find(']') + 1
                task_text = line[checkbox_end:].strip()
                
                if task_text:
                    tasks.append({
                        'text': task_text,
                        'completed': completed,
                        'indent_level': indent_level
                    })
        
        return tasks

    def format_tasks_to_markdown(self):
        """
        Format tasks list into markdown content.
        
        Returns:
            str: Markdown formatted task list
        """
        if not self.tasks:
            return f"# Tasks - {self.current_date.strftime('%Y-%m-%d')}\n\n(No tasks for this date)\n"
        
        content = f"# Tasks - {self.current_date.strftime('%Y-%m-%d')}\n\n"
        
        for task in self.tasks:
            # Create indentation (4 spaces per level)
            indent = "    " * task.get('indent_level', 0)
            
            # Create checkbox
            checkbox = "[x]" if task.get('completed', False) else "[ ]"
            
            # Create task line
            task_line = f"{indent}- {checkbox} {task.get('text', '')}\n"
            content += task_line
        
        return content