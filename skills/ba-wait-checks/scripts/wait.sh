#!/usr/bin/env bash
# Waits until every check and every awaited human review on a GitHub pull request has a result.
# Usage: wait.sh <pr> [limit_s] [sha]
#   sha: the commit just pushed; until the pull request head is this commit, the script keeps waiting
# Exit codes:
#   0  finished and green, also when there is nothing to wait for
#   1  finished with something red: a failed or cancelled check, changes requested, or a merge conflict
#   2  still pending when limit_s ran out; run the script again
#   3  gh failed: no session, no network, no such pull request
set -u

pr="${1:?usage: wait.sh <pr> [limit_s] [sha]}"
limit="${2:-540}"
expected_sha="${3:-}"
interval="${WAIT_CHECKS_INTERVAL:-30}"
grace="${WAIT_CHECKS_GRACE:-120}"
start=$SECONDS
err_file=$(mktemp)
trap 'rm -f "$err_file"' EXIT

fail() {
  echo "ERROR: $1" >&2
  exit 3
}

while :; do
  elapsed=$((SECONDS - start))

  pr_line=$(gh pr view "$pr" --json state,reviewDecision,reviewRequests,latestReviews,headRefOid,mergeStateStatus --jq \
    '[.state, (.reviewDecision // ""),
      ([.reviewRequests[] | .login // .slug // .name] | join(" ")),
      ([.latestReviews[] | select(.state == "CHANGES_REQUESTED") | .author.login] | join(" ")),
      .headRefOid, .mergeStateStatus] | join("|")' \
    2>"$err_file") || fail "gh pr view: $(cat "$err_file")"
  IFS='|' read -r state decision requested changes_by head merge_state <<<"$pr_line"

  if [[ "$state" == "MERGED" || "$state" == "CLOSED" ]]; then
    echo "PR #$pr: $state"
    echo "result: ${state,,}"
    exit 0
  fi

  if ! checks=$(gh pr checks "$pr" --json name,bucket,link --jq \
    '.[] | [.bucket, .link, .name] | join("|")' 2>"$err_file"); then
    grep -q "no checks reported" "$err_file" || fail "gh pr checks: $(cat "$err_file")"
    checks=""
  fi

  report=""
  checks_pending=0
  red=0
  # The name goes last: read gives the last variable the rest of the line, so a '|' in a name cannot shift fields.
  while IFS='|' read -r bucket link name; do
    [[ -z "$name" ]] && continue
    case "$bucket" in
      pending) checks_pending=1 ;;
      fail | cancel) red=1 ;;
    esac
    report+="check: $name — $bucket — $link"$'\n'
  done <<<"$checks"

  stale=0
  if [[ -n "$expected_sha" && "$head" != "$expected_sha" ]]; then
    stale=1
    # GitHub moves the pull request head after a push with a delay; checks shown now belong to an older commit.
    report="head: $head is not $expected_sha yet"$'\n'
    checks_pending=1
    red=0
  fi

  if [[ "$merge_state" == "DIRTY" ]] && ((!stale)); then
    # GitHub runs no pull_request workflows on a conflicting pull request, so missing checks are not "no CI".
    echo "PR #$pr: merge conflict with the base branch; checks do not run until it is resolved"
    printf '%s' "$report"
    echo "result: red"
    exit 1
  fi

  no_checks=0
  if [[ -z "$report" ]]; then
    if ((elapsed < grace)); then checks_pending=1; else no_checks=1; fi
  fi

  human=""
  human_pending=0
  if [[ -n "$requested" ]]; then
    human="waiting for review from $requested"
    human_pending=1
  elif [[ "$decision" == "CHANGES_REQUESTED" || -n "$changes_by" ]]; then
    # Without a required review reviewDecision stays empty, so latestReviews carries the request.
    human="changes requested${changes_by:+ by $changes_by}"
    red=1
  elif [[ "$decision" == "REVIEW_REQUIRED" ]]; then
    human="approval required, nobody requested"
    human_pending=1
  elif [[ "$decision" == "APPROVED" ]]; then
    human="approved"
  fi

  finished=0
  if ((!checks_pending)) && { ((!human_pending)) || ((red)); }; then finished=1; fi

  if ((finished)) || ((elapsed + interval > limit)); then
    echo "PR #$pr after ${elapsed}s"
    printf '%s' "$report"
    if ((no_checks)) && [[ -z "$human" ]]; then
      echo "nothing to wait for: no checks and no reviewer"
    elif ((no_checks)); then
      echo "checks: none reported"
    fi
    [[ -n "$human" ]] && echo "human review: $human"
    if ((!finished)); then
      echo "result: pending"
      exit 2
    fi
    if ((red)); then
      echo "result: red"
      exit 1
    fi
    echo "result: green"
    exit 0
  fi

  sleep "$interval"
done
