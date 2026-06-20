#!/usr/bin/env python3
"""Run a slice of the evaluation test against a testing environment.

The test cases under ``testcases/`` are the source of truth; the environments
under ``environments/`` hold a runnable implementation with an *empty* ``tests/``
folder. This script copies a test "part" into the right environment's tests
folder and invokes ``pytest`` there.

Examples
--------
    python test_driver.py --phase dev  --tech nag                          # all variants
    python test_driver.py --phase dev  --tech nag   --category none        # all parts
    python test_driver.py --phase evol --tech nag   --part part5           # only part5 of all variants

``--part`` is optional: omit it to run every part in the category sequentially.
``--category`` is optional: omit it to run every variant in the category sequentially.

Run ``python test_driver.py --list`` to see what privacy test parts are available.
"""
import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

_STATUS_RE = re.compile(r"^(?P<node>\S.*?)\s+(?P<status>PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\b")
_PCT_RE = re.compile(r"\[\s*(\d+)%\]\s*$")
_COLLECTED_RE = re.compile(r"collected (\d+) item")

ROOT = Path(__file__).resolve().parent
TESTCASES = ROOT / "testcases"
ENVIRONMENTS = ROOT / "environments"
SOLUTIONS = ROOT.parent / "solutions"
TEMPLATES = ROOT.parent / "templates"

PHASES = {"dev": "Development", "evol": "Evolution"}
TECHS = {
    "flask": {"Development": "Flask", "Evolution": "Flask"},
    "nag": {"Development": "NuActionGUI", "Evolution": "NuActionGUI"},
}
CATEGORIES = {
    "none": "privacy/none",
    "basic": "privacy/basic",
    "complex": "privacy/complex",
}
PRIVACY_VARIANTS = ("none", "basic", "complex")

def env_tests_dir(env_dir: Path, tech: str) -> Path:
    if tech == "flask":
        return env_dir / "tests"
    return env_dir / "project" / "EventPlatformNAG" / "tests"

def resolve(phase: str, tech: str):
    phase_dir = PHASES[phase]
    tech_dir = TECHS[tech][phase_dir]         
    corpus = TESTCASES / phase_dir / tech_dir
    env = ENVIRONMENTS / phase_dir / tech_dir
    return phase_dir, tech_dir, corpus, env


def discover_parts(category_dir: Path):
    if not category_dir.is_dir():
        return []
    return sorted(p.name for p in category_dir.iterdir() if p.is_dir())


_RUNTIME_DIRS = {"__pycache__", ".pytest_cache", "instance", ".mypy_cache"}

def clean_runtime(root: Path):
    for d in [p for p in root.rglob("*") if p.is_dir() and p.name in _RUNTIME_DIRS]:
        shutil.rmtree(d, ignore_errors=True)


def _force_remove(p: Path):
    def onerror(func, path, exc):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            pass
    for _ in range(6):
        try:
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p, onerror=onerror)
            else:
                p.unlink(missing_ok=True)
            return
        except FileNotFoundError:
            return
        except (PermissionError, OSError):
            time.sleep(0.5)


def clear_dir(d: Path):
    d.mkdir(parents=True, exist_ok=True)
    for child in d.iterdir():
        _force_remove(child)


def apply_solution(env: Path, phase_dir: str, tech: str):
    if tech == "flask":
        sol_dir = SOLUTIONS / phase_dir / TECHS["flask"][phase_dir]
        matches = sorted(sol_dir.glob("**/project.py"))
        if not matches:
            sys.exit(f"No master solution project.py found under {sol_dir}")
        shutil.copy2(matches[0], env / "src" / "project.py")
        print(f"Using master solution: {matches[0].relative_to(SOLUTIONS.parent)}")
        return
    sol_dir = SOLUTIONS / phase_dir / "NuActionGUI"
    src = sol_dir / "project.ptm"
    if not src.exists():
        sys.exit(f"No solution model project.ptm found under {sol_dir}")
    shutil.copy2(src, env / "models" / "EventPlatformNAG" / "project.ptm")
    print("Using master solution privacy model: project.ptm")
    print("  keeping data model     (project.dtm) as template")
    print("  keeping security model (project.stm) as template")


