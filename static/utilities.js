function histogramRaw(filename, folder) {
  let path = "/histograma/" + filename + "/" + folder;
  fetch(path)
    .then((response) => response.json())
    .then((data) => {
      const redChannel = document.getElementById("redChannel");
      const greenChannel = document.getElementById("greenChannel");
      const blueChannel = document.getElementById("blueChannel");
      console.log(data.Blue);
      createChart(
        redChannel,
        data.intensity,
        "Canal rojo",
        data.Red,
        "rgb(255, 0, 0)"
      );
      createChart(
        greenChannel,
        data.intensity,
        "Canal verde",
        data.Green,
        "rgb(0, 255, 0)"
      );
      createChart(
        blueChannel,
        data.intensity,
        "Canal azul",
        data.Blue,
        "rgb(0, 0, 255)"
      );
    });
}

function createChart(
  canvas,
  histogramValues,
  label,
  data,
  backgroundColor,
  rgb
) {
  new Chart(canvas, {
    type: "bar",
    data: {
      labels: histogramValues,
      datasets: [
        {
          label: label,
          data: data,
          borderWidth: 1,
          backgroundColor: backgroundColor,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
      plugins: {
        legend: {
          display: true,
          labels: {
            color: rgb,
          },
        },
      },
      elements: {
        bar: {
          borderColor: "#000000",
          borderWidth: 1,
          backgroundColor: rgb,
        },
      },
    },
  });
}
