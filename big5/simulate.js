if (uproot.currentPage == "big5/Response") {
    const radios = document.querySelectorAll('input[type="radio"]');
    const idx = Math.floor(Math.random() * 5);
    radios[idx].checked = true;
    uproot.submit();
}

if (uproot.currentPage == "big5/Results") {
    // uproot.submit();
}
