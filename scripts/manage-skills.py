#!/usr/bin/env python3
"""
Claude Code Skills & Commands Manager

Cross-platform script to install/uninstall skills and commands
by creating symbolic links to ~/.claude directory.

Usage:
    python manage.py install    # Install skills and commands
    python manage.py uninstall  # Uninstall skills and commands
    python manage.py status     # Check installation status
"""

import argparse
import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    @classmethod
    def disable(cls):
        cls.GREEN = cls.YELLOW = cls.RED = cls.CYAN = cls.RESET = cls.BOLD = ""


# Disable colors on Windows if not supported
if sys.platform == "win32" and not os.environ.get("WT_SESSION"):
    try:
        os.system("")  # Enable ANSI on Windows 10+
    except Exception:
        Colors.disable()


def get_paths():
    """Get source and destination paths."""
    repo_dir = Path(__file__).resolve().parent.parent
    claude_dir = Path.home() / ".claude"

    return {
        "repo": repo_dir,
        "skills_src": repo_dir / "skills",
        "skills_dest": claude_dir / "skills",
        "commands_src": repo_dir / "commands",
        "commands_dest": claude_dir / "commands",
    }


def print_header(title: str):
    print(f"\n{Colors.BOLD}{'═' * 50}")
    print(f"{title}")
    print(f"{'═' * 50}{Colors.RESET}\n")


def print_section(title: str):
    print(f"\n{Colors.CYAN}{title}{Colors.RESET}")


def is_valid_skill(skill_path: Path) -> bool:
    """Check if directory contains a valid skill (has SKILL.md)."""
    return (skill_path / "SKILL.md").exists()


def is_our_symlink(link_path: Path, target_path: Path) -> bool:
    """Check if symlink points to our target."""
    if not link_path.is_symlink():
        return False
    try:
        return link_path.resolve() == target_path.resolve()
    except OSError:
        return False


def create_symlink(source: Path, dest: Path) -> bool:
    """Create a symbolic link. Returns True on success."""
    try:
        # On Windows, need to specify if it's a directory
        dest.symlink_to(source, target_is_directory=source.is_dir())
        return True
    except OSError as e:
        if sys.platform == "win32" and "privilege" in str(e).lower():
            print(f"{Colors.RED}Error: Administrator privileges required for symlinks on Windows.")
            print(f"Run as Administrator or enable Developer Mode.{Colors.RESET}")
        else:
            print(f"{Colors.RED}Error creating symlink: {e}{Colors.RESET}")
        return False


def install_skills(paths: dict, interactive: bool = True) -> tuple[int, int]:
    """Install skills by creating symlinks. Returns (installed, skipped) counts."""
    installed = 0
    skipped = 0

    skills_src = paths["skills_src"]
    skills_dest = paths["skills_dest"]

    if not skills_src.exists():
        print(f"{Colors.YELLOW}Skills directory not found: {skills_src}{Colors.RESET}")
        return 0, 0

    # Create destination directory
    skills_dest.mkdir(parents=True, exist_ok=True)

    print_section(f"Installing Skills...")
    print(f"  Source: {skills_src}")
    print(f"  Target: {skills_dest}\n")

    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name

        # Skip if no SKILL.md
        if not is_valid_skill(skill_dir):
            print(f"  {Colors.YELLOW}⚠  {skill_name} (no SKILL.md){Colors.RESET}")
            skipped += 1
            continue

        target_link = skills_dest / skill_name

        # Already correctly linked
        if is_our_symlink(target_link, skill_dir):
            print(f"  {Colors.GREEN}✓  {skill_name} (already installed){Colors.RESET}")
            installed += 1
            continue

        # Symlink exists but points elsewhere
        if target_link.is_symlink():
            current = target_link.resolve()
            print(f"  {Colors.YELLOW}⚠  {skill_name} (points to: {current}){Colors.RESET}")
            if interactive:
                response = input("     Replace? (y/n): ").strip().lower()
                if response == "y":
                    target_link.unlink()
                    if create_symlink(skill_dir, target_link):
                        print(f"     {Colors.GREEN}✓  Replaced{Colors.RESET}")
                        installed += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
            else:
                skipped += 1
            continue

        # Path exists as regular file/directory
        if target_link.exists():
            print(f"  {Colors.YELLOW}⚠  {skill_name} (exists as file/directory){Colors.RESET}")
            skipped += 1
            continue

        # Create new symlink
        if create_symlink(skill_dir, target_link):
            print(f"  {Colors.GREEN}✓  {skill_name}{Colors.RESET}")
            installed += 1
        else:
            skipped += 1

    return installed, skipped


