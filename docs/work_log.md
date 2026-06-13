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

---
## June 11, 2026

**5:30 p.m.** Implementing database view.

**7:00 p.m.** Ended up finding out that the database.py and create_tables.sql files didn't really work at all, so I had to fix a lot of bugs and add things that were lacking for them to actually do something.

database.py 144 lines
create_tables.sql 115 lines

---
## June 12, 2026

**11:15 a.m.** Designing backend.

**11:45 a.m.** Implementing backend.

**1:40 p.m.** Finished. `data_backend.py` 222 lines.

**1:50 p.m.** Implementing frontend.

**2:30 p.m.** Basic flask skeleton finished. `main.py` 13 lines, `backend.py` 75 lines. Now implementating templates.

**4:30 p.m.** Implementing CSS before going into the scoring.

**7:50 p.m.** CSS Finished. Break.

**8:20 p.m.** Implementing the scoring system.

**8:45 p.m.** Break.

**9:10 p.m.** Continue.

**1:10 p.m.** Functionality complete. Now refine the GUI.

**2:00 p.m.** Finished.


| **File**          | **Lines** |
| ----------------- | --------- |
| preload.py        | 84        |
| ingest.py         | 326       |
| normalize.py      | 243       |
| enrich.py         | 198       |
| database.py       | 144       |
| create_tables.sql | 115       |
| master.py         | 117       |
| backend_data.py   | 264       |
| backend_feed.py   | 123       |
| main.py           | 19        |
| login.html        | 40        |
| artists.html      | 52        |
| artist.html       | 84        |
| album.html        | 193       |
| global.css        | 50        |
| artists.css       | 44        |
| artist.css        | 124       |
| album.css         | 215       |
| **Total**         | 2413      |
