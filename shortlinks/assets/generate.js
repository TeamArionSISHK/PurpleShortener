(() => {
  const input = document.getElementById("destination");
  const output = document.getElementById("output");
  const copyBtn = document.getElementById("copy");
  const visitBtn = document.getElementById("visit");

  const base = `${window.location.origin}/outbound/`;

  const setDisabled = (disabled) => {
    copyBtn.disabled = disabled;
    visitBtn.setAttribute("aria-disabled", disabled ? "true" : "false");
    if (disabled) {
      visitBtn.removeAttribute("href");
    }
  };

  const update = () => {
    const raw = input.value.trim();
    if (!raw) {
      output.textContent = "Enter a destination to generate a link.";
      setDisabled(true);
      return;
    }

    let url;
    try {
      url = new URL(raw);
    } catch (error) {
      output.textContent = "Please enter a valid URL starting with http or https.";
      setDisabled(true);
      return;
    }

    if (!/^https?:$/.test(url.protocol)) {
      output.textContent = "Only http and https URLs are allowed.";
      setDisabled(true);
      return;
    }

    const encoded = encodeURIComponent(url.href);
    const result = `${base}${encoded}`;
    output.textContent = result;
    visitBtn.href = result;
    setDisabled(false);
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(output.textContent);
      copyBtn.textContent = "Copied";
      setTimeout(() => {
        copyBtn.textContent = "Copy link";
      }, 1500);
    } catch (error) {
      copyBtn.textContent = "Copy failed";
      setTimeout(() => {
        copyBtn.textContent = "Copy link";
      }, 1500);
    }
  };

  input.addEventListener("input", update);
  copyBtn.addEventListener("click", copyLink);
  setDisabled(true);
})();
