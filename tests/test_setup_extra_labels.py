"""ba-setup offers to delete repo labels the config does not define."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SETUP_SKILL = REPO_ROOT / "skills/ba-setup/SKILL.md"
README = REPO_ROOT / "README.md"
SECTION = re.compile(r"^## Etykiety spoza konfiguracji\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
STEPS = re.compile(r"^## Kroki\n(.*?)(?=^## )", re.MULTILINE | re.DOTALL)


def _text() -> str:
    return SETUP_SKILL.read_text(encoding="utf-8")


def _section() -> str:
    match = SECTION.search(_text())
    assert match, "ba-setup has no '## Etykiety spoza konfiguracji' section"
    return match.group(1)


def _positions(text: str, options: list[str]) -> list[int]:
    return [text.find(f"„{option}”") for option in options]


def test_setup_has_extra_labels_step_before_commit() -> None:
    steps = STEPS.search(_text())
    assert steps, "ba-setup has no '## Kroki' section"
    body = steps.group(1)

    assert re.search(r"^7\. \*\*Etykiety spoza konfiguracji\.\*\*", body, re.MULTILINE)
    assert re.search(r"^8\. \*\*Commit\.\*\*", body, re.MULTILINE)
    assert "§ Etykiety spoza konfiguracji" in body


def test_extra_labels_section_counts_usage_and_deletes() -> None:
    section = _section()

    for phrase in [
        "gh api graphql --paginate",
        "pullRequests(states: [CLOSED, MERGED])",
        "gh label delete --yes -- '<nazwa>'",
        "nic do skasowania",
    ]:
        assert phrase in section, f"missing: {phrase}"


def test_extra_labels_section_asks_with_options_in_order() -> None:
    section = _section()
    first = _positions(section, ["zostaw wszystkie", "wybierz", "skasuj wszystkie"])
    second = _positions(section, ["zostaw te", "skasuj też te"])

    assert -1 not in first, f"first question options missing: {first}"
    assert first == sorted(first), "recommended option 'zostaw wszystkie' must come first"
    assert -1 not in second, f"second confirmation options missing: {second}"
    assert second == sorted(second), "recommended option 'zostaw te' must come first"


def test_setup_no_longer_forbids_deleting_every_label() -> None:
    text = _text()

    assert "nie zmieniasz i nie kasujesz" not in text
    assert "Nie zmienia ani nie kasuje istniejących etykiet" not in text
    assert "Nie kasuje etykiet z konfiguracji ani bez zgody operatora" in text


def test_extra_labels_section_keeps_safeguards() -> None:
    section = _section()

    for phrase in [
        "Etykieta z konfiguracji nigdy nie trafia na listę",
        "Tego nie da się cofnąć",
        "Licznik nie obejmuje dyskusji",
        "nie zatrzymuje reszty",
        "dowodem użycia według pytania 8",
        "Lista pokazuje plik trafienia",
    ]:
        assert phrase in section, f"missing safeguard: {phrase}"


def test_extra_labels_warning_precedes_first_question_answer() -> None:
    section = _section()
    warning = section.find("Licznik nie obejmuje dyskusji")

    assert -1 < section.find("„skasuj wszystkie”") < warning < section.find("„zostaw te”")


def test_extra_labels_step_skips_without_config_label_tables() -> None:
    section = _section()

    assert "0 etykiet z konfiguracji" in section
    assert "Krok pomijasz" in section


def test_setup_turn_ending_steps_follow_renumbering() -> None:
    text = _text()

    assert "kończy turę pytaniem w krokach 3, 5 i 8" in text
    assert "w kroku 7 tylko przy etykietach spoza konfiguracji" in text


def test_setup_report_lists_deleted_and_kept_labels() -> None:
    assert "etykiety spoza konfiguracji skasowane i zostawione" in _text()


def test_readme_mentions_label_deletion() -> None:
    row = next(
        line
        for line in README.read_text(encoding="utf-8").splitlines()
        if line.startswith("| [`ba-setup`]")
    )

    assert "etykiety spoza konfiguracji" in row
