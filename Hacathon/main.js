// main.js - Central state management & API connector
function getStoredUser() {
    try {
        const u = JSON.parse(localStorage.getItem('user') || '{}');
        if (u.id && u.name) return u;
    } catch (e) {}
    return { id: 1, name: 'Avinash', streak: 7, xp: 1250 };
}

class LearningSystem {
    constructor() {
        this.user = getStoredUser();
        const origin = (typeof window !== 'undefined' && window.location.origin && !window.location.origin.startsWith('file')) ? window.location.origin : 'http://localhost:5001';
        this.apiBase = origin.replace(/\/$/, '') + '/api';
        this.state = {
            topics: [],
            masteryMap: {},
            recommendations: {},
            leaderboard: []
        };
        this.init();
    }

    async init() {
        await this.loadUserData();
        await this.loadTopics();
        this.renderDashboard();
        this.startStreakTimer();
        this.bindEvents();
        this.renderDashboardExtras();
    }

    // 🔗 API Calls
    async apiCall(endpoint, options = {}) {
        try {
            const token = localStorage.getItem('token');
            const headers = { 'Content-Type': 'application/json', ...options.headers };
            if (token) headers['Authorization'] = 'Bearer ' + token;
            const res = await fetch(`${this.apiBase}${endpoint}`, { ...options, headers });
            return await res.json();
        } catch (error) {
            console.error('API Error:', error);
            return { error: 'Connection failed - using demo mode' };
        }
    }

    async loadUserData() {
        const data = await this.apiCall(`/user/${this.user.id}`);
        if (data && data.id) {
            this.user = { ...this.user, ...data };
            this.state.masteryMap = data.mastery_map || {};
            if ((data.theme || '').toLowerCase() === 'dark') document.body.classList.add('dark-mode');
        }
    }

    async loadTopics() {
        const data = await this.apiCall('/topics');
        this.state.topics = Array.isArray(data) ? data : [];
    }

    async updateProgress(topicId, score) {
        const result = await this.apiCall(`/progress/${this.user.id}/${topicId}`, {
            method: 'POST',
            body: JSON.stringify({ score })
        });
        
        if (result.success) {
            this.state.masteryMap[topicId] = score;
            this.renderWeakTopics();
            this.updateXP(score);
        }
    }

    updateXP(score) {
        const xpGain = Math.floor(score / 10);
        this.user.xp += xpGain;
        this.user.streak++;
        this.renderDashboard();
    }

    // 🎨 Rendering Functions
    renderDashboard() {
        this.renderRecommendations();
        this.renderProgressChart();
        this.renderWeakTopics();
        this.updateStreakCounter();
    }

    renderRecommendations() {
        const recsEl = document.getElementById('recommendations');
        if (!recsEl) return;

        // Try AI first, fallback to rule-based
        this.getRecommendations().then(recommendations => {
            recsEl.innerHTML = `
                <div class="text-left p-8">
                    <div class="flex items-center mb-6">
                        <div class="w-12 h-12 bg-gradient-to-r from-green-400 to-blue-500 rounded-2xl flex items-center justify-center mr-4">
                            <span class="text-white font-bold">🤖</span>
                        </div>
                        <div>
                            <h3 class="text-2xl font-bold text-gray-800">${recommendations.next_topic}</h3>
                            <p class="text-sm text-gray-500">AI Recommended • ${recommendations.estimated_completion}</p>
                        </div>
                    </div>
                    <div class="space-y-3 mb-8">
                        ${recommendations.daily_plan.map((day, i) => `
                            <div class="flex items-center p-4 bg-white/50 backdrop-blur-sm rounded-xl shadow-sm border border-white/50 hover:shadow-md transition-all">
                                <span class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl flex items-center justify-center mr-4">${i+1}</span>
                                <span class="text-gray-700">${day}</span>
                            </div>
                        `).join('')}
                    </div>
                    <button onclick="learningSystem.startTopic('${recommendations.next_topic}')" 
                            class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 px-8 rounded-2xl font-bold text-lg shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300">
                        🚀 Start Learning Path
                    </button>
                </div>
            `;
        });
    }

