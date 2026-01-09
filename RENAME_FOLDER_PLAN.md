# Folder Renaming Plan (Optional but Recommended)

## Current Issue
Folder name: `Career Readiness Mentor & Skill-Gap Navigator`
- Contains spaces (requires quotes)
- Contains `&` (breaks Windows command parsing)
- Causes path resolution issues

## Recommended Rename

### Option 1: Remove Special Characters
```
Career-Readiness-Mentor-Skill-Gap-Navigator
```

### Option 2: Use Underscores
```
Career_Readiness_Mentor_Skill_Gap_Navigator
```

### Option 3: Short Name
```
CareerMentor
```

## Rename Steps (PowerShell)

```powershell
# Navigate to parent directory
cd "D:\PROJECTS"

# Rename folder (choose one option)
Rename-Item "Career Readiness Mentor & Skill-Gap Navigator" "Career-Readiness-Mentor-Skill-Gap-Navigator"

# Or use short name
Rename-Item "Career Readiness Mentor & Skill-Gap Navigator" "CareerMentor"
```

## After Renaming

1. Update all path references in:
   - `manage_project.bat`
   - `setup.ps1`
   - Any other scripts

2. Or use relative paths (recommended):
   - Scripts use `%~dp0` or `$PSScriptRoot` for relative paths
   - No hardcoded paths needed

## Current Workaround (No Rename Needed)

The batch files have been updated to handle paths with spaces and special characters using:
- Proper quoting: `"path with spaces"`
- Environment variables: `%BASE_DIR%`
- PowerShell escaping: `'path with &'`

This works but renaming is cleaner for long-term maintenance.
