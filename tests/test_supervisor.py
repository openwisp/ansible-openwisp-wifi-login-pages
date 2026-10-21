"""Exercise the role handlers with isolated Supervisor processes, without Docker."""

import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time

root = Path(__file__).resolve().parents[1]
env_bin = Path(sys.executable).parent

with tempfile.TemporaryDirectory(prefix="wlp38-", dir="/tmp") as directory:
    temp = Path(directory)
    (temp / "programs").mkdir()
    (temp / "bin").mkdir()
    config = temp / "supervisord.conf"
    config.write_text(
        f"""[unix_http_server]
file={temp}/supervisor.sock
[supervisord]
logfile={temp}/supervisord.log
pidfile={temp}/supervisord.pid
childlogdir={temp}
[rpcinterface:supervisor]
supervisor.rpcinterface_factory=supervisor.rpcinterface:make_main_rpcinterface
[supervisorctl]
serverurl=unix://{temp}/supervisor.sock
[include]
files={temp}/programs/*.conf
[program:unrelated]
command=/bin/sleep 600
startsecs=0
"""
    )
    worker = temp / "worker.py"
    worker.write_text(
        f"import time\nwith open({str(temp / 'starts')!r}, 'a') as stream: stream.write('started\\n')\ntime.sleep(600)\n"
    )
    wrapper = temp / "bin/supervisorctl"
    wrapper.write_text(
        "#!/bin/sh\n"
        f'printf \'%s\\n\' "$*" >> {shlex.quote(str(temp / "commands"))}\n'
        f'exec {shlex.quote(str(env_bin / "supervisorctl"))} -c {shlex.quote(str(config))} "$@"\n'
    )
    wrapper.chmod(0o755)
    environment = dict(
        os.environ,
        PATH=f"{temp}/bin:{env_bin}:" + os.environ["PATH"],
        ANSIBLE_LOCAL_TEMP=str(temp / "ansible-local"),
        ANSIBLE_REMOTE_TEMP=str(temp / "ansible-remote"),
        ANSIBLE_HOME=str(temp / "ansible-home"),
        ANSIBLE_NOCOLOR="1",
    )

    def ctl(*args):
        return subprocess.check_output(
            [str(wrapper), *args], text=True, timeout=15
        ).strip()

    playbook = temp / "test.yml"
    playbook.write_text(
        f"""---
- name: Test targeted handlers
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    ansible_become: false
    ansible_python_interpreter: {env_bin}/python
  handlers:
    - name: Import role handlers
      ansible.builtin.import_tasks: {root}/handlers/main.yml
  tasks:
    - name: Write application configuration
      ansible.builtin.copy:
        dest: {temp}/programs/wifi.conf
        mode: "0600"
        content: |
          [program:wifi_login_pages]
          command={env_bin}/python {worker}
          startsecs=0
          environment=REVISION="{{{{ revision }}}}"
      notify: Update WiFi Login Pages configuration
    - name: Represent an application build
      ansible.builtin.debug:
        msg: Application build
      changed_when: restart_app | bool
      notify: Restart WiFi Login Pages
"""
    )
    subprocess.run(
        [str(env_bin / "supervisord"), "-c", str(config)], check=True, timeout=15
    )
    results = []
    try:
        unrelated_pid = ctl("pid", "unrelated")
        assert int(unrelated_pid) > 0, "Unrelated process did not start"
        for label, revision, restart, expected_starts, expected_restarts in [
            ("first install", 1, True, 1, 0),
            ("application change", 1, True, 2, 1),
            ("configuration and application change", 2, True, 3, 1),
            ("configuration-only change", 3, False, 4, 1),
            ("no change", 3, False, 4, 1),
        ]:
            output = subprocess.run(
                [
                    str(env_bin / "ansible-playbook"),
                    "-i",
                    "localhost,",
                    str(playbook),
                    "-e",
                    json.dumps({"revision": revision, "restart_app": restart}),
                ],
                env=environment,
                capture_output=True,
                text=True,
                timeout=60,
            )
            if output.returncode:
                raise AssertionError(output.stdout + output.stderr)
            for attempt in range(30):
                starts = (
                    len((temp / "starts").read_text().splitlines())
                    if (temp / "starts").exists()
                    else 0
                )
                if starts >= expected_starts:
                    break
                time.sleep(0.1)
            assert starts == expected_starts, (
                label,
                starts,
                expected_starts,
                output.stdout,
            )
            assert ctl("pid", "unrelated") == unrelated_pid, (
                label,
                "unrelated process restarted",
            )
            assert int(ctl("pid", "wifi_login_pages")) > 0
            restarts = (
                (temp / "commands")
                .read_text()
                .splitlines()
                .count("restart wifi_login_pages")
            )
            assert restarts == expected_restarts, (
                label,
                "Unexpected number of explicit restarts",
                restarts,
                expected_restarts,
            )
            results.append(
                {"case": label, "total_starts": starts, "unrelated_pid_unchanged": True}
            )
        print(json.dumps(results, indent=2))
    finally:
        ctl("shutdown")
