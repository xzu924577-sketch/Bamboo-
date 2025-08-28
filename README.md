# 🎋 Bamboo Productivity

A terminal-based, keyboard-only productivity app for Linux and Android Termux.

## Overview

Bamboo Productivity centralizes habit tracking, Pomodoro focus sessions, and task management into a single terminal interface. It uses markdown files for logging, supports dynamic streak tracking, and keeps all input keyboard-friendly.

## Features

- **📝 Habit Tracking**: Daily habit logging with streak calculation and template support
- **🍅 Pomodoro Timer**: Focus sessions with unlimited cycles and session statistics  
- **✅ Task Management**: Daily tasks with subtask support and completion tracking
- **📋 Templates**: Customizable habit templates with multiple field types
- **🗂️ Vault System**: Organized data storage with multiple vault support
- **⌨️ Keyboard-Only**: Fully navigable without mouse input
- **📱 Cross-Platform**: Works on Linux terminals and Android Termux

## Installation

### Prerequisites
- Python 3.7+
- Linux terminal or Android Termux

### Setup
```bash
git clone <repository-url>
cd Bamboo-Productivity
python3 main.py
```

## Usage

### First Launch
On first launch, you'll be guided through vault setup:
1. Choose a vault name (e.g., "BambooVault")
2. Select vault location (e.g., `/home/user/BambooVault`)
3. App creates directory structure automatically

### Main Navigation
- **↑↓**: Navigate between options
- **Enter**: Select/Open
- **Esc**: Back/Cancel

### Modules

#### 📝 Habits
- Track daily habits with customizable templates
- View current and best streaks
- Navigate between dates (D: jump, R: today, N: prev, M: next)
- Log multiple field types: time, pages, mood, notes, MCQs

#### 🍅 Pomodoro
- Start focus sessions with customizable durations
- Unlimited cycles (no forced breaks)
- Session statistics and history
- Automatic markdown logging

#### ✅ Tasks
- Create and manage daily tasks
- Support for subtasks (Tab to indent)
- Toggle completion with Space
- Navigate between dates

#### 📋 Templates
- Create habit templates with custom fields
- Edit templates within app or externally
- Multiple field types: time, pages, mood, notes, MCQ

## Vault Structure

```
VaultRoot/
├─ Pomodoro/
│  └─ Pomodoro_SessionName_YYYY-MM-DD.md
├─ Habits/
│  └─ HabitName/
│     └─ HabitName-YYYY-MM-DD.md
├─ Tasks/
│  └─ Task_YYYY-MM-DD.md
└─ Templates/
   └─ Habits/
      └─ TemplateName.template.md
```

## Keybinds Reference

### Global
- **↑↓**: Move selection/cursor
- **←→**: Navigate pages/back  
- **Enter**: Select/Open/Start
- **Esc**: Back/Cancel
- **Ctrl+C**: Exit application

### Date Navigation
- **D**: Jump to specific date
- **R**: Go to today
- **N**: Previous day
- **M**: Next day

### Editing
- **Space**: Toggle completion
- **Ctrl+S**: Save changes
- **Ctrl+Enter**: Add new task line
- **Tab**: Indent/Create subtask
- **Shift+Tab**: Unindent task

## File Formats

All data is stored in human-readable markdown files:

### Habit Log Example
```markdown
# Habit: Read 30 Pages
Date: 2025-01-20

## Time
- 20:30

## Pages [unit]
- 34

## Mood [scale 1-10]
- 8

## Notes
- Finished chapter 4
- Started chapter 5
```

### Task File Example
```markdown
# Tasks - 2025-01-20

- [ ] Write project proposal
- [x] Read 30 pages
    - [x] Chapter 3
    - [ ] Chapter 4
- [ ] Workout at 7pm
```

## Configuration

Settings are stored in `.bamboo_config.json` within each vault:

```json
{
  "vault_name": "BambooVault",
  "vault_path": "/home/user/BambooVault",
  "pomodoro_focus": 25,
  "pomodoro_break": 5,
  "long_break": 15,
  "cycles_before_long_break": 4
}
```

## Development Status

Current implementation status:
- [x] Project skeleton and module structure
- [x] Comprehensive documentation and mockups
- [ ] Vault and configuration system (Step 2)
- [ ] Dashboard implementation (Step 3)
- [ ] Pomodoro module (Step 4)
- [ ] Habits module (Step 5)
- [ ] Tasks module (Step 6)
- [ ] Templates module (Step 7)
- [ ] Settings module (Step 8)
- [ ] Help module (Step 9)
- [ ] Testing and polish (Step 10)

## Contributing

This project follows a modular architecture for easy expansion:
1. Each module is self-contained in its own file
2. Consistent interface patterns across modules
3. Markdown-based storage for data portability
4. Keyboard-only design for accessibility

Feel free to submit issues and pull requests for improvements!