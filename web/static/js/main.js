/**
 * LLM Career Placement Engine - Main JavaScript
 * Professional UI interactions and API integration
 */

// ============================================================================
// DOM ELEMENTS
// ============================================================================

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
const jobModal = document.getElementById('jobModal');

// ============================================================================
// STATE
// ============================================================================

let currentResumeSkills = null;
let currentMatches = [];

// ============================================================================
// UPLOAD HANDLING
// ============================================================================

uploadArea.addEventListener('click', () => resumeInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        resumeInput.files = files;
        uploadResume();
    }
});

resumeInput.addEventListener('change', uploadResume);

function uploadResume() {
    const file = resumeInput.files[0];
    if (!file) return;

    // Show loading
    uploadArea.classList.add('hidden');
    uploadStatus.classList.remove('hidden');
    successMessage.classList.add('hidden');
    errorMessage.classList.add('hidden');

    const formData = new FormData();
    formData.append('resume', file);

    fetch('/api/upload-resume', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        uploadStatus.classList.add('hidden');
        
        if (data.success) {
            document.getElementById('fileName').textContent = `✓ ${data.filename}`;
            successMessage.classList.remove('hidden');
            
            currentResumeSkills = data.extracted_skills;
            displayExtractedSkills(data.extracted_skills);
            skillsSection.classList.remove('hidden');
            
            // Smooth scroll
            skillsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            document.getElementById('errorText').textContent = data.error || 'Unknown error';
            errorMessage.classList.remove('hidden');
            uploadArea.classList.remove('hidden');
        }
    })
    .catch(error => {
        uploadStatus.classList.add('hidden');
        document.getElementById('errorText').textContent = `Network error: ${error.message}`;
        errorMessage.classList.remove('hidden');
        uploadArea.classList.remove('hidden');
    });
}

// ============================================================================
// SKILLS DISPLAY
// ============================================================================

function displayExtractedSkills(skills) {
    // Technical Skills
    const technicalSkills = document.getElementById('technicalSkills');
    technicalSkills.innerHTML = '';
    if (skills.technical_skills && skills.technical_skills.length > 0) {
        skills.technical_skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'badge badge-primary';
            span.textContent = skill;
            const li = document.createElement('li');
            li.appendChild(span);
            li.style.marginBottom = '0.5rem';
            technicalSkills.appendChild(li);
        });
    } else {
        technicalSkills.innerHTML = '<li><span class="badge badge-primary">Not detected</span></li>';
    }

    // Experience Level
    const experienceLevel = document.getElementById('experienceLevel');
    experienceLevel.textContent = skills.experience_level || 'Not detected';

    // Domains
    const domains = document.getElementById('domains');
    domains.innerHTML = '';
    if (skills.domain_expertise && skills.domain_expertise.length > 0) {
        skills.domain_expertise.forEach(domain => {
            const span = document.createElement('span');
            span.className = 'badge badge-primary';
            span.textContent = domain;
            const li = document.createElement('li');
            li.appendChild(span);
            li.style.marginBottom = '0.5rem';
            domains.appendChild(li);
        });
    } else {
        domains.innerHTML = '<li><span class="badge badge-primary">Not detected</span></li>';
    }

    // Tools
    const tools = document.getElementById('tools');
    tools.innerHTML = '';
    if (skills.tools && skills.tools.length > 0) {
        skills.tools.forEach(tool => {
            const span = document.createElement('span');
            span.className = 'badge badge-primary';
            span.textContent = tool;
            const li = document.createElement('li');
            li.appendChild(span);
            li.style.marginBottom = '0.5rem';
            tools.appendChild(li);
        });
    } else {
        tools.innerHTML = '<li><span class="badge badge-primary">Not detected</span></li>';
    }
}

// ============================================================================
// JOB MATCHING
// ============================================================================

matchButton.addEventListener('click', matchJobs);

function matchJobs() {
    if (!currentResumeSkills) {
        showAlert('Please upload a resume first', 'error');
        return;
    }

    matchingStatus.classList.remove('hidden');
    resultsSection.classList.add('hidden');

    fetch('/api/match-jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ extracted_skills: currentResumeSkills })
    })
    .then(response => response.json())
    .then(data => {
        matchingStatus.classList.add('hidden');
        
        if (data.success) {
            currentMatches = data.matches;
            displayMatches(data.matches);
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            showAlert(data.error || 'Failed to match jobs', 'error');
        }
    })
    .catch(error => {
        matchingStatus.classList.add('hidden');
        showAlert(`Network error: ${error.message}`, 'error');
    });
}

