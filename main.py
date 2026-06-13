#!/usr/bin/env python
# Third-party dependencies:
# - uproot: LGPL v3+, see ./uproot_license.txt
import os

import uproot.deployment as upd
from uproot.cli import cli
from uproot.server import load_config, uproot_server

upd.project_metadata(created="1970-01-01", uproot="*.*.*")

# Load your app configs here
# Examples are available at https://github.com/mrpg/uproot-examples

# fmt: off
load_config(uproot_server, config="anchoring", apps=["anchoring"])
load_config(uproot_server, config="balanced_page_order", apps=["balanced_page_order"])
load_config(uproot_server, config="bargaining", apps=["bargaining"])
load_config(uproot_server, config="barrier", apps=["barrier"])
load_config(uproot_server, config="beauty_contest", apps=["beauty_contest"])
load_config(uproot_server, config="bertrand", apps=["bertrand"])
load_config(uproot_server, config="between", apps=["between"])
load_config(uproot_server, config="big5", apps=["big5"])
load_config(uproot_server, config="bisection", apps=["bisection"])
load_config(uproot_server, config="bounded_choice", apps=["bounded_choice"])
load_config(uproot_server, config="bret", apps=["bret"])
load_config(uproot_server, config="button_placement", apps=["button_placement"])
load_config(uproot_server, config="call_auction", apps=["call_auction"])
load_config(uproot_server, config="captcha", apps=["captcha"])
load_config(uproot_server, config="chat", apps=["chat"])
load_config(uproot_server, config="chat_with_claude", apps=["chat_with_claude"])
load_config(uproot_server, config="conjoint", apps=["conjoint"])
load_config(uproot_server, config="continuous", apps=["continuous"])
load_config(uproot_server, config="counter_alpine", apps=["counter_alpine"])
load_config(uproot_server, config="counter", apps=["counter"])
load_config(uproot_server, config="cournot", apps=["cournot"])
load_config(uproot_server, config="detect_presence", apps=["detect_presence"])
load_config(uproot_server, config="dictator_game", apps=["dictator_game"])
load_config(uproot_server, config="die_roll", apps=["die_roll"])
load_config(uproot_server, config="double_auction", apps=["double_auction"])
load_config(uproot_server, config="draganddrop", apps=["draganddrop"])
load_config(uproot_server, config="drawing_board", apps=["drawing_board"])
load_config(uproot_server, config="dropouts", apps=["dropouts"])
load_config(uproot_server, config="embed_static", apps=["embed_static"])
load_config(uproot_server, config="emoji_sort", apps=["emoji_sort"])
load_config(uproot_server, config="encryption_task", apps=["encryption_task"])
load_config(uproot_server, config="first_price_auction", apps=["first_price_auction"])
load_config(uproot_server, config="focal_point", apps=["focal_point"])
load_config(uproot_server, config="gift_exchange_game", apps=["gift_exchange_game"])
load_config(uproot_server, config="grouping", apps=["grouping"])
load_config(uproot_server, config="grouping_arbitrary_size", apps=["grouping_arbitrary_size"])
load_config(uproot_server, config="grouping_one_spare", apps=["grouping_one_spare"])
load_config(uproot_server, config="group_with_dropout", apps=["group_with_dropout"])
load_config(uproot_server, config="input_elements", apps=["input_elements"])
load_config(uproot_server, config="input_validation", apps=["input_validation"])
load_config(uproot_server, config="many_fields", apps=["many_fields"])
load_config(uproot_server, config="market", apps=["market"])
load_config(uproot_server, config="minimum_effort_game", apps=["minimum_effort_game"])
load_config(uproot_server, config="mpl", apps=["mpl"])
load_config(uproot_server, config="multilanguage", apps=["multilanguage"])
load_config(uproot_server, config="n_by_n", apps=["n_by_n"])
load_config(uproot_server, config="nato_alphabet", apps=["nato_alphabet"])
load_config(uproot_server, config="notifications", apps=["notifications"])
load_config(uproot_server, config="observed_diary", apps=["observed_diary"])
load_config(uproot_server, config="payment_data", apps=["payment_data"])
load_config(uproot_server, config="pgg_punishment", apps=["pgg_punishment"])
load_config(uproot_server, config="ping", apps=["ping"])
load_config(uproot_server, config="prisoners_dilemma", apps=["prisoners_dilemma"])
load_config(uproot_server, config="prisoners_dilemma_apply", apps=["prisoners_dilemma_apply"])
load_config(uproot_server, config="prisoners_dilemma_chat", apps=["prisoners_dilemma_chat"])
load_config(uproot_server, config="prisoners_dilemma_repeated", apps=["prisoners_dilemma_repeated"])
load_config(uproot_server, config="public_goods_game", apps=["public_goods_game"])
load_config(uproot_server, config="quiz", apps=["quiz"])
load_config(uproot_server, config="randomize_pages_allow_back", apps=["randomize_pages_allow_back"])
load_config(uproot_server, config="randomize_pages", apps=["randomize_pages"])
load_config(uproot_server, config="read_settings", apps=["read_settings"])
load_config(uproot_server, config="revise", apps=["revise"])
load_config(uproot_server, config="rounds", apps=["rounds"])
load_config(uproot_server, config="rounds_nested", apps=["rounds_nested"])
load_config(uproot_server, config="second_price_auction", apps=["second_price_auction"])
load_config(uproot_server, config="sound_recording", apps=["sound_recording"])
load_config(uproot_server, config="stackelberg", apps=["stackelberg"])
load_config(uproot_server, config="streaming", apps=["streaming"])
load_config(uproot_server, config="stroop", apps=["stroop"])
load_config(uproot_server, config="student_id", apps=["student_id"])
load_config(uproot_server, config="sumhunt", apps=["sumhunt"])
load_config(uproot_server, config="survey", apps=["survey"])
load_config(uproot_server, config="svo_slider", apps=["svo_slider"])
load_config(uproot_server, config="tabs", apps=["tabs"])
load_config(uproot_server, config="templating_and_typography", apps=["templating_and_typography"])
load_config(uproot_server, config="timeout_multipage", apps=["timeout_multipage"])
load_config(uproot_server, config="total_stranger_matching", apps=["total_stranger_matching"])
load_config(uproot_server, config="travellers_dilemma", apps=["travellers_dilemma"])
load_config(uproot_server, config="treatments", apps=["treatments"])
load_config(uproot_server, config="treatments_balanced", apps=["treatments_balanced"])
load_config(uproot_server, config="trigger_jserrors", apps=["trigger_jserrors"])
load_config(uproot_server, config="trust_game", apps=["trust_game"])
load_config(uproot_server, config="tullock_contest", apps=["tullock_contest"])
load_config(uproot_server, config="twobytwo", apps=["twobytwo"])
load_config(uproot_server, config="ultimatum_game", apps=["ultimatum_game"])
load_config(uproot_server, config="upload", apps=["upload"])
# fmt: on

# Create admin

upd.ADMINS["admin"] = upd.auto_login()

# Set API key

if api_key := os.getenv("UPROOT_API_KEY"):
    upd.API_KEYS.add(api_key)

# Set default language

upd.LANGUAGE = "en"  # Available languages: "de", "en", "es"

# Run uproot (leave this as-is)

if __name__ == "__main__":
    cli()
