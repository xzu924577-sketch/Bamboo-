"""
Templates module for Bamboo Productivity app.
Handles creation and management of habit templates.
"""

import os
import sys
import json
from pathlib import Path


class Templates:
    """
    Template management for habits.
    Allows creating, editing, and deleting habit templates.
    """
    
    def __init__(self):
        """Initialize Templates module."""
        self.templates = []
        self.current_selection = 0
        self.running = True
        self.edit_mode = False

    def run(self):
        """Main Templates module loop."""
        self.load_templates()
        while self.running:
            if self.edit_mode:
                self.display_edit_view()
                self.handle_edit_input()
            else:
                self.display_menu()
                self.handle_menu_input()

    def display_menu(self):
        """Display templates main menu."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           📋 Template Manager        │")
        print("├─────────────────────────────────────┤")
        
        if not self.templates:
            print("│  No templates found.                │")
            print("│  Create your first template!        │")
        else:
            for i, template in enumerate(self.templates):
                prefix = "► " if i == self.current_selection else "  "
                name = template.get('name', 'Unnamed')[:20]
                field_count = len(template.get('fields', []))
                print(f"│ {prefix}{name:<20} [{field_count} fields] │")
        
        print("├─────────────────────────────────────┤")
        print("│ Enter: Edit template                │")
        print("│ C: Create template                  │")
        print("│ D: Delete template                  │")
        print("│ Esc: Back to dashboard              │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def display_edit_view(self):
        """Display template editor."""
        # Placeholder for template editor display
        pass

    def handle_menu_input(self):
        """Handle keyboard input for templates menu."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape
                self.running = False
            elif key == '\x03':  # Ctrl+C
                self.running = False
            # Add other keys later
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def handle_edit_input(self):
        """Handle keyboard input in template editor."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape - go back to menu
                self.edit_mode = False
            elif key == '\x03':  # Ctrl+C
                self.running = False
            # Add other keys later
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def load_templates(self):
        """Load templates from templates directory."""
        # Placeholder for loading templates
        pass

    def save_template(self, template_data):
        """
        Save template to file.
        
        Args:
            template_data (dict): Template configuration
        """
        # Placeholder for saving template
        pass

    def create_template(self):
        """Create a new habit template."""
        # Placeholder for template creation
        pass

    def edit_template(self, template_index):
        """
        Edit selected template.
        
        Args:
            template_index (int): Index of template to edit
        """
        # Placeholder for template editing
        pass

    def delete_template(self, template_index):
        """
        Delete selected template.
        
        Args:
            template_index (int): Index of template to delete
        """
        # Placeholder for template deletion
        pass

    def add_field(self, template_index):
        """
        Add a new field to template.
        
        Args:
            template_index (int): Index of template to modify
        """
        # Placeholder for adding field
        pass

    def edit_field(self, template_index, field_index):
        """
        Edit a field in template.
        
        Args:
            template_index (int): Index of template
            field_index (int): Index of field to edit
        """
        # Placeholder for field editing
        pass

    def delete_field(self, template_index, field_index):
        """
        Delete a field from template.
        
        Args:
            template_index (int): Index of template
            field_index (int): Index of field to delete
        """
        # Placeholder for field deletion
        pass

    def get_field_types(self):
        """
        Get available field types for templates.
        
        Returns:
            list: Available field types
        """
        return [
            {'name': 'Time', 'type': 'time', 'description': 'Time duration with unit'},
            {'name': 'Pages', 'type': 'pages', 'description': 'Page count with unit'},
            {'name': 'Mood', 'type': 'mood', 'description': 'Mood scale 1-10'},
            {'name': 'Notes', 'type': 'notes', 'description': 'Free text notes'},
            {'name': 'MCQ', 'type': 'mcq', 'description': 'Multiple choice question'}
        ]

    def create_default_template(self, name):
        """
        Create a default template structure.
        
        Args:
            name (str): Name of the template
            
        Returns:
            dict: Default template structure
        """
        return {
            'name': name,
            'description': f'Template for {name} habit',
            'fields': [
                {
                    'name': 'Duration',
                    'type': 'time',
                    'unit': 'minutes',
                    'required': True
                },
                {
                    'name': 'Notes',
                    'type': 'notes',
                    'required': False
                }
            ]
        }

    def get_vault_path(self):
        """Get the current vault path from settings."""
        # Placeholder for vault path retrieval
        pass

    def get_templates_path(self):
        """Get the templates directory path."""
        vault_path = self.get_vault_path()
        return Path(vault_path) / "Templates" / "Habits" if vault_path else None

    def template_filename(self, template_name):
        """
        Create filename for template.
        
        Args:
            template_name (str): Name of the template
            
        Returns:
            str: Template filename
        """
        return f"{template_name}.template.md"