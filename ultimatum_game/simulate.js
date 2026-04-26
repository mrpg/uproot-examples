// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "ultimatum_game/Propose") {
    I("offer").value = "4";
    uproot.submit();
}

if (uproot.currentPage == "ultimatum_game/Respond") {
    I("accept-0").checked = true;
    uproot.submit();
}

if (uproot.currentPage == "ultimatum_game/Results") {
    // uproot.submit();
}
