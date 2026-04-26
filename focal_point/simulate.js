// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "focal_point/Claim") {
    var claim = Math.floor(Math.random() * 101);
    I("claim").value = claim;
    uproot.submit();
}

if (uproot.currentPage == "focal_point/Results") {
    // uproot.submit();
}
