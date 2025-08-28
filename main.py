#!/usr/bin/env python3
"""
Bamboo Productivity - Main Entry Point
A terminal-based productivity app with Pomodoro, Habits, Tasks, and more.
"""

import sys
import os
from src.dashboard import Dashboard
from src.settings import Settings


def main():
    """
    Main entry point for Bamboo Productivity app.
    Handles initial setup and launches dashboard.
    """
    try:
        # Initialize settings and check for first-time setup
        settings = Settings()
        
        if settings.is_first_time_setup():
            settings.first_time_setup()
        
        # Launch dashboard
        dashboard = Dashboard()
        dashboard.run()
        
    except KeyboardInterrupt:
        print("\n\nExiting Bamboo Productivity. Have a productive day! 🎋")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()