const monthlyOrdersCtx = document.getElementById('monthlyOrdersChart').getContext('2d');
new Chart(monthlyOrdersCtx, {
    type: 'line',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
            label: 'Monthly Orders',
            data: [65, 59, 80, 81, 56, 55],
            borderColor: 'rgb(59, 130, 246)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


const roboConsumptionCtx = document.getElementById('roboConsumptionChart').getContext('2d');
new Chart(roboConsumptionCtx, {
    type: 'bar',
    data: {
        labels: ['Robo 1', 'Robo 2'],
        datasets: [{
            label: 'Consumption',
            data: [150, 150],
            backgroundColor: [
                'rgba(59, 130, 246, 0.6)',
                'rgba(16, 185, 129, 0.6)'
            ],
            borderColor: [
                'rgb(59, 130, 246)',
                'rgb(16, 185, 129)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


const productConsumptionCtx = document.getElementById('productConsumptionChart').getContext('2d');
new Chart(productConsumptionCtx, {
    type: 'doughnut',
    data: {
        labels: ['Product A', 'Product B', 'Product C', 'Product D'],
        datasets: [{
            label: 'Product Consumption',
            data: [300, 50, 100, 80],
            backgroundColor: [
                'rgba(59, 130, 246, 0.6)',
                'rgba(16, 185, 129, 0.6)',
                'rgba(251, 191, 36, 0.6)',
                'rgba(236, 72, 153, 0.6)'
            ],
            hoverOffset: 8
        }]
    },
    options: {
        responsive: true
    }
});