(function () {
  const counterSection = document.querySelector("#visitor-counter");
  if (!counterSection) return;

  const counterValueEl = document.getElementById("visitor-count");
  const statusEl = document.getElementById("counter-status");
  const endpoints = {
    // Azure Function endpoints exposed via Static Web Apps proxy (/api/* routes)
    get: counterSection.dataset.counterUrl || "/api/counter",
    increment: counterSection.dataset.incrementUrl || "/api/counter/increment",
  };

  const setStatus = (message, isError = false) => {
    statusEl.textContent = message;
    statusEl.classList.toggle("error", Boolean(isError));
  };

  const setLoading = (isLoading) => {
    counterSection.classList.toggle("loading", isLoading);
  };

  const updateCountContent = (count) => {
    const parsed = Number(count);
    counterValueEl.textContent = Number.isFinite(parsed) ? parsed.toLocaleString() : "--";
  };

  const requestCount = async ({ increment = false } = {}) => {
    const endpoint = increment ? endpoints.increment : endpoints.get;
    const method = increment ? "POST" : "GET";

    // Call Azure Function HTTP trigger to read or increment the Cosmos DB counter
    const response = await fetch(endpoint, {
      method,
      headers: { Accept: "application/json" },
    });

    if (!response.ok) {
      throw new Error(`Counter request failed with status ${response.status}`);
    }

    const payload = await response.json();
    if (typeof payload.count === "undefined") {
      throw new Error("Counter response missing count value");
    }

    return payload.count;
  };

  const refreshCounter = async ({ increment = false, fallback = true } = {}) => {
    setLoading(true);
    setStatus(increment ? "Updating counter…" : "Loading counter…");

    try {
      const count = await requestCount({ increment });
      updateCountContent(count);
      setStatus(increment ? "Visitor counted!" : "");
    } catch (error) {
      console.error(error);
      if (increment && fallback) {
        return refreshCounter({ increment: false, fallback: false });
      }
      setStatus("Unable to reach counter service. Please try again.", true);
    } finally {
      setLoading(false);
    }
  };

  // Automatically increment counter on page load
  refreshCounter({ increment: true });
})();
