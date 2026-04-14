// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const resumeInput = document.getElementById('resumeInput');
const uploadStatus = document.getElementById('uploadStatus');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');
const skillsSection = document.getElementById('skillsSection');
const resultsSection = document.getElementById('resultsSection');
const matchButton = document.getElementById('matchButton');
const matchingStatus = document.getElementById('matchingStatus');
const matchesContainer = document.getElementById('matchesContainer');
const scoreFilter = document.getElementById('scoreFilter');
const scoreValue = document.getElementById('scoreValue');

let currentResumeSkills = null;
let currentMatches = [];

// Upload Area Events
uploadArea.addEventListener('click', () => resumeInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.backgroundColor = 'rgba(37, 99, 235, 0.05)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.backgroundColor = 'var(--light-bg)';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';
    uploadArea.style.backgroundColor = 'var(--light-bg)';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        resumeInput.files = files;
        uploadResume();
    }
});

resumeInput.addEventListener('change', uploadResume);

// Upload Resume
function uploadResume() {
    const file = resumeInput.files[0];
    if (!file) return;

    // Show loading state
    uploadArea.style.display = 'none';
    uploadStatus.style.display = 'flex';
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';

    const formData = new FormData();
    formData.append('resume', file);

    fetch('/api/upload-resume', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        uploadStatus.style.display = 'none';
        
        if (data.success) {
            // Show success message
            document.getElementById('fileName').textContent = data.filename;
            successMessage.style.display = 'flex';
            
            // Display extracted skills
            currentResumeSkills = data.extracted_skills;
            displayExtractedSkills(data.extracted_skills);
            skillsSection.style.display = 'block';
        } else {
            // Show error message
            document.getElementById('errorText').textContent = data.error || 'An error occurred';
            errorMessage.style.display = 'flex';
            uploadArea.style.display = 'block';
        }
    })
    .catch(error => {
        uploadStatus.style.display = 'none';
        document.getElementById('errorText').textContent = 'Network error: ' + error.message;
        errorMessage.style.display = 'flex';
        uploadArea.style.display = 'block';
    });
}

// Display Extracted Skills
function displayExtractedSkills(skills) {
    // Technical Skills
    const technicalSkills = document.getElementById('technicalSkills');
    technicalSkills.innerHTML = '';
    if (skills.technical_skills && skills.technical_skills.length > 0) {
        skills.technical_skills.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            technicalSkills.appendChild(li);
        });
    } else {
        technicalSkills.innerHTML = '<li>No technical skills detected</li>';
    }

    // Experience Level
    const experienceLevel = document.getElementById('experienceLevel');
    experienceLevel.textContent = skills.experience_level || 'Not detected';

    // Domains
    const domains = document.getElementById('domains');
    domains.innerHTML = '';
    if (skills.domain_expertise && skills.domain_expertise.length > 0) {
        skills.domain_expertise.forEach(domain => {
            const li = document.createElement('li');
            li.textContent = domain;
            domains.appendChild(li);
        });
    } else {
        domains.innerHTML = '<li>No domains detected</li>';
    }

    // Tools & Technologies
    const tools = document.getElementById('tools');
    tools.innerHTML = '';
    if (skills.tools && skills.tools.length > 0) {
        skills.tools.forEach(tool => {
            const li = document.createElement('li');
            li.textContent = tool;
            tools.appendChild(li);
        });
    } else {
        tools.innerHTML = '<li>No tools detected</li>';
    }
}

// Match Jobs
matchButton.addEventListener('click', matchJobs);

function matchJobs() {
    if (!currentResumeSkills) {
        alert('Please upload a resume first');
        return;
    }

    matchingStatus.style.display = 'flex';
    resultsSection.style.display = 'none';

    fetch('/api/match-jobs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            extracted_skills: currentResumeSkills
        })
    })
    .then(response => response.json())
    .then(data => {
        matchingStatus.style.display = 'none';
        
        if (data.success) {
            currentMatches = data.matches;
            displayMatches(data.matches);
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + (data.error || 'Failed to match jobs'));
        }
    })
    .catch(error => {
        matchingStatus.style.display = 'none';
        alert('Network error: ' + error.message);
    });
}