def apply_template(env: Path, phase_dir: str, tech: str):
    if tech == "flask":
        tpl_dir = TEMPLATES / phase_dir / TECHS["flask"][phase_dir]
        matches = sorted(tpl_dir.glob("**/src/project.py"))
        if not matches:
            sys.exit(f"No template project.py found under {tpl_dir}")
        shutil.copy2(matches[0], env / "src" / "project.py")
        print(f"Using template: {matches[0].relative_to(TEMPLATES.parent)}")
        return
    tpl_dir = TEMPLATES / phase_dir / "NuActionGUI"
    matches = sorted(tpl_dir.glob("**/models/EventPlatformNAG/project.ptm"))
    if not matches:
        sys.exit(f"No template project.ptm found under {tpl_dir}")
    shutil.copy2(matches[0], env / "models" / "EventPlatformNAG" / "project.ptm")
    print("Using template privacy model: project.ptm (keeping dtm/stm as template)")


def load_part(part_src: Path, dest: Path):
    clear_dir(dest)
    for f in part_src.iterdir():
        if f.is_file():
            shutil.copy2(f, dest / f.name)


def _draw_bar(prefix, pct, passed, failed, errored, total, width=26):
    pct = max(0, min(100, pct))
    filled = pct * width // 100
    bar = "#" * filled + "-" * (width - filled)
    tail = f"ok {passed:03d}  fail {failed:03d}"
    if errored:
        tail += f"  err {errored:03d}"
    tail += f"  total {total:03d}"
    sys.stdout.write(f"\r{prefix} [{bar}] {pct:3d}%  {tail}   ")
    sys.stdout.flush()


