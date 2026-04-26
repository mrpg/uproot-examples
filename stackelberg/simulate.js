// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "stackelberg/Instructions") {
    uproot.submit();
}

if (uproot.currentPage == "stackelberg/LeaderDecision") {
    I("units").value = "40";
    uproot.submit();
}

if (uproot.currentPage == "stackelberg/FollowerDecision") {
    I("units").value = "30";
    uproot.submit();
}

if (uproot.currentPage == "stackelberg/Results") {
    // uproot.submit();
}
