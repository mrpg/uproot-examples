// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "public_goods_game/Contribute") {
    I("contribution").value = "5";
    uproot.submit();
}

if (uproot.currentPage == "public_goods_game/Results") {
    // uproot.submit();
}
