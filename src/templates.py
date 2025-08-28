"""
Templates module for Bamboo Productivity app.
Handles creation and management of habit templates.
"""

import os
import sys
import json
import time
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
            print("│                                     │")
            print("│  No templates found.                │")
            print("│  Press C to create your first!      │")
            print("│                                     │")
        else:
            print(f"│ Found {len(self.templates)} template(s):                  │")
            print("├─────────────────────────────────────┤")
            
            for i, template in enumerate(self.templates):
                prefix = "► " if i == self.current_selection else "  "
                name = template.get('name', 'Unnamed')[:20]
                field_count = len(template.get('fields', []))
                print(f"│{prefix}{name:<22} [{field_count:>2} fields] │")
        
        print("├─────────────────────────────────────┤")
        print("│ Enter: View template                │")
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
            
            if key == '\x1b':  # Escape sequence or single escape
                try:
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':  # Up arrow
                        if self.templates:
                            self.current_selection = (self.current_selection - 1) % len(self.templates)
                    elif key == '\x1b[B':  # Down arrow
                        if self.templates:
                            self.current_selection = (self.current_selection + 1) % len(self.templates)
                except:
                    # Single Esc - go back
                    self.running = False
            elif key == '\r' or key == '\n':  # Enter - edit template
                if self.templates:
                    self._show_template_info()
            elif key.lower() == 'c':  # Create template
                self.create_template()
                self.load_templates()  # Reload
            elif key.lower() == 'd':  # Delete template
                if self.templates:
                    self._delete_template()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _show_template_info(self):
        """Show detailed information about selected template."""
        if not self.templates or self.current_selection >= len(self.templates):
            return
        
        template = self.templates[self.current_selection]
        
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print(f"│ 📋 Template: {template['name'][:20]:<20} │")
        print("├─────────────────────────────────────┤")
        print(f"│ File: {template['filename'][:28]:<28} │")
        print(f"│ Fields: {len(template.get('fields', []))}                          │")
        print("├─────────────────────────────────────┤")
        
        for field in template.get('fields', [])[:6]:  # Show first 6 fields
            field_name = field['name'][:20]
            field_type = field['type']
            print(f"│ • {field_name:<20} [{field_type:<8}] │")
        
        if len(template.get('fields', [])) > 6:
            print(f"│ ... and {len(template['fields']) - 6} more fields            │")
        
        print("├─────────────────────────────────────┤")
        print("│ This template can be edited         │")
        print("│ externally in any text editor.      │")
        print("│                                     │")
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

    def _delete_template(self):
        """Delete selected template with confirmation."""
        if not self.templates or self.current_selection >= len(self.templates):
            return
        
        template = self.templates[self.current_selection]
        
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│            ⚠️ Delete Template        │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print(f"│ Delete '{template['name'][:22]}'?             │")
        print("│                                     │")
        print("│ This cannot be undone!              │")
        print("│                                     │")
        print("│ Y - Yes, delete    N - Cancel       │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1).lower()
            
            if key == 'y':
                # Delete file
                vault_path = self.get_vault_path()
                if vault_path:
                    templates_dir = Path(vault_path) / "Templates" / "Habits"
                    filepath = templates_dir / template['filename']
                    
                    try:
                        filepath.unlink()
                        self.templates.pop(self.current_selection)
                        if self.current_selection >= len(self.templates) and self.templates:
                            self.current_selection = len(self.templates) - 1
                        self._show_message(f"✓ Deleted {template['name']}")
                    except Exception as e:
                        self._show_message(f"❌ Error deleting: {e}")
                else:
                    self._show_message("❌ No vault configured")
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
        vault_path = self.get_vault_path()
        if not vault_path:
            self.templates = []
            return
        
        templates_dir = Path(vault_path) / "Templates" / "Habits"
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True, exist_ok=True)
            self.templates = []
            return
        
        self.templates = []
        for template_file in templates_dir.glob("*.template.md"):
            try:
                template_data = self._load_template_file(template_file)
                if template_data:
                    self.templates.append(template_data)
            except Exception as e:
                print(f"Error loading template {template_file.name}: {e}")
        
        self.templates.sort(key=lambda x: x.get('name', ''))

    def get_vault_path(self):
        """Get the current vault path from settings."""
        from .settings import Settings
        settings = Settings()
        vault_path = settings.get_vault_path()
        
        if not vault_path:
            config = settings.load_config()
            vault_path = config.get('vault_path')
        
        return vault_path

    def _load_template_file(self, filepath):
        """Load a single template file."""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Parse template metadata from markdown
            lines = content.split('\n')
            template_name = filepath.stem.replace('.template', '')
            
            template_data = {
                'name': template_name,
                'filename': filepath.name,
                'fields': self._parse_template_fields(content)
            }
            
            return template_data
        except Exception:
            return None

    def _parse_template_fields(self, content):
        """Parse field definitions from template content."""
        fields = []
        lines = content.split('\n')
        
        current_field = None
        for line in lines:
            line = line.strip()
            if line.startswith('## ') and not line.startswith('## Notes'):
                # New field
                field_name = line[3:].strip()
                field_type = 'text'  # default
                
                # Detect field type from name
                if '[time]' in field_name.lower() or 'duration' in field_name.lower():
                    field_type = 'time'
                elif '[pages]' in field_name.lower() or 'page' in field_name.lower():
                    field_type = 'pages'
                elif '[mood]' in field_name.lower() or 'rating' in field_name.lower():
                    field_type = 'mood'
                elif '[mcq]' in field_name.lower() or 'choice' in field_name.lower():
                    field_type = 'mcq'
                
                current_field = {
                    'name': field_name.replace('[time]', '').replace('[pages]', '').replace('[mood]', '').replace('[mcq]', '').strip(),
                    'type': field_type,
                    'required': True
                }
                fields.append(current_field)
        
        return fields

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
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│        📝 Create Template            │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter template name:                │")
        print("│ (e.g., Reading, Exercise, Meditate) │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            template_name = input("Template name: ").strip()
            
            if not template_name:
                self._show_message("❌ Template name cannot be empty")
                return
            
            # Check if template exists
            if any(t['name'].lower() == template_name.lower() for t in self.templates):
                self._show_message(f"❌ Template '{template_name}' already exists")
                return
            
            # Create default template
            template_data = self.create_default_template(template_name)
            
            # Save template
            if self._save_template_to_file(template_data):
                self.templates.append(template_data)
                self.templates.sort(key=lambda x: x.get('name', ''))
                self._show_message(f"✓ Created template: {template_name}")
            else:
                self._show_message("❌ Failed to create template")
            
        except (KeyboardInterrupt, EOFError):
            pass

    def _save_template_to_file(self, template_data):
        """Save template data to markdown file."""
        vault_path = self.get_vault_path()
        if not vault_path:
            return False
        
        templates_dir = Path(vault_path) / "Templates" / "Habits"
        templates_dir.mkdir(parents=True, exist_ok=True)
        
        filename = self.template_filename(template_data['name'])
        filepath = templates_dir / filename
        
        content = self._generate_template_content(template_data)
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

    def _generate_template_content(self, template_data):
        """Generate markdown content for template."""
        content = f"""# Template: {template_data['name']}

This template defines the structure for {template_data['name']} habit logs.

"""
        
        for field in template_data.get('fields', []):
            field_name = field['name']
            field_type = field['type']
            
            if field_type == 'time':
                field_name += " [time]"
            elif field_type == 'pages':
                field_name += " [pages]"
            elif field_type == 'mood':
                field_name += " [mood 1-10]"
            elif field_type == 'mcq':
                field_name += " [mcq]"
            
            content += f"## {field_name}\n"
            
            if field_type == 'mcq':
                content += "- [ ] Option 1\n- [ ] Option 2\n- [ ] Option 3\n"
            else:
                content += "- [Enter value here]\n"
            
            content += "\n"
        
        content += "## Notes\n- [Additional notes and reflections]\n"
        
        return content

    def _show_message(self, message, wait_time=1.5):
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