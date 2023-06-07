async function updateSensorsDashboard() {
    const sensorsData = await getData("/api/sensors");

    let currentDatetime = formatDateTimeFromIsoString(sensorsData.datetime);
    let lastLogTime = formatDateTimeFromIsoString(sensorsData.last_weather_log);

    setSensorValue("temperature-reading", sensorsData.temperature)
    setSensorValue("humidity-reading", sensorsData.humidity)
    setSensorValue("battery-voltage-reading", sensorsData.battery_voltage)
    setSensorValue("pv-voltage-reading", sensorsData.pv_voltage)
    setSensorValue("datetime-reading", currentDatetime)
    setSensorValue("last-log-time-reading", lastLogTime)
}


function setSensorValue(id, value) {
    const container = document.getElementById(id);

    if (container) {
        if (value) {
            container.innerHTML = value;
        } else {
            container.innerHTML = "-"
        }
    }
}

async function renderLoggedDays() {
    const days = await getData("/api/weather/logged_days");
    const daysContainer = document.getElementById("logged-days-container");

    for (let day of days) {
        let dayContainer = document.createElement("div");
        let dayLink = document.createElement("a");
        dayLink.href = "/weather_logs/" + day;

        dayLink.innerHTML = day;
        dayContainer.appendChild(dayLink);

        dayContainer.classList.add("logged-day-wrapper");
        daysContainer.appendChild(dayContainer);
    }

    document.getElementById("loader").classList.add("d-none");
}
