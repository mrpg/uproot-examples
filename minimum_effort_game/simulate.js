// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "minimum_effort_game/ChooseEffort") {
    var level = Math.floor(Math.random() * 7);
    I("effort-" + level).checked = true;
    uproot.submit();
}

if (uproot.currentPage == "minimum_effort_game/Results") {
    // uproot.submit();
}
