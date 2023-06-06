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


function formatDateTimeFromIsoString(datetime) {
    let formattedDatetime = null;

    if (datetime) {
        const splitedDatetime = datetime.split("T");
        formattedDatetime = `${splitedDatetime[0]} ${splitedDatetime[1].split(".")[0]}`;
    }

    return formattedDatetime;
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
}

async function renderLogTable(day) {
    const data = await getData("/api/weather/logs/" + day);
    const tableContainer = document.getElementById("log-data-table");

    if (data.logs.length > 0 && data.headers.length > 0) {
        const table = document.createElement("table");
        const tableHeaders = data.headers;

        let tableRow = document.createElement("tr");

        for (let header of tableHeaders) {
            let tableHeader = document.createElement("td");
            tableHeader.innerHTML = header;

            tableRow.appendChild(tableHeader);
        }

        table.appendChild(tableRow);

        for (let row of data.logs) {
            let tableRow = document.createElement("tr");

            for (let header of tableHeaders) {
                let td = document.createElement("td");
                td.innerHTML = row[header];

                tableRow.appendChild(td);
            }

            table.appendChild(tableRow);
        }

        tableContainer.appendChild(table);
    }
}
