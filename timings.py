#!/usr/bin/env python
import sty
import glint
import os.path
import json
import inspect
import time
import pathlib
import datetime


def myself():
    return inspect.stack()[1][3]


def prj_db_path():
    return os.path.expanduser("~/.timings.txt")


def init_timings():
    print("creating new %s'%s'%s" % (sty.fg.blue, prj_db_path(), sty.fg.rs))
    write_timings(dict())


def save_current_timings_file():

    def mv_timings_to_backup():
        new_name = f"{prj_db_path()}-{time.time()}"
        p = pathlib.Path(prj_db_path())
        print(f"moving {sty.fg.red}{prj_db_path()}{sty.fg.rs} to {sty.fg.green}{new_name}{sty.fg.rs}")
        p.rename(new_name)

    if pathlib.Path(prj_db_path()).exists():
        mv_timings_to_backup()


def read_timings():
    try:
        with open(prj_db_path()) as f:
            content = json.load(f)
    except (json.decoder.JSONDecodeError, FileNotFoundError) as ex:
        save_current_timings_file()
        init_timings()
        print("The timings DB was defect. Starting with an empty DB.")
        content = dict()
    return content


def write_timings(projects):
    with open(prj_db_path(), "w") as f:
        json.dump(projects, f, indent=4)


def add_project(name):
    """Add a project to timings DB to later book time on it."""
    projects = read_timings()
    if name not in projects:
        projects[name] = []
        write_timings(projects)
    else:
        print(f"{name} already in timings DB: no change.")


def del_project(name):
    """Add a project to timings DB to later book time on it."""
    projects = read_timings()
    if name in projects:
        del projects[name]
        write_timings(projects)
    else:
        print(f"{name} {sty.fg.red}not in timings DB: no change.{sty.fg.rs}")


def continue_project(name):
    projects = read_timings()
    if name in projects:
        projects[name].append([time.time(), "started"])
        write_timings(projects)
    else:
        print(f"{name} not in timings DB: no change.")


def stop(name):
    def epoch_to_datetime(t):
        return datetime.datetime.fromtimestamp(t).strftime("%Y.%m.%d %H:%M:%S")

    projects = read_timings()
    if name in projects:
        for i, pair in enumerate(projects[name]):
            if pair[1] == "started":
                t0 = pair[0]
                t1 = time.time()
                minutes = int((t1 - t0) / 60)
                pair[1] = minutes
                pair[0] = f"{epoch_to_datetime(t0)} .. {epoch_to_datetime(t1)}"
        write_timings(projects)
        show_single_project(name, projects[name])
    else:
        print(f"{name} not in timings DB: no change.")


def show_single_project(prj_name, prj, all=True, summaries=True):
    print("%s%s%s" % (sty.fg.green, prj_name, sty.fg.rs))
    if all or summaries:
        sum = 0
        for entry in prj:
            if not summaries:
                print("\t%s%s%s" % (sty.fg.li_blue, entry, sty.fg.rs))
            sum += entry[1] if type(entry[1]) is int else 0
        print(f"\t{sty.fg.yellow}Sum: {sty.fg.green}{int(sum / 60)}:{sum % 60:02} ({sum}){sty.fg.rs}")


def show_projects(raw=False, all=False, summaries=False):
    print(f"Current projects:")
    projects = read_timings()
    if raw:
        print(f"{projects}")
    else:
        for prj_name in projects:
            show_single_project(prj_name, projects[prj_name], all, summaries)
            print()


def empty_project(name):
    projects = read_timings()
    if name in projects:
        projects[name].clear()
        write_timings(projects)
    else:
        print(f"{name} {sty.fg.red}not in timings DB: no change.{sty.fg.rs}")


def default():
    print(sty.fg.red, f"something in RED")
    # save_current_timings_file()
    pass


if __name__ == '__main__':
    runner = glint.Runner()
    runner["add"] = (add_project, "add project 'name'")
    runner["del"] = (del_project, "delete project 'name'")
    runner["projects"] = (show_projects, "show projects")
    runner["continue"] = (continue_project, "start/continue working on project 'name'")
    runner["start"] = (continue_project, "start/continue working on project 'name'")
    runner["done"] = (stop, "stop working on project 'name'")
    runner["stop"] = (stop, "stop working on project 'name'")
    runner["empty"] = (empty_project, "remove all entries from project 'name'")
    runner[None] = default
    runner.run()
