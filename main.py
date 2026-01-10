#!/usr/bin/env python
# Third-party dependencies:
# - uproot: LGPL v3+, see ./uproot_license.txt
import uproot.deployment as upd
from uproot.cli import cli
from uproot.server import load_config, uproot_server

upd.project_metadata(created="1970-01-01", uproot="*.*.*")

# Load your app configs here
# Examples are available at https://github.com/mrpg/uproot-examples

# fmt: off
load_config(uproot_server, config="barrier", apps=["barrier"])
load_config(uproot_server, config="big5_short", apps=["big5_short"])
load_config(uproot_server, config="chat", apps=["chat"])
load_config(uproot_server, config="continuous", apps=["continuous"])
load_config(uproot_server, config="dictator_game", apps=["dictator_game"])
load_config(uproot_server, config="double_auction", apps=["double_auction"])
load_config(uproot_server, config="drawing_board", apps=["drawing_board"])
load_config(uproot_server, config="dropouts", apps=["dropouts"])
load_config(uproot_server, config="focal_point", apps=["focal_point"])
load_config(uproot_server, config="mpl", apps=["mpl"])
load_config(uproot_server, config="observed_diary", apps=["observed_diary"])
load_config(uproot_server, config="payment_data", apps=["payment_data"])
load_config(uproot_server, config="prisoners_dilemma", apps=["prisoners_dilemma"])
load_config(uproot_server, config="prisoners_dilemma_apply", apps=["prisoners_dilemma_apply"])
load_config(uproot_server, config="prisoners_dilemma_repeated", apps=["prisoners_dilemma_repeated"])
load_config(uproot_server, config="public_goods_game", apps=["public_goods_game"])
# load_config(uproot_server, config="randomize_apps", apps=["randomize_apps"])
load_config(uproot_server, config="randomize_pages", apps=["randomize_pages"])
load_config(uproot_server, config="randomize_pages_allow_back", apps=["randomize_pages_allow_back"])
load_config(uproot_server, config="rounds", apps=["rounds"])
load_config(uproot_server, config="student_id", apps=["student_id"])
load_config(uproot_server, config="twobytwo", apps=["twobytwo"])
load_config(uproot_server, config="ultimatum_game", apps=["ultimatum_game"])
load_config(uproot_server, config="upload", apps=["upload"])
# fmt: on

# Create admin

upd.ADMINS["admin"] = ...

# Set default language

upd.LANGUAGE = "en"  # Available languages: "de", "en", "es"

# Run uproot (leave this as-is)

if __name__ == "__main__":
    cli()
