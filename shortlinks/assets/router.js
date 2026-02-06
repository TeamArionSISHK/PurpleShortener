(() => {
  const titleEl = document.getElementById("title");
  const messageEl = document.getElementById("message");
  const messageTextEl = document.getElementById("message-text");
  const fallbackEl = document.getElementById("fallback");
  const statusEl = document.getElementById("status");
  const script = document.currentScript || document.querySelector("script[data-links-url]");

  const linksUrl = (script && script.dataset.linksUrl) || "/links.json";
  const outboundBase = (script && script.dataset.outboundBase) || "/outbound/";

  const showError = (message) => {
    document.title = "Link not found";
    titleEl.textContent = "Link not found";
    messageTextEl.textContent = message;
    if (messageEl) messageEl.classList.remove("hidden");
    if (statusEl) statusEl.classList.add("hidden");
    fallbackEl.style.display = "none";
  };

  const showStatus = () => {
    document.title = "Team Arion Short Links";
    titleEl.textContent = "Team Arion Short Links";
    if (messageEl) messageEl.classList.add("hidden");
    if (statusEl) statusEl.classList.remove("hidden");
    fallbackEl.style.display = "none";
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

  const pathname = window.location.pathname;
  const outboundPrefix = outboundBase.endsWith("/") ? outboundBase : `${outboundBase}/`;

  if (pathname === outboundBase.replace(/\/+$/, "") || pathname.startsWith(outboundPrefix)) {
    const rest = pathname.startsWith(outboundPrefix) ? pathname.slice(outboundPrefix.length) : "";
    const rawTo = getRawQueryParam("to");

    if (rest.startsWith("generate")) {
      window.location.replace("/outbound/generate/");
      return;
    }

    if (rest && rest !== "index.html") {
      window.location.replace(`/outbound/index.html?to=${rest}`);
      return;
    }

    if (rawTo) {
      window.location.replace(`/outbound/index.html?to=${rawTo}`);
      return;
    }

    window.location.replace("/outbound/index.html");
    return;
  }

  const rawPath = pathname.replace(/^\/+|\/+$/g, "");
  let code = rawPath.split("/")[0];
  try {
    code = decodeURIComponent(code);
  } catch (error) {
    code = "";
  }

  if (!code) {
    showStatus();
    return;
  }

  fetch(linksUrl, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load link data");
      }
      return response.json();
    })
    .then((links) => {
      const entry = links[code];
      if (entry && entry.url) {
        const title = entry.title || "Redirecting";
        document.title = title;
        titleEl.textContent = title;
        fallbackEl.href = entry.url;
        window.location.replace(entry.url);
      } else {
        showError("This short link does not exist.");
      }
    })
    .catch(() => {
      titleEl.textContent = "Configuration error";
      messageTextEl.textContent = "Link data is unavailable.";
      fallbackEl.style.display = "none";
    });
})();
