#
# FILENAME.
#       cnt_ft.py - Count Command Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module implements the Command class.
#
# NOTICE.
#       Author: visualge@gmail.com (Count Chu)
#       Created on 2025/8/19
#       Updated on 2025/8/21
#

from pathlib import Path
from types import SimpleNamespace

from Count import cnt_config
import arrow

br = breakpoint


def build_context(ctx, where="app"):
    # Build params if ctx is not None.
    params = None
    command = None
    if ctx is not None:
        params = ctx.params
        command = ctx.invoked_subcommand
        if ctx.parent is not None:
            params = ctx.parent.params
            params.update(ctx.params)
            command = ctx.parent.invoked_subcommand

    # Load config from config.yaml, and get app

    working_p = None
    if where == "jupyter":
        working_p = Path.cwd()

    config = params["config"]
    cfg = cnt_config.load_app_config(config, working_p)

    # Load db_y from InvDatabase/config.yaml

    db_p = Path(cfg["__dir__"]) / cfg["database"]["config"]
    db_y = cnt_config.load(db_p)

    # Build today.

    today = arrow.now().format("YYYY-MM-DD")

    # Build cmd

    cmd = None
    if command != None:
        cmd = cfg["cmd"][command]

    # ctx.obj is a class instance with params, cfg,
    # so that I can access cfg such that ctx.obj.cfg.

    out = SimpleNamespace(
        params=params,
        command=command,
        cfg=cfg,
        db_y=db_y,
        today=today,
        app=None,
        cmd=cmd,
        refer={},
    )

    return out


class Command:
    def __init__(self, ctx):
        self.ctx = build_context(ctx)

    def _get_path(self, key, _id):
        id_parts = _id.split(".")

        if len(id_parts) == 1:
            p = Path(self.ctx.db_y["__dir__"]) / self.ctx.db_y[key][_id]

        elif len(id_parts) == 2:
            refer, _id = id_parts
            p = Path(self.ctx.refer[refer]["__dir__"]) / self.ctx.refer[refer][key][_id]

        else:
            assert False, _id

        return p

    def run(self):
        pass
