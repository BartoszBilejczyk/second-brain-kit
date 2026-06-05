#!/usr/bin/env python3
"""
setup.py — guided onboarding for second-brain-kit.

Run directly: python setup/setup.py
Or via the /brain-setup Claude Code skill.

This script:
  1. Checks Python >= 3.13
  2. Asks 4 questions to configure your brain
  3. Writes the ## User section to CLAUDE.md
  4. Writes a starter profile.md
  5. Updates .gitignore based on your recordings privacy choice
  6. Warns you about download sizes
  7. Runs pip install -r tools/requirements.txt
  8. Runs a small test embed to confirm tooling works
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import date

REPO_ROOT = Path(__file__).parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
PROFILE_MD = REPO_ROOT / "profile.md"
GITIGNORE = REPO_ROOT / ".gitignore"
REQUIREMENTS = REPO_ROOT / "tools" / "requirements.txt"


def check_python_version():
    v = sys.version_info
    if (v.major, v.minor) < (3, 13):
        print(f"\nPython {v.major}.{v.minor} detected. second-brain-kit requires Python 3.13+.")
        print("Download the latest Python at: https://python.org/downloads")
        print("\nAfter installing, run this script again.")
        sys.exit(1)


def ask(prompt: str, default: str = "") -> str:
    """Ask a question; return stripped answer or default."""
    if default:
        answer = input(f"{prompt} [{default}]: ").strip()
        return answer if answer else default
    else:
        return input(f"{prompt}: ").strip()


def write_user_section(name: str, goal: str, language: str):
    """Update the ## User section in CLAUDE.md."""
    content = CLAUDE_MD.read_text(encoding="utf-8")

    new_section = f"""## User

Name/alias: {name}
Goal: {goal}
Language: {language}

*(This section is written by `/brain-setup` during onboarding. Update it any time.)*"""

    # Replace the existing ## User section
    pattern = r"## User\n.*?(?=\n---|\n## )"
    replacement = new_section
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        # Section not found with regex — append it after the first ---
        lines = content.split("\n")
        insert_at = next((i for i, l in enumerate(lines) if l == "---"), None)
        if insert_at is not None:
            lines.insert(insert_at + 1, "\n" + new_section + "\n")
            new_content = "\n".join(lines)

    CLAUDE_MD.write_text(new_content, encoding="utf-8")
    print(f"  ✓ CLAUDE.md updated with your profile")


def write_starter_profile(name: str, goal: str):
    """Write the starter profile.md."""
    today = date.today().isoformat()
    content = f"""# Profile

*(Written and maintained by brain-ingest. Enriched after each batch — never replaced.)*

## Identity

**Name/alias:** {name}

**In one sentence:** [brain-ingest will fill this in after your first interview session]

## Current situation

*Setup completed {today}. Ready for first brain-ingest.*

Goal: {goal}

## Settled beliefs

*(none yet — populated by brain-ingest)*

## Defining stories

*(none yet)*

## How you work / create

*(none yet)*

## Key relationships

*(none yet)*

## Open questions

*(none yet)*
"""
    PROFILE_MD.write_text(content, encoding="utf-8")
    print(f"  ✓ profile.md written")


def update_gitignore_for_recordings(exclude_recordings: bool):
    """Uncomment or add the recordings gitignore line."""
    content = GITIGNORE.read_text(encoding="utf-8")

    if exclude_recordings:
        # Uncomment the line if it's commented out
        new_content = content.replace(
            "# interview/recordings/",
            "interview/recordings/"
        )
        if new_content == content:
            # Not present — add it
            new_content = content.rstrip() + "\ninterview/recordings/\n"
        GITIGNORE.write_text(new_content, encoding="utf-8")
        print("  ✓ Recordings excluded from git (added to .gitignore)")
    else:
        print("  ✓ Recordings will be committed to git (you can change this in .gitignore)")


def print_download_warning():
    print("""
  ⚠  First-run downloads — what to expect:

     sentence-transformers model  ~420 MB  (semantic search, downloaded once)
     PyTorch                      ~700 MB  (required by sentence-transformers)
     Whisper (tiny)                ~75 MB  (if you use fast transcription)
     Whisper (small)              ~460 MB  (if you use balanced transcription)
     Whisper (medium)             ~1.5 GB  (if you use accurate transcription)

     Total: ~1.2 GB to ~2.6 GB depending on Whisper model choice.
     Everything downloads once and runs offline forever after.
""")