    async getRecommendations() {
        try {
            const data = await this.apiCall(`/recommendations/${this.user.id}`);
            if (data.error) throw new Error(data.error);
            const rec = data.recommendations;
            return typeof rec === 'string' ? JSON.parse(rec) : rec;
        } catch {
            // Fallback rule-based recommendations
            const weakTopics = Object.entries(this.state.masteryMap)
                .filter(([_, score]) => score < 60)
                .sort((a, b) => a[1] - b[1]);
            
            return {
                next_topic: weakTopics[0]?.[0] || 'Arrays',
                daily_plan: [
                    `Day 1: ${weakTopics[0]?.[0] || 'Arrays'} basics (45min)`,
                    'Day 2: Practice problems (60min)',
                    'Day 3: Quiz + Review (30min)'
                ],
                estimated_completion: '2.5 hours'
            };
        }
    }

    renderProgressChart() {
        const scores = Object.values(this.state.masteryMap);
        const canvas = document.getElementById('progressChart');
        if (!canvas || typeof Chart === 'undefined') return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Mastered (80+)', 'Good (60-79)', 'Needs Work (<60)'],
                datasets: [{
                    data: [
                        scores.filter(s => s >= 80).length,
                        scores.filter(s => s >= 60 && s < 80).length,
                        scores.filter(s => s < 60).length
                    ],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: { 
                    legend: { 
                        position: 'bottom',
                        labels: { padding: 20, usePointStyle: true }
                    }
                },
                cutout: '65%',
                animation: {
                    animateRotate: true,
                    duration: 2000
                }
            }
        });
    }

    renderWeakTopics() {
        const weakEl = document.getElementById('weakTopics');
        if (!weakEl) return;

        const weakTopics = Object.entries(this.state.masteryMap)
            .filter(([_, score]) => score < 60)
            .map(([topicId, score]) => {
                const topic = this.state.topics.find(t => t.id == topicId);
                return { topic: topic?.name || topicId, score };
            });

        if (weakTopics.length === 0) {
            weakEl.innerHTML = `
                <div class="text-center py-12 text-green-600">
                    <div class="w-20 h-20 bg-green-100 rounded-3xl mx-auto mb-4 flex items-center justify-center">
                        ✅
                    </div>
                    <h4 class="text-xl font-bold mb-2">No weak topics!</h4>
                    <p class="text-gray-500">You're doing great! Keep the momentum.</p>
                </div>
            `;
        } else {
            weakEl.innerHTML = weakTopics.map(({ topic, score }) => `
                <div class="p-6 bg-gradient-to-r from-red-50 to-orange-50 rounded-2xl border-l-4 border-red-400 hover:shadow-md transition-all">
                    <div class="flex justify-between items-start mb-3">
                        <h4 class="font-bold text-lg text-gray-800">${topic}</h4>
                        <span class="px-3 py-1 bg-red-100 text-red-800 text-sm font-bold rounded-full">${score}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-3 mb-3 overflow-hidden">
                        <div class="progress-bar" style="width: ${score}%"></div>
                    </div>
                    <button onclick="learningSystem.startQuiz('${String(topic).replace(/'/g, "\\'")}')" 
                            class="text-red-600 hover:text-red-800 font-semibold hover:underline">
                        🔄 Revise Now
                    </button>
                </div>
            `).join('');
        }
    }

    updateStreakCounter() {
        document.querySelectorAll('.streak-badge').forEach(el => {
            el.textContent = `🔥 ${this.user.streak} day streak`;
        });
    }

    // 🕐 Real-time Features
    startStreakTimer() {
        setInterval(() => {
            const now = new Date();
            const hour = now.getHours();
            // Reset streak at midnight
            if (hour === 0) {
                this.user.streak = 0;
                this.renderDashboard();
            }
        }, 60000);
    }

    // 🎮 Interactive Features
    startTopic(topicName) {
        // Navigate to subject page with topic
        window.location.href = `subject.html?topic=${encodeURIComponent(topicName)}`;
    }

    startQuiz(topicIdOrName) {
        this.showQuizModal(topicIdOrName);
    }

    showQuizModal(topicIdOrName) {
        const topic = this.state.topics.find(t => t.id == topicIdOrName || t.name === topicIdOrName);
        if (!topic) return;

        const modal = `
            <div id="quizModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-6">
                <div class="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
                    <div class="p-8 border-b">
                        <h2 class="text-2xl font-bold text-gray-800 mb-2">${topic.name} Quiz</h2>
                        <p class="text-gray-600">Test your mastery (10 questions)</p>
                    </div>
                    <div id="quizQuestions" class="p-8 space-y-6">
                        ${(topic.quiz || []).slice(0, 3).map((q, i) => `
                            <div class="space-y-2">
                                <h4 class="font-semibold text-gray-800">Q${i+1}. ${q.q}</h4>
                                <div class="space-y-2 ml-4">
                                    ${q.options.map((opt, optIdx) => `
                                        <label class="flex items-center p-3 bg-gray-50 rounded-xl hover:bg-gray-100 cursor-pointer transition-all">
                                            <input type="radio" name="q${i}" value="${optIdx}" class="w-5 h-5 text-blue-600">
                                            <span class="ml-3 font-medium">${opt}</span>
                                        </label>
                                    `).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    <div class="p-8 border-t bg-gray-50 rounded-b-3xl">
                        <button onclick="learningSystem.submitQuiz('${topic.id}')" 
                                class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 px-8 rounded-2xl font-bold shadow-lg hover:shadow-2xl">
                            Submit & Get Score
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modal);
    }

    submitQuiz(topicId) {
        const formData = new FormData();
        const selected = document.querySelectorAll('input[type="radio"]:checked');
        let score = 0;
        
        // Simple scoring (demo)
        score = selected.length * 25; // 25% per question
        
        document.getElementById('quizModal').remove();
        this.updateProgress(topicId, score);
        
        // Show result toast
        this.showToast(`Great job! ${score}% on ${topicId}`, score > 70 ? 'success' : 'warning');
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `fixed top-6 right-6 p-6 rounded-2xl shadow-2xl transform translate-x-full transition-all duration-300 z-50 ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'warning' ? 'bg-orange-500 text-white' : 'bg-blue-500 text-white'
        }`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.classList.remove('translate-x-full'), 100);
        setTimeout(() => {
            toast.classList.add('translate-x-full');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Event Listeners
    bindEvents() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="continue"]')) {
                this.startTopic('Arrays');
            }
        });
    }

    // Dashboard extras: downloads, recent test scores
    renderDashboardExtras() {
        const uid = this.user.id;
        const dl = document.getElementById('downloads-list');
        if (dl) {
            this.apiCall('/downloads/' + uid).then(data => {
                if (Array.isArray(data) && data.length) dl.innerHTML = data.map(d => '<li>' + d.resource_name + '</li>').join('');
                else if (dl) dl.innerHTML = '<li class="text-muted">No downloads yet</li>';
            }).catch(() => { if (dl) dl.innerHTML = '<li class="text-muted">No downloads yet</li>'; });
        }
        const ts = document.getElementById('test-scores-list');
        if (ts) {
            this.apiCall('/test-scores/' + uid).then(data => {
                if (Array.isArray(data) && data.length) ts.innerHTML = data.map(d => '<li>' + d.topic_name + ': ' + d.score + '%</li>').join('');
                else ts.innerHTML = '<li class="text-muted">No tests yet</li>';
            }).catch(() => { ts.innerHTML = '<li class="text-muted">No tests yet</li>'; });
        }
    }
}

// 🌟 Global instance (only on pages that need dashboard logic)
if (document.getElementById('recommendations') || document.getElementById('progressChart') || document.getElementById('weakTopics')) {
    const learningSystem = new LearningSystem();
    window.learningSystem = learningSystem;
}