def install_commands(paths: dict, interactive: bool = True) -> tuple[int, int]:
    """Install commands by creating symlinks. Returns (installed, skipped) counts."""
    installed = 0
    skipped = 0

    commands_src = paths["commands_src"]
    commands_dest = paths["commands_dest"]

    if not commands_src.exists():
        print(f"{Colors.YELLOW}Commands directory not found: {commands_src}{Colors.RESET}")
        return 0, 0

    # Create destination directory
    commands_dest.mkdir(parents=True, exist_ok=True)

    print_section(f"Installing Commands...")
    print(f"  Source: {commands_src}")
    print(f"  Target: {commands_dest}\n")

    for cmd_file in sorted(commands_src.glob("*.md")):
        cmd_name = cmd_file.name

        # Skip README.md
        if cmd_name == "README.md":
            continue

        target_link = commands_dest / cmd_name

        # Already correctly linked
        if is_our_symlink(target_link, cmd_file):
            print(f"  {Colors.GREEN}✓  {cmd_name} (already installed){Colors.RESET}")
            installed += 1
            continue

        # Symlink exists but points elsewhere
        if target_link.is_symlink():
            current = target_link.resolve()
            print(f"  {Colors.YELLOW}⚠  {cmd_name} (points to: {current}){Colors.RESET}")
            if interactive:
                response = input("     Replace? (y/n): ").strip().lower()
                if response == "y":
                    target_link.unlink()
                    if create_symlink(cmd_file, target_link):
                        print(f"     {Colors.GREEN}✓  Replaced{Colors.RESET}")
                        installed += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
            else:
                skipped += 1
            continue

        # Path exists as regular file/directory
        if target_link.exists():
            print(f"  {Colors.YELLOW}⚠  {cmd_name} (exists as file/directory){Colors.RESET}")
            skipped += 1
            continue

        # Create new symlink
        if create_symlink(cmd_file, target_link):
            print(f"  {Colors.GREEN}✓  {cmd_name}{Colors.RESET}")
            installed += 1
        else:
            skipped += 1

    return installed, skipped


def uninstall_skills(paths: dict) -> tuple[int, int]:
    """Uninstall skills by removing symlinks. Returns (removed, skipped) counts."""
    removed = 0
    skipped = 0

    skills_src = paths["skills_src"]
    skills_dest = paths["skills_dest"]

    print_section("Uninstalling Skills...")
    print(f"  Target: {skills_dest}\n")

    if not skills_dest.exists():
        print(f"  {Colors.YELLOW}No skills directory found{Colors.RESET}")
        return 0, 0

    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        target_link = skills_dest / skill_name

        if is_our_symlink(target_link, skill_dir):
            target_link.unlink()
            print(f"  {Colors.GREEN}✓  Removed {skill_name}{Colors.RESET}")
            removed += 1
        elif target_link.is_symlink():
            print(f"  {Colors.YELLOW}⚠  {skill_name} (points elsewhere){Colors.RESET}")
            skipped += 1
        elif target_link.exists():
            print(f"  {Colors.YELLOW}⚠  {skill_name} (not a symlink){Colors.RESET}")
            skipped += 1
        else:
            print(f"  ○  {skill_name} (not installed)")

    return removed, skipped