function displayMatches(matches) {
    matchesContainer.innerHTML = '';
    
    if (matches.length === 0) {
        matchesContainer.innerHTML = `
            <div class="text-center" style="grid-column: 1/-1; padding: 3rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
                <h4>No matches found</h4>
                <p style="color: var(--text-light);">Try uploading a different resume</p>
            </div>
        `;
        return;
    }

    matches.forEach((match) => {
        const score = match.overall_score;
        const scoreClass = score >= 80 ? 'high' : score >= 60 ? 'medium' : 'low';
        
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h4>${match.job_role}</h4>
                    <p style="color: var(--text-light); margin: 0;">${match.job_company}</p>
                </div>
                <div class="score-badge ${scoreClass}">${score}%</div>
            </div>
            
            <div class="grid grid-2" style="gap: 1rem; margin: 1rem 0;">
                ${getComponentScoresHTML(match.component_scores)}
            </div>
            
            <button class="btn btn-primary btn-block" onclick="viewJobDetails(${match.job_index})" style="margin-top: 1rem;">
                <i class="fas fa-external-link-alt"></i> View Details
            </button>
        `;
        matchesContainer.appendChild(card);
    });
}

function getComponentScoresHTML(scores) {
    const components = [
        { name: 'Skills', key: 'skill_overlap' },
        { name: 'Semantic', key: 'semantic_similarity' },
        { name: 'Experience', key: 'experience_match' },
        { name: 'Domain', key: 'domain_match' }
    ];

    return components.map(comp => {
        const value = scores[comp.key] || 0;
        return `
            <div style="text-align: center; padding: 0.75rem; background: var(--gray-50); border-radius: var(--radius);">
                <div style="font-size: 0.875rem; color: var(--text-light); margin-bottom: 0.25rem;">${comp.name}</div>
                <div style="font-weight: 600; color: var(--primary); font-size: 1.25rem;">${Math.round(value)}%</div>
            </div>
        `;
    }).join('');
}

// ============================================================================
// JOB DETAILS MODAL
// ============================================================================

function viewJobDetails(jobIndex) {
    fetch(`/api/job-details/${jobIndex}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayJobModal(data.job);
            } else {
                showAlert(data.error || 'Failed to load job details', 'error');
            }
        })
        .catch(error => showAlert(`Network error: ${error.message}`, 'error'));
}

function displayJobModal(job) {
    const jobDetails = document.getElementById('jobDetails');
    
    jobDetails.innerHTML = `
        <div>
            <div style="margin-bottom: 2rem;">
                <h3 style="margin: 0 0 0.5rem 0;">${job.role}</h3>
                <p style="margin: 0; color: var(--text-light); font-size: 1.125rem;">
                    <i class="fas fa-building"></i> ${job.company}
                </p>
            </div>

            <div style="margin-bottom: 2rem;">
                <h5 style="margin-bottom: 1rem;">📋 Description</h5>
                <p style="color: var(--text-light);">${job.description}</p>
            </div>

            <div style="margin-bottom: 2rem;">
                <h5 style="margin-bottom: 1rem;">✓ Required Skills</h5>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    ${job.requirements.map(req => `<span class="badge badge-success">${req}</span>`).join('')}
                </div>
            </div>

            <div style="margin-bottom: 2rem;">
                <h5 style="margin-bottom: 1rem;">⭐ Nice to Have</h5>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    ${job.nice_to_have.map(nh => `<span class="badge badge-warning">${nh}</span>`).join('')}
                </div>
            </div>

            <div class="grid grid-2" style="gap: 2rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--gray-200);">
                <div>
                    <h6 style="color: var(--text-light); margin-bottom: 0.5rem;">Experience Required</h6>
                    <p style="font-weight: 600; margin: 0;">${job.experience}</p>
                </div>
                <div>
                    <h6 style="color: var(--text-light); margin-bottom: 0.5rem;">Salary Range</h6>
                    <p style="font-weight: 600; margin: 0;">${job.salary}</p>
                </div>
            </div>
        </div>
    `;
    
    jobModal.classList.add('active');
}

function closeModal() {
    jobModal.classList.remove('active');
}

jobModal.addEventListener('click', (e) => {
    if (e.target === jobModal) closeModal();
});

// ============================================================================
// SCORE FILTERING
// ============================================================================

scoreFilter.addEventListener('input', (e) => {
    scoreValue.textContent = e.target.value + '%';
    filterMatches(parseInt(e.target.value));
});

function filterMatches(minScore) {
    const cards = document.querySelectorAll('#matchesContainer .card');
    let visibleCount = 0;

    cards.forEach(card => {
        const scoreBadge = card.querySelector('.score-badge');
        const score = parseInt(scoreBadge.textContent);
        
        if (score >= minScore) {
            card.style.display = '';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    if (visibleCount === 0) {
        const emptyMsg = document.createElement('div');
        emptyMsg.className = 'text-center';
        emptyMsg.style.gridColumn = '1/-1';
        emptyMsg.style.padding = '2rem';
        emptyMsg.innerHTML = `
            <div style="font-size: 2rem; margin-bottom: 1rem;">🔍</div>
            <p>No matches found with score ≥ ${minScore}%</p>
        `;
        
        // Only show message if not already displayed
        if (!matchesContainer.querySelector('.text-center')) {
            matchesContainer.appendChild(emptyMsg);
        }
    }
}

// ============================================================================
// UTILITIES
// ============================================================================

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <div class="alert-icon">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        </div>
        <p style="margin: 0;">${message}</p>
    `;
    
    // Insert at top of main
    const main = document.querySelector('main');
    main.insertBefore(alert, main.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => alert.remove(), 5000);
}
