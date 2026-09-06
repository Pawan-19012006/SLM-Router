# SLM Router

Local AI Request Classification & Intelligent 3-Way Dispatch.

## What It Does

SLM Router classifies incoming user queries using an on-device Small Language Model (SLM) and automatically routes them to the optimal execution path:

```
                      User Query
                          ↓
              Qwen2.5-1.5B V3 Classifier
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
      LOCAL            COMMAND            CLOUD
        ↓                 ↓                 ↓
    Local SLM          Local SLM        Gemini API
 (Direct Answer)  (Dynamic Simulated  (Complex Task
                     Confirmation)      Execution)
```

- **LOCAL**: Answered directly on-device by the local SLM.
- **COMMAND**: Action/device intents are detected and confirmed dynamically by the local SLM using a dedicated command confirmation prompt. **Note:** All command execution is currently simulated and does not perform operating system or hardware changes.
- **CLOUD**: Heavy, open-ended, or complex tasks are offloaded to Google Gemini via the official `google-genai` SDK.

---

## Requirements

- **Python**: `>= 3.11`
- **Package Manager**: [`uv`](https://docs.astral.sh/uv/)
- **Network**: Internet connection for initial Hugging Face model weight download (`Qwen/Qwen2.5-1.5B-Instruct`, ~3.1 GB) and Google Gemini API access.
- **Gemini API Key**: Required for live cloud routing (a mock fallback mode is also supported).

---

## Installation

Clone the repository and install all dependencies using `uv`:

```bash
git clone <repository-url>
cd SLM-Router
uv sync
```

---

## Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your-gemini-api-key-here
CLOUD_MODEL=gemini-3.6-flash
CLOUD_MODE=live
```

### Configuration Options:
- `GEMINI_API_KEY`: Your Google AI Studio API key. If left blank, the router automatically falls back to safe **Mock Mode** without raising errors.
- `CLOUD_MODEL`: Target Gemini model (default: `gemini-3.6-flash`).
- `CLOUD_MODE`: Set to `live` for real API calls, or `mock` for simulated cloud dispatch.

> **Security Note**: Never commit your `.env` file to version control. It is ignored by `.gitignore`.

---

## Run the Application

Launch the clean Streamlit web application:

```bash
uv run streamlit run app.py
```

The application interface allows you to enter any query, view the real-time routing decision, and read the generated response.

---

## Architecture

1. **Classification Layer (`ClassifierV3`)**:
   - Uses `Qwen/Qwen2.5-1.5B-Instruct` with a structured system prompt.
   - Categorizes queries strictly into `LOCAL`, `COMMAND`, or `CLOUD`.
2. **Execution Layer (`Router`)**:
   - Dispatches to the appropriate handler with millisecond execution telemetry.
   - Reuses a single loaded SLM instance in memory across classification, local generation, and command confirmation to minimize RAM footprint.
3. **Cloud Layer (`CloudHandler`)**:
   - Communicates with Google Gemini via `google-genai`.
   - Provides resilient error sanitation (API keys are never logged or exposed in error messages or UI).

---

## Hardware Portability & Device Selection

The local SLM automatically detects and selects compute hardware at runtime with the following priority:

1. **NVIDIA CUDA**: Selected if `torch.cuda.is_available()`.
2. **Apple Silicon (MPS)**: Selected if `torch.backends.mps.is_available()`.
3. **CPU Fallback**: Selected on x86_64, Windows, or systems without GPU acceleration.

### Platform Support:
- **macOS (Apple Silicon / Intel)**: Supported with native Metal Performance Shaders (MPS) or CPU.
- **Linux (x86_64 / ARM64)**: Supported with CUDA or CPU.
- **Windows (x86_64)**: Supported with CUDA or CPU.
- **Raspberry Pi (ARM64)**: Intended future target using CPU inference. *Note: Raspberry Pi deployment is architecturally prepared via standard CPU fallback, but has not yet been physically tested on Pi hardware.*

---

## Running Tests

Run the unit and integration test suite:

```bash
uv run python -m unittest src/slm_router/tests/test_router.py src/slm_router/tests/test_phase3.py
```