def run_pip_install() -> bool:
    """Run pip install -r tools/requirements.txt. Returns True on success."""
    print("\nInstalling Python dependencies...")
    print("(This may take a few minutes on first run)\n")

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        capture_output=False,
    )

    if result.returncode != 0:
        print("\n❌ pip install failed.")
        print("Troubleshooting:")
        print("  1. Make sure pip is up to date: python -m pip install --upgrade pip")
        print("  2. Check your Python version: python --version (need 3.13+)")
        print("  3. See README.md for more help")
        return False

    print("\n✓ Dependencies installed successfully")
    return True


def run_test_embed() -> bool:
    """Run a small test embed to confirm sentence-transformers works."""
    print("\nRunning a test embed to confirm everything works...")
    print("(This triggers the ~420MB model download on first run)\n")

    # Write a tiny test wiki page
    test_dir = REPO_ROOT / "wiki" / "concepts"
    test_file = test_dir / "_setup-test.md"
    test_file.write_text(
        "---\ntitle: Setup Test\ntype: concept\ncreated: 2025-01-01\nupdated: 2025-01-01\nconfidence: high\nlang: en\n---\nThis page confirms the embedding tooling works.\n",
        encoding="utf-8"
    )

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "embed-wiki.py")],
        cwd=REPO_ROOT,
        capture_output=False,
    )

    # Clean up test page
    test_file.unlink(missing_ok=True)
    # Clean up embeddings (they'd just have the test entry)
    embeddings_file = REPO_ROOT / "meta" / "embeddings.json"
    embeddings_file.unlink(missing_ok=True)

    if result.returncode != 0:
        print("\n⚠  Test embed had issues. The brain will still work — semantic search may need troubleshooting.")
        print("Try: python tools/embed-wiki.py after adding your first wiki pages.")
        return False

    print("✓ Semantic search tooling confirmed working")
    return True


def main():
    print("\n" + "=" * 60)
    print("  Welcome to second-brain-kit setup")
    print("=" * 60)
    print()
    print("This takes about 5 minutes. It will configure your brain")
    print("and install the Python tools you'll need.")
    print()

    # Step 0 — Python version check
    check_python_version()

    # Step 1 — Name
    print("━" * 60)
    print("\n1. What should I call you?")
    print("   This appears in your Claude/AI sessions so it knows who you are.")
    print("   A nickname is totally fine — it doesn't have to be your real name.")
    name = ask("   Name or alias", default="User")

    # Step 2 — Goal
    print("\n━" * 60)
    print("\n2. What's the main thing you want to use this brain for?")
    print("   Examples:")
    print("   - Generate Instagram content ideas and scripts in my voice")
    print("   - Think through career decisions and reflect on patterns")
    print("   - Write and create with my authentic perspective")
    goal = ask("   Your goal", default="Build a personal knowledge base in my voice")

    # Step 3 — Language
    print("\n━" * 60)
    print("\n3. What language will you mainly use?")
    print("   The brain supports any language — English, Polish, Spanish, etc.")
    print("   You can also say 'bilingual' or 'English and Polish'.")
    language = ask("   Language", default="English")

    # Step 4 — Recordings privacy
    print("\n━" * 60)
    print("\n4. Should voice recordings be excluded from git?")
    print()
    print("   Recordings can be personal and are often large files.")
    print("   Excluding them means they stay on your machine and won't be pushed")
    print("   to GitHub even if you push the rest of the repo.")
    print()
    print("   Note: git doesn't mean push. You can keep everything local forever.")
    print("   But if you share the repo with anyone, recordings would be included.")
    print()
    recordings_answer = ask("   Exclude recordings from git? (Y/n)", default="Y")
    exclude_recordings = recordings_answer.strip().upper() not in ("N", "NO")

    # Apply configuration
    print("\n━" * 60)
    print("\nConfiguring your brain...\n")

    write_user_section(name, goal, language)
    write_starter_profile(name, goal)
    update_gitignore_for_recordings(exclude_recordings)

    # Download warning + pip install
    print_download_warning()
    input("  Press Enter to start installing dependencies (or Ctrl+C to skip)...")

    pip_ok = run_pip_install()

    if pip_ok:
        run_test_embed()

    # Done
    print("\n" + "=" * 60)
    print(f"  Setup complete, {name}!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("  1. Generate your interview questions:")
    print("     Open interview/README.md — it has a prompt template to paste")
    print("     into any LLM (Claude, ChatGPT, etc.) that generates questions")
    print("     personalized to you.")
    print()
    print("  2. Record your answers:")
    print("     Drop .m4a, .mp3, or .wav files into interview/recordings/")
    print()
    print("  3. Transcribe:")
    print("     Run /brain-transcribe in Claude Code")
    print()
    print("  4. Ingest:")
    print("     Run /brain-ingest — this builds your wiki")
    print()
    print("  5. Query:")
    print('     Run /brain-query "what do I actually think about X?"')
    print()


if __name__ == "__main__":
    main()
