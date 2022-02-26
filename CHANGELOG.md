<!--
@changed 2022.02.27, 02:45
-->

# Changelog

- 2022.02.27, 02:45 -- RecordsStorage using TinyDB (fully worked code & tests).
- 2022.02.26, 05:31 -- Using TinyDB for data engine in `RecordsStorage` (in progress: basic methods and tests are ready).
- 2022.02.24, 00:55 -- v.0.0.5: Moved `lib` to `core/lib` scope (extract to shared submodule in future). Using pylint as project-wide linter (fixed all linter issues).
- 2022.02.23, 00:24 -- RecordsStorage: remove outdated records during findng (in `processRecords`), added metod for rorced remove of outdated records (`removeOutdatedRecords`).
- 2022.02.22, 02:30 -- RecordsStorage, Record: Basic records and records storage routines and tests.
- 2022.02.21, 23:06 -- Test support utilities (`getTrace`). Restuctured utils module.
- 2022.02.15, 06:12 -- v.0.0.4: Created automatic tests & linters for python code.
- 2022.02.15, 03:53 -- Helper modules moved to lib folder.
- 2022.02.14, 04:45 -- Experimantal sessions support.
- 2022.02.12, 04:52 -- Implemented simple socket.io tests. Relocated cdn files.
- 2022.02.12, 02:58 -- v.0.0.3: Restrucured server application (extracted several blueprint modules for different apis).
- 2022.02.08, 06:19 -- Device server shot creation method.
- 2022.02.08, 01:51 -- Fixed logger async (non-atomic) print issuesm server: starting only once (skip first initialization in debug mode, when app is initialized twice), templates: temporarily removed unused assets.
- 2022.02.07, 22:33 -- Local device server start scripts (via gunicorn, see `utils/rpi-start-server.sh`).
- 2022.02.07, 03:24 -- Readme venv instructions, disable basic auth in htaccess.
