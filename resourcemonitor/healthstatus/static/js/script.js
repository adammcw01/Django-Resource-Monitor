document.addEventListener("DOMContentLoaded", () => {
  async function fetchDevices() {
    try {
      const resp = await fetch("/devices");
      const data = await resp.json();

      const tbody = document.querySelector("#deviceTable tbody");
      tbody.innerHTML = ""; // clear old rows

      data.forEach(d => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${d.name}</td>
          <td>${d.ip_address}</td>
          <td>${d.status === true
              ? '<span class="text-success">Up</span>'
              : '<span class="text-danger">Down</span>'}
          </td>`;
        tbody.appendChild(row);
      });
    } catch (err) {
      console.error("Error fetching devices:", err);
    }
  }

  // Manual refresh button
  document.getElementById("refreshBtn").addEventListener("click", fetchDevices);

  // Auto refresh toggle
  let intervalId = null;
  document.getElementById("autoRefreshSwitch").addEventListener("change", (e) => {
    if (e.target.checked) {
      fetchDevices(); // refresh immediately when enabled
      intervalId = setInterval(fetchDevices, 5000); // 5 seconds
    } else {
      clearInterval(intervalId);
    }
  });

  // Initial load
  fetchDevices();
});
