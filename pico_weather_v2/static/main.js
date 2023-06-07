async function getData(url) {
    const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }

    const response = await fetch(url, options);

    return response.json();
}


async function postData(url, data={}) {
    const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        }

    const response = await fetch(url, options);

    return response.json();
}


function formatDateTimeFromIsoString(datetime) {
    let formattedDatetime = null;

    if (datetime) {
        const splitedDatetime = datetime.split("T");
        formattedDatetime = `${splitedDatetime[0]} ${splitedDatetime[1].split(".")[0]}`;
    }

    return formattedDatetime;
}


function formatTimeFromIsoString(datetime) {
    let formattedTime = null;

    if (datetime) {
        const splitedDatetime = datetime.split("T");
        formattedTime = splitedDatetime[1].split(".")[0];
    }

    return formattedTime;
}