def run_pytest_with_bar(dest: Path, prefix: str) -> dict:
    proc = subprocess.Popen(
        [sys.executable, "-m", "pytest", "-v", "--tb=no", "-p", "no:cacheprovider"],
        cwd=dest, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )
    passed = failed = errored = skipped = total = pct = 0
    failures = []
    _draw_bar(prefix, 0, 0, 0, 0, 0)
    for line in proc.stdout:
        line = line.rstrip("\n")
        m = _COLLECTED_RE.search(line)
        if m:
            total = int(m.group(1))
        sm = _STATUS_RE.match(line)
        if sm:
            status = sm.group("status")
            if status == "PASSED":
                passed += 1
            elif status == "FAILED":
                failed += 1
                failures.append(sm.group("node").strip())
            elif status == "ERROR":
                errored += 1
                failures.append(sm.group("node").strip())
            elif status == "SKIPPED":
                skipped += 1
            pm = _PCT_RE.search(line)
            done = passed + failed + errored + skipped
            pct = int(pm.group(1)) if pm else (done * 100 // total if total else 0)
            _draw_bar(prefix, pct, passed, failed, errored, done)
    rc = proc.wait()
    _draw_bar(prefix, 100, passed, failed, errored, passed + failed + errored + skipped)
    sys.stdout.write("\n")
    return dict(passed=passed, failed=failed, errored=errored, skipped=skipped,
                total=total, rc=rc, failures=failures)

def _nag_proj(env: Path) -> Path:
    return env / "project" / "EventPlatformNAG"

def nag_regenerate(env: Path):
    print("  regenerating project from models ...")
    p = subprocess.run(
        [sys.executable, "src/generate.py", "-p", "EventPlatformNAG", "-o", "project", "-re"],
        cwd=str(env), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        sys.stdout.write((p.stdout or "")[-2000:])
        sys.exit(f"NuActionGUI regeneration failed (exit {p.returncode})")


def nag_overlay_dtm(env: Path, category: str):
    dtm = _nag_proj(env) / "dtm.py"
    prepared_path = env / "_harness" / "prepared_dtm.py"
    if category == "security":
        shutil.copy2(prepared_path, dtm)
        print("  applied prepared security dtm")
        return
    prepared = prepared_path.read_text(encoding="utf-8")
    dest = dtm.read_text(encoding="utf-8")
    pattern = r"(# PURPOSES[\s\S]*?)(with app\.app_context\(\):[\s\S]*)"
    m = re.search(pattern, dest)
    if not m:
        sys.exit("nag_overlay_dtm: PURPOSES/app-context block not found in regenerated dtm.py")
    purposes = m.group(1)
    shutil.copy2(dtm, Path(str(dtm) + ".bak"))
    dtm.write_text(re.sub(pattern, lambda _: f"{prepared}\n \n{purposes}", dest), encoding="utf-8")
    print("  applied prepared privacy dtm (preserving regenerated purposes)")


def nag_move_annotations(env: Path):
    proj = _nag_proj(env)
    app_content = (proj / "app.py").read_text(encoding="utf-8")
    secure = {m.group(3): m.group(1)
              for m in re.finditer(r"(@secure\(.*?\))\n(def\s+(\w+)\s*\()", app_content)}
    project_py = proj / "project.py"
    pc = project_py.read_text(encoding="utf-8")
    lines = pc.splitlines()
    for m in re.finditer(r"^(def\s+(\w+)\s*\(.*\):)", pc, re.MULTILINE):
        deco = secure.get(m.group(2))
        if not deco:
            continue
        prev = pc[:m.start(1)].count("\n") - 1
        if prev >= 0 and lines[prev].strip().startswith("@secure"):
            lines[prev] = deco
    project_py.write_text("\n".join(lines), encoding="utf-8")
    print("  moved @secure annotations into project.py")


def _replace_block(conftest: Path, app_py: Path, new_pat: str, old_pat: str):
    nm = re.search(new_pat, app_py.read_text(encoding="utf-8"))
    if not nm:
        return
    new_block = "\n".join("    " + ln for ln in nm.group(1).splitlines()[1:-1])
    conf = conftest.read_text(encoding="utf-8")
    om = re.search(old_pat, conf)
    if not om:
        return
    old_block = "\n".join(om.group(1).splitlines()[1:-1])
    conftest.write_text(conf.replace(old_block, new_block), encoding="utf-8")


def nag_patch_conftest(dest: Path, app_py: Path):
    conftest = dest / "conftest.py"
    if not conftest.exists():
        return
    _replace_block(
        conftest, app_py,
        r"(purposes = Purpose\.query\.all\(\)\s+if len\(purposes\) == 0:[\s\S]*?personaldata = PersonalData\.query\.all\(\))",
        r"(purposes = Purpose\.query\.all\(\)\s+if len\(purposes\) == 0:[\s\S]*?personaldata = PersonalData\.query\.all\(\))")
    _replace_block(
        conftest, app_py,
        r"(personaldata = PersonalData\.query\.all\(\)\s+if len\(personaldata\) == 0:[\s\S]*?def P\(ls\):)",
        r"(personaldata = PersonalData\.query\.all\(\)\s+if len\(personaldata\) == 0:[\s\S]*?visitorrole)")


def nag_stage_templates(env: Path, dest: Path):
    src = _nag_proj(env) / "templates"
    if src.is_dir():
        shutil.copytree(src, dest / "templates", dirs_exist_ok=True)


def nag_setup(env: Path, category: str):
    print("Setting up NuActionGUI environment ...")
    nag_regenerate(env)
    nag_overlay_dtm(env, category)
    if category != "security":
        nag_move_annotations(env)


def do_list():
    for phase in PHASES:
        for tech in TECHS:
            _, _, corpus, _ = resolve(phase, tech)
            for cat, sub in CATEGORIES.items():
                parts = discover_parts(corpus / sub)
                if parts:
                    print(f"  --phase {phase:4} --tech {tech:5} --category {cat:9} "
                          f"--part {{{','.join(parts)}}}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phase", choices=PHASES)
    ap.add_argument("--tech", choices=TECHS)
    ap.add_argument("--category", choices=list(CATEGORIES), default=None,
                    help="privacy variant to run: none, basic, or complex; "
                         "omit to run all three")
    ap.add_argument("--part", help="a single part (e.g. part1); omit to run all parts in the category")
    ap.add_argument("--solution", action="store_true",
                    help="copy the master solution (solutions/<phase>/<tech>/project.py) into the "
                         "environment before running, instead of the template")
    ap.add_argument("--list", action="store_true", help="list available corpus parts and exit")
    ap.add_argument("--no-run", action="store_true",
                    help="copy the test files into the environment but do not run pytest")
    args = ap.parse_args()

    if args.list:
        do_list()
        return 0

    missing = [f"--{n}" for n in ("phase", "tech")
               if getattr(args, n) is None]
    if missing:
        ap.error("the following arguments are required: " + ", ".join(missing))

    phase_dir, tech_dir, corpus, env = resolve(args.phase, args.tech)
    if not env.is_dir():
        sys.exit(f"Environment not found: {env}")
    variants = [args.category] if args.category else list(PRIVACY_VARIANTS)
    multi = len(variants) > 1
    cat_label = args.category or "privacy"  

    jobs = []
    for v in variants:
        vdir = corpus / CATEGORIES[v]
        if args.part:
            if (vdir / args.part).is_dir():
                jobs.append((f"{v}/{args.part}" if multi else args.part, vdir / args.part))
        else:
            for part in discover_parts(vdir):
                jobs.append((f"{v}/{part}" if multi else part, vdir / part))
    if not jobs:
        sys.exit("No matching corpus parts found (use --list to see what exists)")

    dest = env_tests_dir(env, args.tech)
    clean_runtime(env)
    clear_dir(dest)
    if args.solution:
        apply_solution(env, phase_dir, args.tech)
    else:
        apply_template(env, phase_dir, args.tech)

    if args.no_run:
        for label, src in jobs:
            load_part(src, dest)
            print(f"Loaded {args.phase}/{args.tech}/{cat_label}/{label} "
                  f"-> {dest.relative_to(ROOT)}")
        return 0

    if args.tech == "nag":
        nag_setup(env, args.category)
        clear_dir(dest)  
    app_py = _nag_proj(env) / "app.py"

    print(f"\nRunning {args.phase}/{args.tech}/{cat_label} "
          f"({len(jobs)} part{'s' if len(jobs) != 1 else ''})\n")
    results = {}
    order = []
    width = max((len(lbl) for lbl, _ in jobs), default=7)
    iw = len(str(len(jobs)))  
    for i, (label, src) in enumerate(jobs, 1):
        load_part(src, dest)
        if args.tech == "nag":
            nag_stage_templates(env, dest)
            if args.category != "security":
                nag_patch_conftest(dest, app_py)
        prefix = f"[{i:0{iw}d}/{len(jobs)}] {label:{width}}"
        results[label] = run_pytest_with_bar(dest, prefix)
        order.append(label)

    tot_pass = sum(r["passed"] for r in results.values())
    tot_fail = sum(r["failed"] for r in results.values())
    tot_err = sum(r["errored"] for r in results.values())
    tot_skip = sum(r["skipped"] for r in results.values())
    grand = tot_pass + tot_fail + tot_err + tot_skip
    w = max(3, len(str(grand)))

    def fmt(passed, failed, errored, total):
        s = f"ok {passed:0{w}d}  fail {failed:0{w}d}"
        if tot_err:
            s += f"  err {errored:0{w}d}"
        return s + f"  total {total:0{w}d}"

    print("\n" + "=" * 60)
    print(f"Summary: {args.phase}/{args.tech}/{cat_label}")
    lw = max(width, len("TOTAL"))
    for label in order:
        r = results[label]
        ptot = r["passed"] + r["failed"] + r["errored"] + r["skipped"]
        print(f"  {label:{lw}} {fmt(r['passed'], r['failed'], r['errored'], ptot)}")
    print("-" * 60)
    pct = (tot_pass / grand * 100) if grand else 0.0
    print(f"  {'TOTAL':{lw}} {fmt(tot_pass, tot_fail, tot_err, grand)}  ({pct:.1f}% passed)")
    return 0 if (tot_fail == 0 and tot_err == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
