function readChartData(id) {
    const element = document.getElementById(id);

    if (!element) {
        return [];
    }

    try {
        return JSON.parse(element.textContent);
    } catch (error) {
        return [];
    }
}

function buildParticipationChart() {
    const canvas = document.getElementById('participationChart');
    const statistics = readChartData('election-statistics-data');

    if (!canvas || !statistics.length || typeof Chart === 'undefined') {
        return;
    }

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: statistics.map((election) => election.title),
            datasets: [
                {
                    label: 'Voted',
                    data: statistics.map((election) => election.voted),
                    backgroundColor: '#16794c',
                },
                {
                    label: 'Not Voted',
                    data: statistics.map((election) => election.not_voted),
                    backgroundColor: '#b42318',
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                    },
                },
            },
        },
    });
}

function buildLiveElectionCharts() {
    const elections = readChartData('live-election-count-data');

    if (!elections.length || typeof Chart === 'undefined') {
        return;
    }

    document.querySelectorAll('[data-live-election-chart]').forEach((canvas) => {
        const electionId = Number(canvas.dataset.electionId);
        const election = elections.find((item) => item.id === electionId);

        if (!election || !election.labels.length) {
            return;
        }

        new Chart(canvas, {
            type: 'bar',
            data: {
                labels: election.labels,
                datasets: [
                    {
                        label: 'Live Votes',
                        data: election.votes,
                        backgroundColor: [
                            '#1255a4',
                            '#16794c',
                            '#b42318',
                            '#b7791f',
                            '#7a3fb1',
                            '#087f8c',
                            '#475467',
                        ],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0,
                        },
                    },
                },
            },
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    buildParticipationChart();
    buildLiveElectionCharts();
});
