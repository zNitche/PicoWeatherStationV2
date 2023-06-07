async function renderLogs(dataURL) {
    const data = await getData(dataURL);
    renderLogTable(data);
    createGraphs(data);

    document.getElementById("logs-wrapper").classList.remove("d-none");
}


function renderLogTable(data) {
    const tableContainer = document.getElementById("log-data-table");

    if (data.logs.length > 0 && data.headers.length > 0) {
        const table = document.createElement("table");
        const tableHeaders = data.headers;

        createTableHeader(tableHeaders, table);
        createTableRow(data.logs, tableHeaders, table);

        tableContainer.appendChild(table);
    }

    document.getElementById("loader").classList.add("d-none");
}


function createTableHeader(tableHeaders, table) {
    let tableRow = document.createElement("tr");

    for (let header of tableHeaders) {
        let tableHeader = document.createElement("td");
        tableHeader.innerHTML = header.replace("_", " ");

        tableRow.appendChild(tableHeader);
    }

    table.appendChild(tableRow);
}


function createTableRow(logs, tableHeaders, table) {
    for (let row of logs) {
        let tableRow = document.createElement("tr");

        for (let header of tableHeaders) {
            let td = document.createElement("td");

            if (header == "DATETIME") {
                td.innerHTML = formatTimeFromIsoString(row[header]);
            } else {
                td.innerHTML = row[header];
            }

            tableRow.appendChild(td);
        }

        table.appendChild(tableRow);
    }
}


function createGraphs(data) {
    if (data.logs.length > 0 && data.headers.length > 0) {
        for (let header of data.headers) {
            const graphId = header.toLowerCase().replace("_", "-") + "-graph";

            if (document.getElementById(graphId)) {
                const graphDataset = createGraphDatasetForHeader(header, data.logs);
                createGraph(graphId, graphDataset);
            }
        }
    }
}

function createGraphDatasetForHeader(header, data) {
    let dataset = {
        title: header.replace("_", " "),
        x: [],
        y: []
    };

    for (let row of data) {
        const time = formatTimeFromIsoString(row["DATETIME"]);

        dataset.x.push(time.slice(0, -3));
        dataset.y.push(row[header]);
    }

    return dataset;
}

function createGraph(graphId, graphDataset) {
    createLinearChart(graphId, graphDataset.title, graphDataset.x, graphDataset.y);
}
