# Windows Installation Package Testing Instructions

## Testing the PyInstaller Executable

1. After creating the executable using the instructions in `windows_packaging_instructions.md`:
   - Navigate to the `dist` folder
   - Run `MoodTracker.exe`
   - Verify the application launches without errors
   - Test all functionality:
     - Enter a mood and save it
     - Verify the entry appears in the listbox with correct timestamp
     - Delete a selected entry
     - Clear all entries
     - Close and reopen the application to verify data persistence

2. Test on different Windows versions if possible:
   - Windows 10
   - Windows 11

3. Check for common issues:
   - Missing DLL errors
   - Database access errors
   - GUI rendering issues

## Testing the Pynsist Installer

1. After creating the installer using the instructions in `windows_installer_instructions.md`:
   - Run the installer from the `build\nsis` folder
   - Verify the installation completes without errors
   - Check that the application appears in the Start menu
   - Launch the application from the Start menu
   - Verify all functionality works as expected

2. Test the uninstaller:
   - Uninstall the application from Control Panel or Settings
   - Verify the uninstallation completes without errors
   - Check that application files are removed

3. Test installation options:
   - Install for all users (requires admin privileges)
   - Install for current user only

## Reporting Issues

If you encounter any issues during testing:
1. Note the exact error message
2. Document the steps to reproduce the issue
3. Check the application logs (if available)
4. Consider rebuilding the executable or installer with debug options enabled