// Display Matches
function displayMatches(matches) {
    matchesContainer.innerHTML = '';
    
    if (matches.length === 0) {
        matchesContainer.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>No matches found</p></div>';
        return;
    }

    matches.forEach((match, index) => {
        const scorePercentage = match.overall_score;
        let scoreBadgeClass = 'score-badge';
        
        if (scorePercentage >= 80) {
            scoreBadgeClass += ' high';
        } else if (scorePercentage >= 60) {
            scoreBadgeClass += ' medium';
        } else {
            scoreBadgeClass += ' low';
        }

        const card = document.createElement('div');
        card.className = 'match-card';
        card.innerHTML = `
            <div class="match-header">
                <div class="match-info">
                    <h3>${match.job_role}</h3>
                    <p>${match.job_company}</p>
                </div>
                <div class="${scoreBadgeClass}">${scorePercentage}%</div>
            </div>
            
            <div class="component-scores">
                ${getComponentScoresHTML(match.component_scores)}
            </div>
            
            <button class="btn btn-primary view-details" onclick="viewJobDetails(${match.job_index})">
                <i class="fas fa-search"></i> View Details
            </button>
        `;
        matchesContainer.appendChild(card);
    });
}

// Get Component Scores HTML
function getComponentScoresHTML(scores) {
    const components = [
        { name: 'Skill', key: 'skill_overlap' },
        { name: 'Semantic', key: 'semantic_similarity' },
        { name: 'Experience', key: 'experience_match' },
        { name: 'Domain', key: 'domain_match' }
    ];

    return components.map(comp => {
        const value = scores[comp.key] || 0;
        return `
            <div class="component">
                <span class="component-name">${comp.name}</span>
                <span class="component-value">${Math.round(value)}%</span>
            </div>
        `;
    }).join('');
}

// View Job Details
function viewJobDetails(jobIndex) {
    fetch(`/api/job-details/${jobIndex}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayJobModal(data.job);
            } else {
                alert('Error: ' + (data.error || 'Failed to load job details'));
            }
        })
        .catch(error => alert('Network error: ' + error.message));
}

// Display Job Modal
function displayJobModal(job) {
    const modal = document.getElementById('jobModal');
    const jobDetails = document.getElementById('jobDetails');
    
    jobDetails.innerHTML = `
        <div>
            <h2>${job.role}</h2>
            <p><strong>Company:</strong> ${job.company}</p>
            
            <div class="job-detail">
                <h4><i class="fas fa-briefcase"></i> Description</h4>
                <p>${job.description}</p>
            </div>
            
            <div class="job-detail">
                <h4><i class="fas fa-check"></i> Required Skills</h4>
                <ul>
                    ${job.requirements.map(req => `<li>${req}</li>`).join('')}
                </ul>
            </div>
            
            <div class="job-detail">
                <h4><i class="fas fa-star"></i> Nice to Have</h4>
                <ul>
                    ${job.nice_to_have.map(nh => `<li>${nh}</li>`).join('')}
                </ul>
            </div>
            
            <div class="job-detail">
                <h4><i class="fas fa-chart-line"></i> Experience Required</h4>
                <p>${job.experience_required}</p>
            </div>
            
            <div class="job-detail">
                <h4><i class="fas fa-dollar-sign"></i> Salary Range</h4>
                <p>${job.salary_range}</p>
            </div>
        </div>
    `;
    
    modal.style.display = 'block';
}

// Close Modal
const modal = document.getElementById('jobModal');
const closeBtn = document.querySelector('.close');

closeBtn.onclick = function() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Score Filter
scoreFilter.addEventListener('input', (e) => {
    scoreValue.textContent = e.target.value;
    filterMatches(parseInt(e.target.value));
});

function filterMatches(minScore) {
    const cards = document.querySelectorAll('.match-card');
    let visibleCount = 0;

    cards.forEach(card => {
        const scoreBadge = card.querySelector('.score-badge');
        const score = parseInt(scoreBadge.textContent);
        
        if (score >= minScore) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    if (visibleCount === 0) {
        matchesContainer.innerHTML = '<div class="empty-state"><i class="fas fa-filter"></i><p>No matches with score >= ' + minScore + '%</p></div>';
    }
}
