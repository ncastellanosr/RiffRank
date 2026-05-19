# Work Log

---

## April 24, 2026

**8:00 p.m.** Implementing `spotify_preload.py`. Need to remember the uses of `.venv` and logging. Might take longer than it should.

**8:30 p.m.** First working draft finished (35 lines, counting blank lines and spaced braces/parentheses formatting). Moving on to improvements.

**9:00 p.m.** Finished the code (72 lines, counting comments, blank lines and spaced braces/parentheses formatting). Break — guitar.

**10:00 p.m.** Beginning `spotify_ingestion.py`.

**11:00 p.m.** Coffee break.

**11:13 p.m.** Back.

---

## April 25, 2026

**2:00 a.m.** Finished the code (285 lines, counting comments, blank lines and spaced braces/parentheses formatting).

**3:00 p.m.** Beginning snapshot system docs.

**3:40 p.m.** Finished snapshot system docs. Almost falling asleep. Nap.

**8:40 p.m.** Beginning pseudo-orchestrator implementation (snapshot system).

**11:00 p.m.** All files looking good. Break.

| File | Lines |
|---|---|
| `preload.py` | 65 |
| `ingestion.py` | 286 |
| `master.py` | 64 |

---

## April 26, 2026

**12:10 a.m.** Beginning transformation layers.

**2:00 a.m.** Normalization layer finished.

| File | Lines |
|---|---|
| `master.py` | 76 |
| `normalize.py` | 116 |

**3:00 p.m.** Beginning transformation layer docs.

**3:40 p.m.** Break.

**4:00 p.m.** Beginning enrichment layer implementation.

**6:00 p.m.** Enrichment layer finished. Break — eating and guitar.

| File | Lines |
|---|---|
| `enrichment.py` | 153 |
| `master.py` | 84 |

**10:00 p.m.** Beginning database layer implementation.

---

## April 27, 2026

**12:45 a.m.** Finished.

| File | Lines |
|---|---|
| `database.py` | 101 |
| `master.py` | 92 |

---

## May 8, 2026

**7:30 p.m.** Beginning better resumability implementation via `status.json`.

**7:50 p.m.** Done, but suspect normalization lacks individual distinction for skipping or adding artists — it likely runs a single batch for all artists found rather than handling them individually. Changes were small and simple; took longer than expected due to not remembering the code well and being tired. Pending: improve error handling (needs error code implementation).

---

## May 10, 2026

**11:20 a.m.** Implementing better error handling in ingestion.

**2:30 p.m.** Finished. `ingestion.py` now at 318 lines.

**6:30 p.m.** Refactoring `normalize.py`, improving resumability.

**8:30 p.m.** Finished. `normalize.py` now at 243 lines.

---

## May 18, 2026

**6:40 p.m.** Refactoring `enrichment.py`, improving resumability.

**9:00 p.m.** Finished. `enrichment.py` now at  198 lines, `master.py` now at 117lines.

**9:40 p.m.** Adding exception handling in `database.py` and reviewing potential changes.

**9:45 p.m.** No potential changes found. `database.py` now at 113 lines.

**10:25 p.m.** Punctual minor adjustments to `preload.py`. `preload.py` now at 84 lines.

**11:35 p.m.** Writting `readme.md`.

**12:10 a.m.** *(May 19)* Finished.