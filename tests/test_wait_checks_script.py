"""wait.sh waits for every check and awaited human review on a pull request."""

import os
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/ba-wait-checks/scripts/wait.sh"

FAKE_GH = r"""#!/usr/bin/env bash
dir="$(dirname "$0")/.."
kind="$2"
count_file="$dir/$kind.count"
n=$(( $(cat "$count_file" 2>/dev/null || echo 0) + 1 ))
echo "$n" > "$count_file"
if [[ -f "$dir/$kind.err" ]]; then cat "$dir/$kind.err" >&2; exit 1; fi
file="$dir/$kind.$n"
while [[ ! -f "$file" && $n -gt 1 ]]; do n=$((n - 1)); file="$dir/$kind.$n"; done
cat "$file"
"""


def _run(
    tmp_path: Path, views: list[str], checks: list[str], **env: str
) -> subprocess.CompletedProcess[str]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    gh = bin_dir / "gh"
    gh.write_text(FAKE_GH, encoding="utf-8")
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    for index, body in enumerate(views, start=1):
        (tmp_path / f"view.{index}").write_text(body, encoding="utf-8")
    for index, body in enumerate(checks, start=1):
        (tmp_path / f"checks.{index}").write_text(body, encoding="utf-8")
    run_env = {
        **os.environ,
        "PATH": f"{bin_dir}:{os.environ['PATH']}",
        "WAIT_CHECKS_INTERVAL": "1",
        "WAIT_CHECKS_GRACE": "0",
        **env,
    }
    limit = run_env.pop("LIMIT", "10")
    sha = run_env.pop("SHA", "")
    return subprocess.run(  # noqa: S603 - fixed argv built in the test, no external input
        ["bash", str(SCRIPT), "7", limit, *([sha] if sha else [])],  # noqa: S607 - bash from PATH runs the repo's own script
        capture_output=True,
        text=True,
        env=run_env,
        timeout=60,
        check=False,
    )


OPEN = "OPEN||\n"
GREEN = "pass|https://ci/1|lint\npass|https://ci/2|review\n"


def test_all_checks_green_exits_zero(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], [GREEN])

    assert result.returncode == 0, result.stdout + result.stderr
    assert "lint" in result.stdout
    assert "review" in result.stdout


def test_red_check_exits_one(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], ["fail|https://ci/1|lint\npass|https://ci/2|review\n"])

    assert result.returncode == 1
    assert "lint" in result.stdout
    assert "fail" in result.stdout


def test_cancelled_check_counts_as_red(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], ["cancel|https://ci/1|lint\n"])

    assert result.returncode == 1


def test_waits_until_pending_check_finishes(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], ["pending|https://ci/1|lint\n", GREEN])

    assert result.returncode == 0
    assert int((tmp_path / "checks.count").read_text()) >= 2


def test_still_pending_at_limit_exits_two(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], ["pending|https://ci/1|lint\n"], LIMIT="0")

    assert result.returncode == 2
    assert "pending" in result.stdout


def test_no_checks_and_no_reviewer_exits_zero(tmp_path: Path) -> None:
    (tmp_path / "checks.err").write_text("no checks reported on the 'x' branch\n")

    result = _run(tmp_path, [OPEN], [""])

    assert result.returncode == 0
    assert "nothing to wait for" in result.stdout


def test_no_checks_within_grace_keeps_waiting(tmp_path: Path) -> None:
    (tmp_path / "checks.err").write_text("no checks reported on the 'x' branch\n")

    result = _run(tmp_path, [OPEN], [""], LIMIT="0", WAIT_CHECKS_GRACE="100")

    assert result.returncode == 2


def test_requested_reviewer_keeps_waiting(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|REVIEW_REQUIRED|alice\n"], [GREEN], LIMIT="0")

    assert result.returncode == 2
    assert "alice" in result.stdout


def test_required_review_without_person_keeps_waiting(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|REVIEW_REQUIRED|\n"], [GREEN], LIMIT="0")

    assert result.returncode == 2


def test_approval_ends_wait_on_human(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|REVIEW_REQUIRED|alice\n", "OPEN|APPROVED|\n"], [GREEN])

    assert result.returncode == 0
    assert "approved" in result.stdout


def test_changes_requested_exits_one(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|CHANGES_REQUESTED|\n"], [GREEN])

    assert result.returncode == 1


def test_re_requested_review_after_changes_keeps_waiting(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|CHANGES_REQUESTED|alice\n"], [GREEN], LIMIT="0")

    assert result.returncode == 2


def test_red_check_stops_waiting_for_human(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|REVIEW_REQUIRED|alice\n"], ["fail|https://ci/1|lint\n"])

    assert result.returncode == 1


def test_merged_pr_exits_zero(tmp_path: Path) -> None:
    result = _run(tmp_path, ["MERGED||\n"], [GREEN])

    assert result.returncode == 0
    assert "result: merged" in result.stdout


def test_gh_failure_exits_three(tmp_path: Path) -> None:
    (tmp_path / "view.err").write_text("gh: not logged in\n")

    result = _run(tmp_path, [OPEN], [GREEN])

    assert result.returncode == 3
    assert "not logged in" in result.stderr


def test_changes_requested_without_required_review_exits_one(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN|||bob|abc\n"], [GREEN])

    assert result.returncode == 1
    assert "bob" in result.stdout


def test_waits_until_head_is_the_pushed_commit(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN||||old\n", "OPEN||||new\n"], [GREEN], SHA="new")

    assert result.returncode == 0
    assert int((tmp_path / "view.count").read_text()) >= 2


def test_old_head_with_red_checks_keeps_waiting(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN||||old\n"], ["fail|https://ci/1|lint\n"], SHA="new", LIMIT="0")

    assert result.returncode == 2
    assert "old" in result.stdout


def test_pipe_in_check_name_cannot_turn_a_failure_green(tmp_path: Path) -> None:
    result = _run(tmp_path, [OPEN], ["fail|https://ci/1|lint|pass\n"])

    assert result.returncode == 1


def test_merge_conflict_is_red_not_missing_ci(tmp_path: Path) -> None:
    (tmp_path / "checks.err").write_text("no checks reported on the 'x' branch\n")

    result = _run(tmp_path, ["OPEN|||||DIRTY\n"], [""])

    assert result.returncode == 1
    assert "merge conflict" in result.stdout


def test_conflict_on_old_head_keeps_waiting_for_pushed_commit(tmp_path: Path) -> None:
    result = _run(tmp_path, ["OPEN||||old|DIRTY\n"], [GREEN], SHA="new", LIMIT="0")

    assert result.returncode == 2
