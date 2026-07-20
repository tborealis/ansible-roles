"""Rule: a task name must not reference the task's own loop variable."""

from __future__ import annotations

import re

from ansiblelint.rules import AnsibleLintRule

LOOP_KEYWORDS = ("loop", "with_items", "with_dict", "with_fileglob",
                 "with_first_found", "with_together", "with_sequence",
                 "with_subelements", "with_nested", "with_random_choice",
                 "with_indexed_items", "with_ini", "with_lines", "with_list")


class LoopVarInNameRule(AnsibleLintRule):
    """Task name references its loop variable, which is undefined there."""

    id = "loop-var-in-name"
    shortdesc = "Task name must not reference the loop variable"
    description = (
        "Task names are templated once, before the loop runs, so the loop "
        "variable is always undefined there and Ansible warns "
        "\"'item' is undefined\". Use a static name and put per-item detail "
        "in loop_control.label instead."
    )
    severity = "HIGH"
    tags = ["idiom"]
    version_changed = "1.0.0"
    # Profile filtering unloads every rule whose id is not in the profile;
    # this marker is the only way a custom rule survives `profile: production`.
    unloadable = True

    def matchtask(self, task, file=None):
        name = task.get("name")
        if not name or "{{" not in name:
            return False
        raw = getattr(task, "raw_task", None) or task
        if not any(key in raw for key in LOOP_KEYWORDS):
            return False
        loop_var = "item"
        loop_control = raw.get("loop_control")
        if isinstance(loop_control, dict):
            loop_var = loop_control.get("loop_var", "item")
        pattern = re.compile(r"{{(?:(?!}}).)*\b%s\b(?:(?!}}).)*}}" % re.escape(loop_var))
        if pattern.search(name):
            return (f"Task name references loop variable '{loop_var}', which is "
                    "undefined when names are templated; use loop_control.label.")
        return False
