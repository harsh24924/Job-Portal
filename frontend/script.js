let currentResumeData = null;
let currentJobData = null;

// DOM Elements
const resumeForm = document.getElementById('resumeForm');
const recommendationsContainer = document.getElementById('recommendationsContainer');
const sidePanel = document.getElementById('sidePanel');
const overlay = document.getElementById('overlay');
const closePanel = document.getElementById('closePanel');
const jobDetails = document.getElementById('jobDetails');

// Form submission handler
resumeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(resumeForm);
    const resumeData = {
        summary: formData.get('summary'),
        skills: formData.get('skills'),
        education: formData.get('education'),
        experience: formData.get('experience'),
        projects: formData.get('projects')
    };
    
    currentResumeData = resumeData;
    await getRecommendations(resumeData);
});

// Get recommendations from API
async function getRecommendations(resumeData) {
    const submitBtn = resumeForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Loading...';
    
    recommendationsContainer.innerHTML = '<div class="loading">Fetching recommendations</div>';
    
    try {
        const response = await fetch('/recommend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(resumeData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch recommendations');
        }
        
        const jobs = await response.json();
        displayRecommendations(jobs);
    } catch (error) {
        console.error('Error:', error);
        recommendationsContainer.innerHTML = `
            <div class="empty-state">
                <p style="color: #ff5252;">Error fetching recommendations. Please try again.</p>
            </div>
        `;
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Get Recommendations';
    }
}

// Display recommendations in the UI
function displayRecommendations(jobs) {
    if (!jobs || jobs.length === 0) {
        recommendationsContainer.innerHTML = `
            <div class="empty-state">
                <p>No recommendations found. Try updating your resume.</p>
            </div>
        `;
        return;
    }
    
    recommendationsContainer.innerHTML = jobs.map((job, index) => `
        <div class="job-item" data-index="${index}">
            <h3>${escapeHtml(job.title)}</h3>
            <div class="company">${escapeHtml(job.company)}</div>
            <div class="location">${escapeHtml(job.location)}</div>
        </div>
    `).join('');
    
    // Add click handlers to job items
    document.querySelectorAll('.job-item').forEach((item, index) => {
        item.addEventListener('click', () => {
            showJobDetails(jobs[index]);
        });
    });
}

// Show job details in side panel
function showJobDetails(job) {
    currentJobData = job;
    
    jobDetails.innerHTML = `
        <div class="job-detail-section">
            <h3>${escapeHtml(job.title)}</h3>
            <div class="company-name">${escapeHtml(job.company)}</div>
            <div class="job-location">${escapeHtml(job.location)}</div>
            
            <h4>Description</h4>
            <p>${escapeHtml(job.description)}</p>
            
            <h4>Requirements</h4>
            <p>${escapeHtml(job.requirements)}</p>
            
            <button class="btn-analyze" id="analyzeBtn">Analyze Match</button>
        </div>
        <div id="analysisContainer"></div>
    `;
    
    // Add analyze button handler
    document.getElementById('analyzeBtn').addEventListener('click', analyzeJob);
    
    // Show side panel
    sidePanel.classList.add('active');
    overlay.classList.add('active');
}

// Analyze job match
async function analyzeJob() {
    if (!currentResumeData || !currentJobData) {
        return;
    }
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisContainer = document.getElementById('analysisContainer');
    
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';
    
    analysisContainer.innerHTML = '<div class="loading">Analyzing your match</div>';
    
    try {
        const response = await fetch('/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job: currentJobData,
                resume: currentResumeData
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to analyze match');
        }
        
        const analysis = await response.json();
        displayAnalysis(analysis);
    } catch (error) {
        console.error('Error:', error);
        analysisContainer.innerHTML = `
            <div class="analysis-section">
                <p style="color: #ff5252;">Error analyzing match. Please try again.</p>
            </div>
        `;
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Match';
    }
}

// Display analysis results
function displayAnalysis(analysis) {
    const analysisContainer = document.getElementById('analysisContainer');
    
    const matchesHtml = analysis.matches && analysis.matches.length > 0
        ? analysis.matches.map(match => `<li>${escapeHtml(match)}</li>`).join('')
        : '<li>No matching qualifications found</li>';
    
    const missingHtml = analysis.missing && analysis.missing.length > 0
        ? analysis.missing.map(item => `<li>${escapeHtml(item)}</li>`).join('')
        : '<li>No missing qualifications</li>';
    
    analysisContainer.innerHTML = `
        <div class="analysis-section matches-section">
            <h4>✓ Matching Qualifications</h4>
            <ul>${matchesHtml}</ul>
        </div>
        <div class="analysis-section missing-section">
            <h4>⚠ Missing Qualifications</h4>
            <ul>${missingHtml}</ul>
        </div>
    `;
}

// Close side panel
function closeSidePanel() {
    sidePanel.classList.remove('active');
    overlay.classList.remove('active');
}

closePanel.addEventListener('click', closeSidePanel);
overlay.addEventListener('click', closeSidePanel);

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close panel with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidePanel.classList.contains('active')) {
        closeSidePanel();
    }
});