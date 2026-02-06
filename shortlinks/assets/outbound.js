(() => {
  const domainEl = document.getElementById("dest-domain");
  const urlEl = document.getElementById("dest-url");
  const continueEl = document.getElementById("continue");

  const disableContinue = (message) => {
    domainEl.textContent = "Invalid destination";
    urlEl.textContent = message;
    continueEl.setAttribute("aria-disabled", "true");
    continueEl.removeAttribute("href");
  };

  const getRawQueryParam = (name) => {
    const query = window.location.search.replace(/^\?/, "");
    if (!query) return "";
    for (const part of query.split("&")) {
      if (!part) continue;
      const [key, ...rest] = part.split("=");
      if (key === name) {
        return rest.join("=");
      }
    }
    return "";
  };

  const pathBase = "/outbound/";
  const path = window.location.pathname;
  let rawPath = path.startsWith(pathBase) ? path.slice(pathBase.length) : "";
  if (rawPath.startsWith("index.html")) {
    rawPath = "";
  }
  if (rawPath.startsWith("generate")) {
    rawPath = "";
  }

  const rawQuery = getRawQueryParam("to");
  const raw = rawPath || rawQuery;

  if (!raw) {
    disableContinue("Missing destination.");
    return;
  }

  let decoded;
  try {
    decoded = decodeURIComponent(raw);
  } catch (error) {
    disableContinue("Unable to decode destination.");
    return;
  }

  try {
    const target = new URL(decoded);
    if (!/^https?:$/.test(target.protocol)) {
      throw new Error("Unsupported protocol");
    }
    domainEl.textContent = target.hostname;
    urlEl.textContent = target.href;
    continueEl.href = target.href;
    continueEl.setAttribute("aria-disabled", "false");
  } catch (error) {
    disableContinue("Destination must be a valid http or https URL.");
  }
})();
