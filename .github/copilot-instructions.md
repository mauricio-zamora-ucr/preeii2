<!-- Copilot / AI agent instructions for the PreEII repository -->
# Copilot instructions — PreEII

Purpose: give an AI coding agent the minimal, high-value facts to be productive in this repo.

- **Start here (entry points):** `main.py` (calls `MenuController`) and
  `src/presentation/console/menu_controller.py` (menu flow and major orchestration).

- **Big picture architecture:** the project mixes a legacy procedural layer
  (top-level modules like `funciones_*.py`) and a refactored package under `src/`.
  The `src/` tree follows a layered approach: `presentation` -> `application` ->
  `infrastructure` -> `shared`. Example: menu -> `ExpedienteService` ->
  `FileRepository` -> `ExcelWriter`.

- **Primary data flow (common task):**
  1. User triggers download or processing via `MenuController`.
  2. `WebScrapingService` (in `src/application/services`) downloads raw files into `expediente/` (.edf/.sdf).
  3. `FileRepository` (`src/infrastructure/repositories/file_repository.py`) reads those files with `leer_historial()` and `leer_informacion_estudiante()`.
  4. `ExpedienteService` (`src/application/services/expediente_service.py`) converts history → domain `Expediente` and computes analyses.
  5. `ExcelWriter` (adapter in `src/infrastructure/adapters/excel_writer.py`) produces `.xlsx` into `salida/` (7 specialized sheets).

- **Where to look for common logic:**
  - File I/O and encoding: `funciones_io.py` (legacy) and `src/infrastructure/repositories/file_repository.py` (refactor).
  - Processing logic: `funciones_procesamiento_expediente.py` (legacy) and `src/application/services/expediente_service.py`.
  - Excel generation: `funciones_xlsxwriter.py` (legacy) and `src/infrastructure/adapters/excel_writer.py`.
  - Web scraping / download: `funciones_web_scraping.py` (legacy) and `src/application/services/web_scraping_service.py`.

- **Project-specific conventions & patterns:**
  - Source identifiers and functions are often in Spanish (e.g., `carne`, `historial`, `expediente`).
  - Tests live at repo root with `test_*.py` filenames. Use `pytest` to run them.
  - There are two config layers: an older `config.py` at the repo root and a refactored
    `src/shared/config/settings.py` referenced by `MenuController` via `app_config`.
    Check both when changing defaults or auth handling.
  - Legacy modules (`funciones_*.py`) are still used by tests and CLI helpers — prefer updating
    `src/` services but verify backward-compatible behavior in the legacy scripts.

- **Important files & directories to reference in PRs/edits:**
  - `main.py` — app entry (for integration/run changes)
  - `src/presentation/console/menu_controller.py` — primary orchestration and CLI flows
  - `src/application/services/` — core business services (`expediente_service.py`, `web_scraping_service.py`, `memory_reader_service.py`)
  - `src/infrastructure/repositories/file_repository.py` — file access, encoding handling, output paths
  - `src/infrastructure/adapters/excel_writer.py` — Excel sheet layout and formatting
  - `expediente/` — sample raw data (.edf/.sdf used by tests), `salida/` — generated `.xlsx`
  - `REFACTORING_SUMMARY.md` — map between legacy files and refactored locations (useful when editing)

- **How to run / debug locally:**
  - Install deps: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
  - Run CLI: `python main.py` (interactive menu). For focused runs call services directly in a REPL.
  - Run tests: `pytest -q` or `pytest tests/specific_test.py`.
  - To reproduce encoding issues, use test data in `expediente/` (tests reference `.edf`/`.sdf`).

- **Small, high-value edits an AI can safely propose:**
  - Replace duplicated encoding logic by delegating to `FileRepository` helpers.
  - Add unit tests around `ExpedienteService` for edge-case histories (there are many `test_*.py` examples).
  - When touching config, update both `config.py` and `src/shared/config/settings.py` or add a migration comment.

- **What *not* to change without review:**
  - CLI user-visible strings (Spanish messages) — these are intentionally localized.
  - Excel sheet layout unless testing confirms identical output (several downstream analyses depend on exact sheet names).

Examples (use these code snippets as jump-starts):
  - Read a student history: `from src.infrastructure.repositories.file_repository import FileRepository; FileRepository().leer_historial(carne)`
  - Trigger Excel generation for an `Expediente` instance: `from src.infrastructure.adapters.excel_writer import ExcelWriter; ExcelWriter().generar_expediente(expediente, salida_path)`

If anything here is unclear or you'd like me to expand examples (e.g., list public methods for `ExpedienteService`), tell me which area to document next.
