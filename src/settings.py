"""
Settings module for Bamboo Productivity app.
Handles vault creation, switching, configuration management, and first-time setup.
"""

import os
import sys
import json
from pathlib import Path


class Settings:
    """
    Settings and vault management for Bamboo Productivity.
    Handles first-time setup, vault switching, and configuration persistence.
    """
    
    def __init__(self):
        """Initialize Settings module."""
        self.config_filename = ".bamboo_config.json"
        self.default_config = {
            "vault_name": "BambooVault",
            "vault_path": None,
            "pomodoro_focus": 25,
            "pomodoro_break": 5,
            "long_break": 15,
            "cycles_before_long_break": 4
        }
        self.current_config = None
        self.running = True
        self.current_selection = 0

    def run(self):
        """Main Settings module loop."""
        while self.running:
            self.display_menu()
            self.handle_input()

    def display_menu(self):
        """Display settings main menu."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│              ⚙️ Settings              │")
        print("├─────────────────────────────────────┤")
        
        config = self.load_config()
        vault_name = config.get('vault_name', 'No vault')
        vault_path = config.get('vault_path', 'Not set')
        
        print(f"│ Current Vault: {vault_name[:20]:<20}     │")
        print(f"│ Path: {vault_path[:30]:<30}   │")
        print("├─────────────────────────────────────┤")
        
        menu_items = [
            "Create New Vault",
            "Switch Vault",
            "Change Vault Location", 
            "Set Pomodoro Focus Time",
            "Set Pomodoro Break Time",
            "Reset to Defaults"
        ]
        
        for i, item in enumerate(menu_items):
            prefix = "► " if i == self.current_selection else "  "
            print(f"│ {prefix}{item:<32} │")
        
        print("├─────────────────────────────────────┤")
        print("│ ↑↓: Navigate  Enter: Select  Esc: Back │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def handle_input(self):
        """Handle keyboard input for settings navigation."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape sequence
                key += sys.stdin.read(2)
                if key == '\x1b[A':  # Up arrow
                    self.current_selection = (self.current_selection - 1) % 6
                elif key == '\x1b[B':  # Down arrow
                    self.current_selection = (self.current_selection + 1) % 6
                elif key == '\x1b':  # Esc alone
                    self.running = False
            elif key == '\r' or key == '\n':  # Enter
                self._handle_menu_selection()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _handle_menu_selection(self):
        """Handle menu selection based on current_selection."""
        if self.current_selection == 0:  # Create New Vault
            self._create_new_vault_dialog()
        elif self.current_selection == 1:  # Switch Vault
            self._switch_vault_dialog()
        elif self.current_selection == 2:  # Change Vault Location
            self._change_vault_location_dialog()
        elif self.current_selection == 3:  # Set Pomodoro Focus Time
            self._set_focus_time_dialog()
        elif self.current_selection == 4:  # Set Pomodoro Break Time
            self._set_break_time_dialog()
        elif self.current_selection == 5:  # Reset to Defaults
            self._reset_defaults_dialog()

    def _create_new_vault_dialog(self):
        """Dialog for creating a new vault."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│           Create New Vault          │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ This will create a new vault and    │")
        print("│ switch to it immediately.           │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        vault_name = self._get_user_input("Enter vault name", "NewVault")
        if not vault_name:
            return
        
        default_path = str(Path.home() / vault_name)
        vault_path = self._get_user_input("Enter vault path", default_path)
        if not vault_path:
            return
        
        if self.create_vault(vault_name, vault_path):
            print(f"\n✅ Created vault '{vault_name}' at {vault_path}")
        else:
            print(f"\n❌ Failed to create vault")
        
        print("Press any key to continue...")
        self._get_single_key()

    def _switch_vault_dialog(self):
        """Dialog for switching to existing vault."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│             Switch Vault            │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter path to existing vault or     │")
        print("│ path where new vault should be      │")
        print("│ created.                            │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        current_path = self.get_vault_path() or str(Path.home())
        vault_path = self._get_user_input("Enter vault path", current_path)
        if not vault_path:
            return
        
        if self.switch_vault(vault_path):
            print(f"\n✅ Switched to vault at {vault_path}")
        else:
            print(f"\n❌ Failed to switch vault")
        
        print("Press any key to continue...")
        self._get_single_key()

    def _change_vault_location_dialog(self):
        """Dialog for changing current vault location."""
        # This moves the current vault to a new location
        self._switch_vault_dialog()  # Same functionality

    def _set_focus_time_dialog(self):
        """Dialog for setting Pomodoro focus time."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│        Set Focus Time               │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter focus time in minutes         │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        current_time = self.get_pomodoro_settings()['focus_time']
        time_str = self._get_user_input("Focus time (minutes)", str(current_time))
        
        try:
            minutes = int(time_str)
            if 1 <= minutes <= 120:  # Reasonable range
                self.set_pomodoro_focus_time(minutes)
                print(f"\n✅ Set focus time to {minutes} minutes")
            else:
                print(f"\n❌ Invalid time. Please enter 1-120 minutes")
        except ValueError:
            print(f"\n❌ Invalid input. Please enter a number")
        
        print("Press any key to continue...")
        self._get_single_key()

    def _set_break_time_dialog(self):
        """Dialog for setting Pomodoro break time."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│         Set Break Time              │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter break time in minutes         │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        current_time = self.get_pomodoro_settings()['break_time']
        time_str = self._get_user_input("Break time (minutes)", str(current_time))
        
        try:
            minutes = int(time_str)
            if 1 <= minutes <= 60:  # Reasonable range
                self.set_pomodoro_break_time(minutes)
                print(f"\n✅ Set break time to {minutes} minutes")
            else:
                print(f"\n❌ Invalid time. Please enter 1-60 minutes")
        except ValueError:
            print(f"\n❌ Invalid input. Please enter a number")
        
        print("Press any key to continue...")
        self._get_single_key()

    def _reset_defaults_dialog(self):
        """Dialog for resetting to default settings."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│         Reset to Defaults           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ This will reset Pomodoro times to   │")
        print("│ defaults. Vault path will remain    │")
        print("│ unchanged.                          │")
        print("│                                     │")
        print("│ Continue? (y/N)                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        key = self._get_single_key()
        if key.lower() == 'y':
            self.reset_to_defaults()
            print("\n✅ Reset to default settings")
        else:
            print("\n❌ Cancelled")
        
        print("Press any key to continue...")
        self._get_single_key()

    def is_first_time_setup(self):
        """
        Check if this is the first time the app is being run.
        
        Returns:
            bool: True if no vault configuration exists
        """
        # Check for config file in common locations
        possible_configs = [
            Path.home() / self.config_filename,
            Path.cwd() / self.config_filename
        ]
        
        for config_path in possible_configs:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        if config.get('vault_path') and Path(config['vault_path']).exists():
                            return False
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return True

    def first_time_setup(self):
        """Guide user through first-time vault setup."""
        import termios
        import tty
        
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│        🎋 Bamboo Productivity        │")
        print("│          First Time Setup           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Welcome! Let's set up your vault.   │")
        print("│                                     │")
        print("│ Your vault will store all your      │")
        print("│ habits, tasks, and Pomodoro data.   │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        # Get vault name
        vault_name = self._get_user_input("Enter vault name", "BambooVault")
        if not vault_name:
            return False
        
        # Get vault path
        default_path = str(Path.home() / vault_name)
        vault_path = self._get_user_input("Enter vault path", default_path)
        if not vault_path:
            return False
        
        # Validate path
        is_valid, error = self.validate_vault_path(vault_path)
        if not is_valid:
            print(f"\nError: {error}")
            print("Press any key to continue...")
            self._get_single_key()
            return False
        
        # Create vault
        if self.create_vault(vault_name, vault_path):
            os.system('clear')
            print("\033[32m")
            print("╭─────────────────────────────────────╮")
            print("│          ✅ Setup Complete!          │")
            print("├─────────────────────────────────────┤")
            print(f"│ Vault: {vault_name:<26} │")
            print(f"│ Path:  {vault_path[:26]:<26} │")
            print("│                                     │")
            print("│ Press any key to continue...        │")
            print("╰─────────────────────────────────────╯")
            print("\033[0m")
            self._get_single_key()
            return True
        else:
            print("\nFailed to create vault. Press any key to continue...")
            self._get_single_key()
            return False

    def create_vault(self, vault_name=None, vault_path=None):
        """
        Create a new vault with directory structure.
        
        Args:
            vault_name (str): Name of the vault
            vault_path (str): Path where vault should be created
            
        Returns:
            bool: True if vault created successfully
        """
        if not vault_name:
            vault_name = self.default_config['vault_name']
        
        if not vault_path:
            vault_path = str(Path.home() / vault_name)
        
        try:
            vault_dir = Path(vault_path)
            vault_dir.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = ['Pomodoro', 'Habits', 'Tasks', 'Templates']
            for subdir in subdirs:
                (vault_dir / subdir).mkdir(exist_ok=True)
            
            # Create Templates/Habits subdirectory
            (vault_dir / 'Templates' / 'Habits').mkdir(parents=True, exist_ok=True)
            
            # Create config file in vault
            config = self.default_config.copy()
            config['vault_name'] = vault_name
            config['vault_path'] = str(vault_dir)
            
            self.save_config(config, vault_dir)
            self.current_config = config
            
            return True
            
        except (PermissionError, OSError) as e:
            print(f"Error creating vault: {e}")
            return False

    def switch_vault(self, new_vault_path):
        """
        Switch to an existing vault or create new one.
        
        Args:
            new_vault_path (str): Path to the vault to switch to
            
        Returns:
            bool: True if switch successful
        """
        vault_dir = Path(new_vault_path)
        
        if not vault_dir.exists():
            # Create new vault at this path
            vault_name = vault_dir.name
            return self.create_vault(vault_name, str(vault_dir))
        
        # Load existing vault
        config_path = vault_dir / self.config_filename
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.current_config = config
                    return True
            except (json.JSONDecodeError, IOError):
                pass
        
        # Create config for existing vault without config
        vault_name = vault_dir.name
        config = self.default_config.copy()
        config['vault_name'] = vault_name
        config['vault_path'] = str(vault_dir)
        
        self.save_config(config, vault_dir)
        self.current_config = config
        return True

    def load_config(self):
        """
        Load configuration from current vault.
        
        Returns:
            dict: Configuration dictionary
        """
        if self.current_config:
            return self.current_config
        
        # Try to find config file
        possible_configs = [
            Path.home() / self.config_filename,
            Path.cwd() / self.config_filename
        ]
        
        for config_path in possible_configs:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        self.current_config = config
                        return config
                except (json.JSONDecodeError, IOError):
                    continue
        
        return self.default_config.copy()

    def save_config(self, config=None, vault_dir=None):
        """
        Save configuration to vault directory.
        
        Args:
            config (dict): Configuration to save (uses current if None)
            vault_dir (Path): Vault directory (uses current if None)
        """
        if config is None:
            config = self.current_config or self.default_config
        
        if vault_dir is None:
            vault_path = config.get('vault_path')
            if vault_path:
                vault_dir = Path(vault_path)
            else:
                vault_dir = Path.home()
        
        config_path = Path(vault_dir) / self.config_filename
        
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            self.current_config = config
        except (IOError, PermissionError) as e:
            print(f"Error saving config: {e}")

    def get_vault_path(self):
        """
        Get current vault path.
        
        Returns:
            str: Current vault path or None if not set
        """
        config = self.load_config()
        return config.get('vault_path')

    def set_pomodoro_focus_time(self, minutes):
        """
        Set default Pomodoro focus time.
        
        Args:
            minutes (int): Focus time in minutes
        """
        config = self.load_config()
        config['pomodoro_focus'] = minutes
        self.save_config(config)

    def set_pomodoro_break_time(self, minutes):
        """
        Set default Pomodoro break time.
        
        Args:
            minutes (int): Break time in minutes
        """
        config = self.load_config()
        config['pomodoro_break'] = minutes
        self.save_config(config)

    def get_pomodoro_settings(self):
        """
        Get Pomodoro timer settings.
        
        Returns:
            dict: Pomodoro settings (focus_time, break_time, etc.)
        """
        config = self.load_config()
        return {
            'focus_time': config.get('pomodoro_focus', 25),
            'break_time': config.get('pomodoro_break', 5),
            'long_break': config.get('long_break', 15),
            'cycles_before_long_break': config.get('cycles_before_long_break', 4)
        }

    def reset_to_defaults(self):
        """Reset configuration to default values."""
        vault_path = self.get_vault_path()
        config = self.default_config.copy()
        if vault_path:
            config['vault_path'] = vault_path
            vault_name = Path(vault_path).name
            config['vault_name'] = vault_name
        
        self.save_config(config)

    def validate_vault_path(self, path):
        """
        Validate that a vault path is usable.
        
        Args:
            path (str): Path to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            vault_dir = Path(path)
            
            # Check if parent directory exists and is writable
            if not vault_dir.parent.exists():
                return False, "Parent directory does not exist"
            
            if not os.access(vault_dir.parent, os.W_OK):
                return False, "No write permission to parent directory"
            
            # Check if path already exists and is a directory
            if vault_dir.exists() and not vault_dir.is_dir():
                return False, "Path exists but is not a directory"
            
            return True, ""
            
        except Exception as e:
            return False, str(e)

    def _get_user_input(self, prompt, default_value=""):
        """
        Get text input from user with default value.
        
        Args:
            prompt (str): Input prompt
            default_value (str): Default value if user presses Enter
            
        Returns:
            str: User input or None if cancelled
        """
        print(f"\n{prompt} [{default_value}]: ", end="", flush=True)
        
        try:
            user_input = input().strip()
            return user_input if user_input else default_value
        except (KeyboardInterrupt, EOFError):
            return None

    def _get_single_key(self):
        """Get a single keypress from user."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)