/**
 * Dashboard JavaScript
 * Analytics and chart visualization
 */

let scoreChart = null;

document.addEventListener('DOMContentLoaded', loadEvaluationReport);

function loadEvaluationReport() {
    fetch('/api/evaluation-report')
        .then(response => response.json())
        .then(data => {
            if (data.summary) {
                displayReportData(data);
            } else {
                showEmptyDashboard();
            }
        })
        .catch(error => {
            console.error('Error loading report:', error);
            showEmptyDashboard();
        });
}

function displayReportData(report) {
    const { summary, detailed_metrics } = report;

    // Summary stats
    document.getElementById('totalResumes').textContent = summary.total_resumes;
    document.getElementById('totalJobs').textContent = summary.total_jobs;
    document.getElementById('avgScore').textContent = summary.average_match_score.toFixed(2) + '%';
    document.getElementById('totalMatches').textContent = summary.total_matches_evaluated;

    // Statistics
    const stats = detailed_metrics.statistics;
    document.getElementById('meanScore').textContent = stats.mean_score.toFixed(2) + '%';
    document.getElementById('medianScore').textContent = stats.median_score.toFixed(2) + '%';
    document.getElementById('minMaxScore').textContent = `${stats.min_score.toFixed(2)}% - ${stats.max_score.toFixed(2)}%`;
    document.getElementById('stdDev').textContent = stats.std_dev.toFixed(4);

    // Role analysis
    const roleAnalysis = detailed_metrics.role_analysis;
    document.getElementById('sameRoleCount').textContent = roleAnalysis.same_role_matches;
    document.getElementById('sameRoleAvg').textContent = roleAnalysis.same_role_avg_score.toFixed(2) + '%';
    document.getElementById('diffRoleCount').textContent = roleAnalysis.different_role_matches;
    document.getElementById('diffRoleAvg').textContent = roleAnalysis.different_role_avg_score.toFixed(2) + '%';

    // Observations
    const observationsList = document.getElementById('observationsList');
    observationsList.innerHTML = '';
    report.observations.forEach(obs => {
        const div = document.createElement('div');
        div.style.cssText = 'padding: 1rem; background: var(--gray-50); border-radius: var(--radius); display: flex; gap: 1rem;';
        div.innerHTML = `
            <i class="fas fa-lightbulb" style="color: var(--warning); margin-top: 0.25rem; flex-shrink: 0;"></i>
            <p style="margin: 0;">${obs}</p>
        `;
        observationsList.appendChild(div);
    });

    // Chart
    createScoreChart(detailed_metrics.score_distribution);
}

function createScoreChart(scoreDistribution) {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    
    if (scoreChart) {
        scoreChart.destroy();
    }

    scoreChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
            datasets: [{
                label: 'Number of Matches',
                data: generateHistogram(scoreDistribution),
                backgroundColor: 'rgba(37, 99, 235, 0.7)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 2,
                borderRadius: 4,
                hoverBackgroundColor: 'rgba(37, 99, 235, 0.9)'
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

function generateHistogram(scoreDistribution) {
    const bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
    const counts = new Array(bins.length - 1).fill(0);
    
    Object.values(scoreDistribution).forEach(score => {
        for (let i = 0; i < bins.length - 1; i++) {
            if (score >= bins[i] && score < bins[i + 1]) {
                counts[i]++;
                break;
            }
        }
        if (score === 100) {
            counts[counts.length - 1]++;
        }
    });

    return counts;
}

function showEmptyDashboard() {
    const main = document.querySelector('main');
    main.innerHTML = `
        <div class="hero">
            <h1>📊 System Analytics</h1>
        </div>
        
        <div class="card text-center" style="margin: 4rem auto; max-width: 600px;">
            <div class="card-body">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <h3>No Data Available</h3>
                <p style="color: var(--text-light);">Please run the main pipeline first:</p>
                <code style="display: block; background: var(--gray-100); padding: 1rem; border-radius: var(--radius); margin: 1rem 0; font-family: monospace;">python main.py</code>
                <p style="color: var(--text-light); font-size: 0.875rem;">This will generate the evaluation report and populate the dashboard.</p>
            </div>
        </div>
    `;
}
