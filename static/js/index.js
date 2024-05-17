
// var paid = document.getElementById("paid");
// var unpaid = document.getElementById("unpaid");
var ctx6 = document.getElementById("pieChart6");
var pieChart6 = new Chart(ctx6, {
    type: 'pie',
    options: {
        rotation: -20,
        cutoutPercentage: 10,
        animation: {
            animateScale: true,
        },
        legend: {
            position: 'left',
            borderAlign: 'inner',
            labels: {
                boxWidth: 10,
                fontStyle: 'italic',
                fontColor: '#aaa',
                usePointStyle: true,
            }
        },
    },
    data: {
        labels: [
            "Paid",
            "Unpaid",
        ],
        datasets: [
            {
                data: [3, 1],
                borderWidth: 2,
                backgroundColor: [
                    'rgba(70, 215, 212, 0.2)',
                    "rgba(245, 225, 50, 0.2)",
                ],
                borderColor: [
                    '#46d8d5',
                    "#f5e132",
                ],
                hoverBackgroundColor: [
                    '#46d8d5',
                    "#f5e132",
                ]
            }]
        }
    });

// Get and Update invoice modal form

