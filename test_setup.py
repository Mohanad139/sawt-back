"""Pre-flight check — run before starting the agent to verify the environment."""

from __future__ import annotations

import os
import sys


def check_python_version() -> bool:
    v = sys.version_info
    ok = v >= (3, 9)
    status = f"Python {v.major}.{v.minor}.{v.micro}"
    print(f"  {status}" if ok else f"  {status} — need 3.9+")
    return ok


def check_dependencies() -> bool:
    packages = {
        "livekit.agents": "livekit-agents",
        "livekit.plugins.deepgram": "livekit-plugins-deepgram",
        "livekit.plugins.openai": "livekit-plugins-openai",
        "livekit.plugins.silero": "livekit-plugins-silero",
        "dotenv": "python-dotenv",
    }
    all_ok = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  {package}")
        except ImportError:
            print(f"  {package} — MISSING (pip install {package})")
            all_ok = False
    return all_ok


def check_env_variables() -> bool:
    from dotenv import load_dotenv

    load_dotenv()

    required = [
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY",
        "LIVEKIT_API_SECRET",
        "DEEPGRAM_API_KEY",
        "OPENAI_API_KEY",
    ]
    all_ok = True
    for var in required:
        value = os.getenv(var)
        if value and not value.startswith("your_"):
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"  {var} = {masked}")
        else:
            print(f"  {var} — NOT SET")
            all_ok = False
    return all_ok


def main() -> None:
    print("\n=== Sawt Voice Agent — Pre-flight Check ===\n")
    results: dict[str, bool] = {}

    print("[1/3] Python Version")
    results["python"] = check_python_version()

    print("\n[2/3] Dependencies")
    results["deps"] = check_dependencies()

    print("\n[3/3] Environment Variables")
    results["env"] = check_env_variables()

    print("\n" + "=" * 44)
    if all(results.values()):
        print("All checks passed. Run: python -m sawt.agent dev")
    else:
        failed = [k for k, v in results.items() if not v]
        print(f"Issues found in: {', '.join(failed)}")
        print("Fix the above issues and re-run this script.")
    print()


if __name__ == "__main__":
    main()