def uninstall_commands(paths: dict) -> tuple[int, int]:
    """Uninstall commands by removing symlinks. Returns (removed, skipped) counts."""
    removed = 0
    skipped = 0

    commands_src = paths["commands_src"]
    commands_dest = paths["commands_dest"]

    print_section("Uninstalling Commands...")
    print(f"  Target: {commands_dest}\n")

    if not commands_dest.exists():
        print(f"  {Colors.YELLOW}No commands directory found{Colors.RESET}")
        return 0, 0

    for cmd_file in sorted(commands_src.glob("*.md")):
        cmd_name = cmd_file.name

        if cmd_name == "README.md":
            continue

        target_link = commands_dest / cmd_name

        if is_our_symlink(target_link, cmd_file):
            target_link.unlink()
            print(f"  {Colors.GREEN}✓  Removed {cmd_name}{Colors.RESET}")
            removed += 1
        elif target_link.is_symlink():
            print(f"  {Colors.YELLOW}⚠  {cmd_name} (points elsewhere){Colors.RESET}")
            skipped += 1
        elif target_link.exists():
            print(f"  {Colors.YELLOW}⚠  {cmd_name} (not a symlink){Colors.RESET}")
            skipped += 1
        else:
            print(f"  ○  {cmd_name} (not installed)")

    return removed, skipped


def check_status(paths: dict):
    """Check and display installation status."""
    skills_src = paths["skills_src"]
    skills_dest = paths["skills_dest"]
    commands_src = paths["commands_src"]
    commands_dest = paths["commands_dest"]

    print_section("Skills Status")
    print(f"  Source: {skills_src}")
    print(f"  Target: {skills_dest}\n")

    installed = 0
    not_installed = 0

    for skill_dir in sorted(skills_src.iterdir()):
        if not skill_dir.is_dir() or not is_valid_skill(skill_dir):
            continue

        skill_name = skill_dir.name
        target_link = skills_dest / skill_name

        if is_our_symlink(target_link, skill_dir):
            print(f"  {Colors.GREEN}✓  {skill_name}{Colors.RESET}")
            installed += 1
        else:
            print(f"  {Colors.RED}✗  {skill_name}{Colors.RESET}")
            not_installed += 1

    print(f"\n  Installed: {installed} | Not installed: {not_installed}")

    print_section("Commands Status")
    print(f"  Source: {commands_src}")
    print(f"  Target: {commands_dest}\n")

    installed = 0
    not_installed = 0

    for cmd_file in sorted(commands_src.glob("*.md")):
        if cmd_file.name == "README.md":
            continue

        cmd_name = cmd_file.name
        target_link = commands_dest / cmd_name

        if is_our_symlink(target_link, cmd_file):
            print(f"  {Colors.GREEN}✓  {cmd_name}{Colors.RESET}")
            installed += 1
        else:
            print(f"  {Colors.RED}✗  {cmd_name}{Colors.RESET}")
            not_installed += 1

    print(f"\n  Installed: {installed} | Not installed: {not_installed}")


def cmd_install(args):
    """Handle install command."""
    paths = get_paths()
    print_header("Installing Skills and Commands")

    skills_installed, skills_skipped = install_skills(paths, not args.yes)
    commands_installed, commands_skipped = install_commands(paths, not args.yes)

    print_header("Installation Complete!")
    print(f"  Skills:   Installed: {skills_installed} | Skipped: {skills_skipped}")
    print(f"  Commands: Installed: {commands_installed} | Skipped: {commands_skipped}")


def cmd_uninstall(args):
    """Handle uninstall command."""
    paths = get_paths()
    print_header("Uninstalling Skills and Commands")

    skills_removed, skills_skipped = uninstall_skills(paths)
    commands_removed, commands_skipped = uninstall_commands(paths)

    print_header("Uninstallation Complete!")
    print(f"  Skills:   Removed: {skills_removed} | Skipped: {skills_skipped}")
    print(f"  Commands: Removed: {commands_removed} | Skipped: {commands_skipped}")


def cmd_status(args):
    """Handle status command."""
    paths = get_paths()
    print_header("Installation Status")
    check_status(paths)


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Skills & Commands Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py install      Install all skills and commands
  python manage.py install -y   Install without prompts
  python manage.py uninstall    Uninstall all skills and commands
  python manage.py status       Check installation status
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install skills and commands")
    install_parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip confirmation prompts"
    )
    install_parser.set_defaults(func=cmd_install)

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Uninstall skills and commands"
    )
    uninstall_parser.set_defaults(func=cmd_uninstall)

    # Status command
    status_parser = subparsers.add_parser("status", help="Check installation status")
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
