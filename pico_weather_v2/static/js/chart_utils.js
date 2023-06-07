function createLinearChart(chartID, title, xValues, yValues) {
    new Chart(chartID, {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          backgroundColor:"#fff",
          borderColor: "#8DB580",
          data: yValues
        }]
      },
      options: {
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true,
                text: title
            }
        },
      }
    });

    Chart.defaults.color = "#fff";
}
