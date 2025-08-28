"""
Pomodoro module for Bamboo Productivity app.
Handles focus timer sessions with unlimited cycles and markdown logging.
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path


class Pomodoro:
    """
    Pomodoro timer with session tracking and markdown logging.
    Supports unlimited cycles, break tracking, and statistics.
    """
    
    def __init__(self):
        """Initialize Pomodoro with default settings."""
        # Load settings from vault
        from .settings import Settings
        self.settings = Settings()
        pomodoro_settings = self.settings.get_pomodoro_settings()
        
        self.work_duration = pomodoro_settings['focus_time'] * 60  # Convert to seconds
        self.short_break = pomodoro_settings['break_time'] * 60
        self.long_break = pomodoro_settings['long_break'] * 60
        self.cycles_before_long_break = pomodoro_settings['cycles_before_long_break']
        
        self.session_name = ""
        self.running = False
        self.current_cycle = 0
        self.in_session = False
        self.timer_running = False
        self.current_timer_type = None  # 'work', 'short_break', 'long_break'
        self.remaining_time = 0
        
        self.stats = {
            'work_cycles': 0,
            'break_cycles': 0,
            'total_work_time': 0,
            'total_break_time': 0,
            'longest_work_session': 0,
            'session_start': None,
            'session_end': None
        }
        
        self.menu_selection = 0
        self.menu_items = [
            "Start new session",
            "View today's stats", 
            "Session history",
            "Back to dashboard"
        ]

    def run(self):
        """Main Pomodoro module loop."""
        self.running = True
        while self.running:
            self.display_menu()
            self.handle_menu_input()

    def display_menu(self):
        """Display Pomodoro main menu."""
        os.system('clear')
        print("\033[32m")  # Green tint
        print("╭─────────────────────────────────────╮")
        print("│           🍅 Pomodoro Timer          │")
        print("├─────────────────────────────────────┤")
        
        for i, item in enumerate(self.menu_items):
            prefix = "► " if i == self.menu_selection else "  "
            print(f"│ {prefix}{item:<32} │")
        
        print("├─────────────────────────────────────┤")
        
        # Show current session info if active
        if self.in_session:
            print(f"│ Active Session: {self.session_name[:20]:<20} │")
            print(f"│ Work Cycles: {self.stats['work_cycles']:<3} Break Cycles: {self.stats['break_cycles']:<3} │")
            print(f"│ Total Work: {self.format_time(self.stats['total_work_time']):<8} Total Break: {self.format_time(self.stats['total_break_time']):<8} │")
            print("├─────────────────────────────────────┤")
        
        print("│ ↑↓: Navigate  Enter: Select  Esc: Back │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def handle_menu_input(self):
        """Handle keyboard input for Pomodoro menu."""
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape sequence
                try:
                    key += sys.stdin.read(2)
                    if key == '\x1b[A':  # Up arrow
                        self.menu_selection = (self.menu_selection - 1) % len(self.menu_items)
                    elif key == '\x1b[B':  # Down arrow
                        self.menu_selection = (self.menu_selection + 1) % len(self.menu_items)
                except:
                    # Single Esc
                    self.running = False
            elif key == '\r' or key == '\n':  # Enter
                self._handle_menu_selection()
            elif key == '\x03':  # Ctrl+C
                self.running = False
                
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _handle_menu_selection(self):
        """Handle menu selection based on current choice."""
        if self.menu_selection == 0:  # Start new session
            self._start_new_session()
        elif self.menu_selection == 1:  # View today's stats
            self._view_todays_stats()
        elif self.menu_selection == 2:  # Session history
            self._view_session_history()
        elif self.menu_selection == 3:  # Back to dashboard
            self.running = False

    def _start_new_session(self):
        """Start a new Pomodoro session with user input."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│          🍅 New Session             │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ Enter session name:                 │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        try:
            session_name = input("Session name: ").strip()
            if not session_name:
                session_name = f"Session_{datetime.now().strftime('%H%M')}"
            
            self.session_name = session_name
            self.in_session = True
            self.stats['session_start'] = datetime.now()
            self.current_cycle = 0
            
            # Reset stats for new session
            self.stats.update({
                'work_cycles': 0,
                'break_cycles': 0,
                'total_work_time': 0,
                'total_break_time': 0,
                'longest_work_session': 0
            })
            
            # Start first work cycle
            self._start_work_cycle()
            
        except (KeyboardInterrupt, EOFError):
            return

    def _start_work_cycle(self):
        """Start a work cycle."""
        self.current_cycle += 1
        self.current_timer_type = 'work'
        self.remaining_time = self.work_duration
        
        cycle_start_time = time.time()
        self._run_timer()
        cycle_duration = int(time.time() - cycle_start_time)
        
        # Update stats
        self.stats['work_cycles'] += 1
        self.stats['total_work_time'] += cycle_duration
        self.stats['longest_work_session'] = max(
            self.stats['longest_work_session'], 
            cycle_duration
        )
        
        # Ask if user wants a break
        if self._ask_for_break():
            self._start_break_cycle()
        else:
            # Continue with another work cycle
            self._start_work_cycle()

    def _start_break_cycle(self):
        """Start a break cycle."""
        # Determine break type (short vs long)
        if self.stats['work_cycles'] % self.cycles_before_long_break == 0:
            break_duration = self.long_break
            break_type = 'long_break'
        else:
            break_duration = self.short_break
            break_type = 'short_break'
        
        self.current_timer_type = break_type
        self.remaining_time = break_duration
        
        break_start_time = time.time()
        self._run_timer()
        break_duration_actual = int(time.time() - break_start_time)
        
        # Update stats
        self.stats['break_cycles'] += 1
        self.stats['total_break_time'] += break_duration_actual
        
        # Ask if user wants to continue
        if self._ask_to_continue():
            self._start_work_cycle()
        else:
            self._end_session()

    def _run_timer(self):
        """Run the current timer with real-time display."""
        self.timer_running = True
        start_time = time.time()
        
        while self.timer_running and self.remaining_time > 0:
            self.display_timer()
            
            # Wait 1 second or check for user input
            if self._check_timer_input():
                break
                
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            self.remaining_time = max(0, 
                (self.work_duration if self.current_timer_type == 'work' 
                 else (self.long_break if self.current_timer_type == 'long_break' 
                       else self.short_break)) - elapsed)
        
        # Timer completed or was stopped
        if self.remaining_time <= 0:
            self._show_timer_complete()

    def _check_timer_input(self):
        """
        Check for user input during timer (non-blocking).
        
        Returns:
            bool: True if timer should stop
        """
        import select
        import termios
        import tty
        
        # Check if input is available (non-blocking)
        if select.select([sys.stdin], [], [], 0)[0]:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                key = sys.stdin.read(1)
                
                if key == ' ':  # Space - pause/resume
                    self._pause_timer()
                elif key == '\x1b':  # Esc - stop timer
                    self.timer_running = False
                    return True
                elif key == '\x03':  # Ctrl+C - stop timer
                    self.timer_running = False
                    return True
                    
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        return False

    def _pause_timer(self):
        """Pause/resume timer functionality."""
        paused = True
        pause_start = time.time()
        
        while paused:
            self._display_paused()
            
            # Wait for resume input
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.cbreak(fd)
                key = sys.stdin.read(1)
                
                if key == ' ':  # Space - resume
                    paused = False
                elif key == '\x1b' or key == '\x03':  # Esc/Ctrl+C - stop
                    self.timer_running = False
                    return
                    
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        # Adjust remaining time to account for pause duration
        pause_duration = int(time.time() - pause_start)
        # Note: We don't subtract pause time since we want accurate work time tracking

    def display_timer(self):
        """Display the running timer interface."""
        os.system('clear')
        print("\033[32m")  # Green tint
        
        # Timer type display
        if self.current_timer_type == 'work':
            timer_name = f"🍅 WORK SESSION - Cycle {self.current_cycle}"
            emoji = "💪"
        elif self.current_timer_type == 'short_break':
            timer_name = "☕ SHORT BREAK"
            emoji = "😌"
        else:  # long_break
            timer_name = "🌟 LONG BREAK"
            emoji = "😴"
        
        print("╭─────────────────────────────────────╮")
        print(f"│ {timer_name:<35} │")
        print("├─────────────────────────────────────┤")
        print(f"│ Session: {self.session_name[:25]:<25} │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        
        # Large time display
        time_str = self.format_time(self.remaining_time)
        print(f"│     {emoji}    {time_str:>8}    {emoji}     │")
        print("│                                     │")
        
        # Progress bar
        if self.current_timer_type == 'work':
            total_time = self.work_duration
        elif self.current_timer_type == 'long_break':
            total_time = self.long_break
        else:
            total_time = self.short_break
            
        progress = max(0, (total_time - self.remaining_time) / total_time)
        bar_width = 25
        filled = int(progress * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"│ [{bar}] │")
        print("│                                     │")
        
        print("├─────────────────────────────────────┤")
        print("│ Space: Pause  Esc: Stop             │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def _display_paused(self):
        """Display paused timer interface."""
        os.system('clear')
        print("\033[33m")  # Yellow for pause
        print("╭─────────────────────────────────────╮")
        print("│              ⏸️  PAUSED              │")
        print("├─────────────────────────────────────┤")
        print(f"│ Session: {self.session_name[:25]:<25} │")
        print(f"│ Timer: {self.current_timer_type.replace('_', ' ').title():<27} │")
        print(f"│ Remaining: {self.format_time(self.remaining_time):<23} │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│          Timer is paused            │")
        print("│                                     │")
        print("├─────────────────────────────────────┤")
        print("│ Space: Resume  Esc: Stop            │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")

    def _show_timer_complete(self):
        """Show timer completion notification."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│              🎉 COMPLETE!            │")
        print("├─────────────────────────────────────┤")
        
        if self.current_timer_type == 'work':
            print("│   Work session completed!           │")
            print("│   Great job staying focused! 💪     │")
        else:
            print("│   Break time is over!               │")
            print("│   Ready to get back to work? 🚀     │")
        
        print("│                                     │")
        print("│   Press any key to continue...      │")
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

    def _ask_for_break(self):
        """Ask user if they want to take a break."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│          🍅 Work Complete!           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│   Take a break?                     │")
        print("│                                     │")
        print("│   Y - Yes, take a break             │")
        print("│   N - No, continue working          │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1).lower()
            return key == 'y'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _ask_to_continue(self):
        """Ask user if they want to continue the session."""
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│         ☕ Break Complete!           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│   Continue session?                 │")
        print("│                                     │")
        print("│   Y - Yes, keep going               │")
        print("│   N - No, end session              │")
        print("│                                     │")
        print("╰─────────────────────────────────────╯")
        print("\033[0m")
        
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.cbreak(fd)
            key = sys.stdin.read(1).lower()
            return key == 'y'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _end_session(self):
        """End the current session and save log."""
        self.stats['session_end'] = datetime.now()
        self.save_session_log()
        self.in_session = False
        
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│           📊 Session Summary         │")
        print("├─────────────────────────────────────┤")
        print(f"│ Session: {self.session_name[:25]:<25} │")
        print(f"│ Work Cycles: {self.stats['work_cycles']:<19} │")
        print(f"│ Break Cycles: {self.stats['break_cycles']:<18} │")
        print(f"│ Total Work: {self.format_time(self.stats['total_work_time']):<21} │")
        print(f"│ Total Break: {self.format_time(self.stats['total_break_time']):<20} │")
        print(f"│ Longest Work: {self.format_time(self.stats['longest_work_session']):<19} │")
        print("│                                     │")
        print("│ Session saved! Press any key...     │")
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

    def save_session_log(self):
        """Save current session to markdown file."""
        if not self.stats.get('session_start'):
            return
        
        # Get vault path
        vault_path = self.get_vault_path()
        if not vault_path:
            return
        
        # Create pomodoro directory if it doesn't exist
        pomodoro_dir = Path(vault_path) / "Pomodoro"
        pomodoro_dir.mkdir(exist_ok=True)
        
        # Create filename
        filename = self.create_session_filename()
        filepath = pomodoro_dir / filename
        
        # Calculate session duration
        if self.stats.get('session_end'):
            session_duration = self.stats['session_end'] - self.stats['session_start']
            total_session_time = int(session_duration.total_seconds())
        else:
            total_session_time = self.stats['total_work_time'] + self.stats['total_break_time']
        
        # Create markdown content
        content = f"""# Pomodoro Session: {self.session_name}

Date: {self.stats['session_start'].strftime('%Y-%m-%d')}
Start Time: {self.stats['session_start'].strftime('%H:%M:%S')}
End Time: {self.stats.get('session_end', datetime.now()).strftime('%H:%M:%S')}

## Session Statistics

- Work cycles completed: {self.stats['work_cycles']}
- Break cycles taken: {self.stats['break_cycles']}
- Total work time: {self.format_time(self.stats['total_work_time'])}
- Total break time: {self.format_time(self.stats['total_break_time'])}
- Longest work session: {self.format_time(self.stats['longest_work_session'])}
- Total session time: {self.format_time(total_session_time)}

## Session Notes

Focus Quality: [Rate 1-10]
Key Accomplishments:
- 
- 
- 

Distractions/Challenges:
- 
- 

Next Session Goals:
- 
- 
"""
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Error saving session log: {e}")

    def _view_todays_stats(self):
        """Display today's Pomodoro statistics."""
        # Placeholder for stats view
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│         📊 Today's Stats            │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ This feature will show:             │")
        print("│ - All sessions today                │")
        print("│ - Total focus time                  │")
        print("│ - Average session length            │")
        print("│ - Session count                     │")
        print("│                                     │")
        print("│ [Coming soon...]                    │")
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

    def _view_session_history(self):
        """Display session history."""
        # Placeholder for history view
        os.system('clear')
        print("\033[32m")
        print("╭─────────────────────────────────────╮")
        print("│        📈 Session History           │")
        print("├─────────────────────────────────────┤")
        print("│                                     │")
        print("│ This feature will show:             │")
        print("│ - Past sessions by date             │")
        print("│ - Session trends                    │")
        print("│ - Productivity insights             │")
        print("│ - Session comparisons               │")
        print("│                                     │")
        print("│ [Coming soon...]                    │")
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

    def load_session_stats(self):
        """Load session statistics from today's log."""
        # Placeholder for loading stats
        pass

    def display_stats(self):
        """Display session statistics table."""
        # Placeholder for stats display
        pass

    def get_vault_path(self):
        """Get the current vault path from settings."""
        vault_path = self.settings.get_vault_path()
        
        # If no vault path found, try to load config
        if not vault_path:
            config = self.settings.load_config()
            vault_path = config.get('vault_path')
        
        return vault_path

    def create_session_filename(self):
        """Create filename for current session log."""
        today = datetime.now().strftime("%Y-%m-%d")
        return f"Pomodoro_{self.session_name}_{today}.md"

    def format_time(self, seconds):
        """
        Format seconds into readable time string.
        
        Args:
            seconds (int): Time in seconds
            
        Returns:
            str: Formatted time string (HH:MM:SS)
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"