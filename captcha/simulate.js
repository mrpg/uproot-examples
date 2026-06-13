uproot.simulate.on("captcha/SolveCaptcha", (sim) => {
    const image = document.querySelector("[data-captcha-answer]");

    sim.fill("captcha_answer", image.dataset.captchaAnswer).submit();
});
