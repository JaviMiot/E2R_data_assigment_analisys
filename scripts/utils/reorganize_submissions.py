#!/usr/bin/env python3
"""
Script to extract all nested zip/rar files and move files to root of each student folder.
"""

import os
import zipfile
import shutil
from pathlib import Path
import tempfile


def extract_archive(archive_path, extract_to):
    """Extract zip or rar archive to destination."""
    archive_path = Path(archive_path)
    
    if archive_path.suffix.lower() == '.zip':
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except Exception as e:
            print(f"  ⚠ Error extracting {archive_path.name}: {e}")
            return False
    elif archive_path.suffix.lower() == '.rar':
        # Try using unrar if available, otherwise skip
        try:
            import subprocess
            result = subprocess.run(['unrar', 'x', '-y', str(archive_path), str(extract_to)],
                                  capture_output=True, timeout=30)
            return result.returncode == 0
        except:
            print(f"  ⚠ Cannot extract RAR file {archive_path.name} (unrar not available)")
            return False
    
    return False


def find_all_useful_files(directory):
    """Find all xlsx, pdf, doc, docx files recursively."""
    directory = Path(directory)
    useful_extensions = {'.xlsx', '.xls', '.pdf', '.doc', '.docx'}
    found_files = []
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        for file in files:
            file_path = root_path / file
            if file_path.suffix.lower() in useful_extensions:
                found_files.append(file_path)
    
    return found_files


def extract_all_archives_recursive(directory, max_depth=5):
    """Recursively extract all archives in a directory."""
    directory = Path(directory)
    depth = 0
    
    while depth < max_depth:
        archives = list(directory.glob('**/*.zip')) + list(directory.glob('**/*.rar'))
        if not archives:
            break
        
        for archive in archives:
            extract_to = archive.parent
            extract_archive(archive, extract_to)
        
        depth += 1


def reorganize_student_folder(student_dir):
    """Extract all archives and move files to root of student folder."""
    student_dir = Path(student_dir)
    student_name = student_dir.name
    
    print(f"\n📁 Processing: {student_name}")
    
    # Step 1: Extract all archives recursively
    print("  🔓 Extracting archives...")
    extract_all_archives_recursive(student_dir)
    
    # Step 2: Find all useful files
    useful_files = find_all_useful_files(student_dir)
    
    if not useful_files:
        print("  ⚠ No useful files found")
        return
    
    # Step 3: Move all files to root, avoiding duplicates
    files_moved = 0
    for file_path in useful_files:
        # Skip if already in root
        if file_path.parent == student_dir:
            continue
        
        # Determine destination
        dest_path = student_dir / file_path.name
        
        # Handle duplicates
        if dest_path.exists():
            # If files are identical, skip
            if dest_path.stat().st_size == file_path.stat().st_size:
                continue
            
            # Otherwise, add a number suffix
            counter = 1
            stem = dest_path.stem
            suffix = dest_path.suffix
            while dest_path.exists():
                dest_path = student_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        
        # Move file
        try:
            shutil.move(str(file_path), str(dest_path))
            files_moved += 1
        except Exception as e:
            print(f"  ⚠ Error moving {file_path.name}: {e}")
    
    print(f"  ✓ Moved {files_moved} files to root")
    
    # Step 4: Clean up empty directories and archive files
    print("  🧹 Cleaning up...")
    
    # Remove all zip and rar files
    for archive in list(student_dir.glob('**/*.zip')) + list(student_dir.glob('**/*.rar')):
        try:
            archive.unlink()
        except:
            pass
    
    # Remove empty directories
    for root, dirs, files in os.walk(student_dir, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except:
                pass
    
    # Final count
    final_files = list(student_dir.glob('*.xlsx')) + list(student_dir.glob('*.pdf')) + \
                  list(student_dir.glob('*.xls')) + list(student_dir.glob('*.doc')) + \
                  list(student_dir.glob('*.docx'))
    
    print(f"  📊 Final: {len(final_files)} files in root")


def main():
    """Process all student submission folders."""
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    base_dir = ROOT_DIR
    
    # Find all student directories
    student_dirs = sorted([d for d in base_dir.glob("*_assignsubmission_file")])
    
    print(f"Found {len(student_dirs)} student submissions")
    print("=" * 80)
    
    for student_dir in student_dirs:
        reorganize_student_folder(student_dir)
    
    print("\n" + "=" * 80)
    print("✅ All submissions reorganized!")


if __name__ == '__main__':
    main()
