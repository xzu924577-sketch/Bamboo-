# 🎋 Bamboo Productivity - Quick Start Guide

## Launch the App
```bash
python3 main.py
```

## First Time Setup
1. **Vault Creation**: Enter a name and path for your data vault
2. **Ready to Go**: Navigate with arrow keys, Enter to select

## Core Modules

### 🍅 Pomodoro Timer
- **Start Session**: Enter session name, timer begins
- **Controls**: Space (pause/resume), Esc (stop)
- **Features**: Unlimited cycles, automatic break prompts, session logging

### 📝 Habit Tracker  
- **Quick Log**: Space bar for instant completion
- **Detailed Log**: Enter for structured logging
- **Navigation**: D (jump date), R (today), N/M (prev/next day)
- **Streaks**: Automatically calculated current and best streaks

### ✅ Task Manager
- **View Mode**: Navigate and toggle completion (Space)
- **Edit Mode**: Press E to create/edit tasks
  - Ctrl+Enter: Add task
  - Tab: Create subtask
  - Shift+Tab: Unindent
  - Enter: Edit text
  - Del: Delete task

### 📋 Templates
- **Create**: C key to make new habit templates
- **External Editing**: Edit .template.md files in any text editor
- **Field Types**: Time, Pages, Mood (1-10), Notes, Multiple Choice

### ⚙️ Settings
- **Vault Management**: Create, switch between data vaults
- **Pomodoro Defaults**: Customize focus and break times
- **Data Location**: Change where your data is stored

## Pro Tips
- **All keyboard-driven**: No mouse needed
- **Markdown storage**: Your data is human-readable and portable
- **Date navigation**: D key works in Habits and Tasks for any date
- **Quick actions**: Space key toggles completion in most contexts
- **Esc key**: Always goes back or exits current view

## Data Structure
```
YourVault/
├── Pomodoro/           # Focus session logs
├── Habits/            # Daily habit tracking
│   └── HabitName/     # One folder per habit
├── Tasks/             # Daily task lists
└── Templates/         # Reusable habit templates
    └── Habits/
```

## Keyboard Reference
- **↑↓**: Navigate    
- **Enter**: Select/Open
- **Esc**: Back/Exit
- **Space**: Toggle completion
- **D**: Jump to date
- **R**: Return to today  
- **N/M**: Previous/Next day
- **C**: Create (habits/templates)
- **E**: Edit mode (tasks)

Enjoy building productive habits! 🚀