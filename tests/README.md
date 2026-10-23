# Browser stability checks

Install dependencies with `npm install`, then run `npm test`.
The tests use `/usr/bin/chromium`; set `CHROMIUM_PATH` to another Chromium executable if needed.
No live accounts or external pages are used. Camera and microphone inputs use Chromium fake devices.

Coverage:
- Existing IndexedDB v2 data upgrades to v3 without changing notes.
- Draft autosave and committed database writes.
- Real MediaRecorder video/audio data, intermediate chunks, finalization and interrupted-session recovery.
- Late camera permission results and note-switching during recording completion.
- Fifty thumbnail redraws release their URLs.
- An embedded generated MP4 plays/pauses through repeated viewer switches without full-buffer reads.
- Single/multiple exports, active share taps, downloads and preparation failures.
- Chunked legacy JSON backup preserves binary bytes and media duration.

These checks run in desktop Chromium. iPhone Safari, long device recordings, OS memory termination,
and native share sheets still need device testing. Recovery can preserve only chunks already committed
before termination; a recovered interrupted media container may require an external player.
