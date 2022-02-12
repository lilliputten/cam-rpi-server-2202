<!--
@changed 2022.02.12, 04:52
-->

# Changelog

- 2022.02.12, 04:52 -- Implemented simple socket.io tests. Relocated cdn files.
- 2022.02.12, 02:58 -- v.0.0.3: Restrucured server application (extracted several blueprint modules for different apis).
- 2022.02.08, 06:19 -- Device server shot creation method.
- 2022.02.08, 01:51 -- Fixed logger async (non-atomic) print issuesm server: starting only once (skip first initialization in debug mode, when app is initialized twice), templates: temporarily removed unused assets.
- 2022.02.07, 22:33 -- Local device server start scripts (via gunicorn, see `utils/rpi-start-server.sh`).
- 2022.02.07, 03:24 -- Readme venv instructions, disable basic auth in htaccess.
