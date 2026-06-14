# iPhone → Mac Auto-Transcribe Pipeline

Hands-free recording: speak on iPhone → file syncs to Mac via iCloud → Mac transcribes automatically → transcript lands in holding folder for brain-ingest.

No terminal commands after setup. No manual transcription step.

---

## What you need

- iPhone with Shortcuts app
- Mac with Apple Silicon (M1+) — required for mlx_whisper GPU acceleration
- [ai-toolkit](https://github.com/your-repo/ai-toolkit) cloned to `~/ai-toolkit`
- `mlx_whisper` installed: `pip install mlx_whisper`
- `ffmpeg` installed: `brew install ffmpeg`

---

## How it works

```
iPhone Shortcut → records audio → saves to iCloud Drive/voice-notes/<subfolder>/
Mac VoiceWatcher daemon detects new file (via launchd WatchPaths)
  → mlx_whisper transcribes (Polish or your language, GPU-accelerated)
  → .txt appears next to the audio in iCloud
  → .txt moved to <brain-repo>/raw/transcripts/YYYY-MM-DD/ (date folder created if needed)
  → .m4a archived to done/ subfolder
When ready → run /brain-ingest to process transcripts from raw/transcripts/
```

---

## Step 1 — iPhone Shortcut

Create one shortcut per destination (second-brain, project notes, etc.):

1. Open **Shortcuts** app on iPhone
2. Create new shortcut → add actions:
   - **Record Audio** → Start Recording: **Immediately** (tap to stop recording)
   - **Save File** → Location: **iCloud Drive** → `voice-notes/second-brain/` → Ask where to save: **OFF**
3. Name the shortcut **"Second Brain Voice Note"** (or per-destination variant, e.g. "Together Games Voice Note")
4. Add to Home Screen for one-tap access

To add more destinations (e.g. project notes): duplicate the shortcut, change the save folder.

---

## Step 2 — VoiceWatcher daemon on Mac

The daemon lives in `~/ai-toolkit/tools/voice-watcher/`. Full details in its README:
```
~/ai-toolkit/tools/voice-watcher/README.md
```

Quick setup:

```bash
# 1. Make script executable
chmod +x ~/ai-toolkit/tools/voice-watcher/transcribe_new.sh

# 2. Build the .app wrapper (needed for Full Disk Access grant)
osacompile -o ~/ai-toolkit/tools/voice-watcher/VoiceWatcher.app \
           ~/ai-toolkit/tools/voice-watcher/VoiceWatcher.applescript

# 3. Grant Full Disk Access to VoiceWatcher.app
#    System Settings → Privacy & Security → Full Disk Access → + →
#    navigate to ~/ai-toolkit/tools/voice-watcher/VoiceWatcher.app → toggle ON
#
#    WHY: iCloud Drive requires Full Disk Access. VoiceWatcher.app is a
#    compiled AppleScript binary (not Python/bash), so granting FDA to it
#    is narrow and safe — it only runs the one transcription script.

# 4. Deploy and start the launchd agent
cp ~/ai-toolkit/tools/voice-watcher/com.life.voicewatcher.plist \
   ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.life.voicewatcher.plist
```

The daemon starts on login and fires whenever a new `.m4a` appears in any subfolder of `iCloud Drive/voice-notes/`.

---

## Step 3 — Verify it works

```bash
# Check daemon is running
launchctl list | grep voicewatcher

# Watch live transcription
tail -f ~/Library/Logs/voice-watcher.log
```

Drop a test recording via iPhone Shortcut and watch the log.

---

## Step 4 — Trigger brain-ingest

When transcripts have accumulated in `raw/transcripts/`, run brain-ingest from your second-brain repo in Claude Code:

```
/brain-ingest
```

The skill reads transcripts from `raw/transcripts/` (organized by date subfolder), synthesizes them into wiki pages, and updates index, hot cache, and log. You can tell it "ingest today's transcripts" or "ingest the last 4 days" — it filters by folder name.

---

## Upgrading to fully automatic (optional)

To trigger brain-ingest automatically after every transcription, add to `~/ai-toolkit/tools/voice-watcher/transcribe_new.sh` after the `mv "$transcript"` line:

```bash
log "Triggering brain-ingest"
cd "$HOME/<your-brain-repo>" && claude -p "brain-ingest" >> "$LOG" 2>&1
log "brain-ingest complete"
```

Replace `<your-brain-repo>` with the path to your second-brain repo (e.g. `~/life`).

---

## Language

The daemon transcribes in Polish (`--language pl`). To change, edit `transcribe_new.sh` and update the `--language` flag:

```bash
# e.g. for English:
--language en
# or let Whisper auto-detect:
# remove --language entirely
```
