// Dashboard functionality
let scoreChart = null;

// Load evaluation report when page loads
document.addEventListener('DOMContentLoaded', loadEvaluationReport);

function loadEvaluationReport() {
    fetch('/api/evaluation-report')
        .then(response => response.json())
        .then(data => {
            displayReportData(data);
        })
        .catch(error => {
            console.error('Error loading report:', error);
            displayEmptyDashboard();
        });
}

function displayReportData(report) {
    // Summary Statistics
    document.getElementById('totalResumes').textContent = report.summary.total_resumes;
    document.getElementById('totalJobs').textContent = report.summary.total_jobs;
    document.getElementById('avgScore').textContent = report.summary.average_match_score.toFixed(2) + '%';
    document.getElementById('totalMatches').textContent = report.summary.total_matches_evaluated;

    // Detailed Statistics
    const stats = report.detailed_metrics.statistics;
    document.getElementById('meanScore').textContent = stats.mean_score.toFixed(2) + '%';
    document.getElementById('medianScore').textContent = stats.median_score.toFixed(2) + '%';
    document.getElementById('minScore').textContent = stats.min_score.toFixed(2) + '%';
    document.getElementById('maxScore').textContent = stats.max_score.toFixed(2) + '%';
    document.getElementById('stdDev').textContent = stats.std_dev.toFixed(4);

    // Role-Based Analysis
    const roleAnalysis = report.detailed_metrics.role_analysis;
    document.getElementById('sameRoleCount').textContent = roleAnalysis.same_role_matches;
    document.getElementById('sameRoleAvg').textContent = roleAnalysis.same_role_avg_score.toFixed(2) + '%';
    document.getElementById('diffRoleCount').textContent = roleAnalysis.different_role_matches;
    document.getElementById('diffRoleAvg').textContent = roleAnalysis.different_role_avg_score.toFixed(2) + '%';

    // Observations
    const observationsList = document.getElementById('observationsList');
    observationsList.innerHTML = '';
    report.observations.forEach(obs => {
        const div = document.createElement('div');
        div.className = 'observation-item';
        div.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <p>${obs}</p>
        `;
        observationsList.appendChild(div);
    });

    // Score Chart
    createScoreChart(report.detailed_metrics.score_distribution);

    // Download Report Button
    document.getElementById('downloadReport').addEventListener('click', () => {
        downloadReport(report);
    });
}

function createScoreChart(scoreDistribution) {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    
    // Create histogram data
    const bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    const counts = new Array(bins.length - 1).fill(0);
    
    // Count scores in each bin
    Object.values(scoreDistribution).forEach(score => {
        for (let i = 0; i < bins.length - 1; i++) {
            if (score >= bins[i] && score < bins[i + 1]) {
                counts[i]++;
                break;
            }
        }
        // Handle edge case for 100
        if (score === 100) {
            counts[counts.length - 1]++;
        }
    });

    const labels = bins.slice(0, -1).map((b, i) => `${b}-${bins[i + 1]}%`);

    if (scoreChart) {
        scoreChart.destroy();
    }

    scoreChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Matches',
                data: counts,
                backgroundColor: 'rgba(37, 99, 235, 0.6)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 2,
                borderRadius: 4,
                hoverBackgroundColor: 'rgba(37, 99, 235, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function downloadReport(report) {
    const dataStr = JSON.stringify(report, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'evaluation_report.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function displayEmptyDashboard() {
    // Display empty state message
    document.querySelector('.dashboard-section').innerHTML = `
        <div class="empty-state">
            <i class="fas fa-inbox"></i>
            <h2>No data available</h2>
            <p>Please run the main.py script first to generate the evaluation report.</p>
            <p style="margin-top: 1rem;">Run: <code>python main.py</code></p>
        </div>
    `;
}
