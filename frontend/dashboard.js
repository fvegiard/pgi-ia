// PGI-IA Dashboard JavaScript

// Import real data
const script = document.createElement('script');
script.src = 'dashboard_real_data.js';
document.head.appendChild(script);

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Lucide icons
    lucide.createIcons();

    // Global variables
    let sidebarOpen = true;
    let unreadEmailCount = 3;
    let activeTab = 'dashboard';
    let currentProject = 'S-1086';  // Default to Kahnawake

    // Sidebar toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const logo = document.getElementById('logo');
    
    toggleBtn.addEventListener('click', function() {
        sidebarOpen = !sidebarOpen;
        if (sidebarOpen) {
            sidebar.style.width = '256px';
            sidebar.classList.remove('sidebar-collapsed');
            logo.style.opacity = '1';
            toggleBtn.innerHTML = '<i data-lucide="x" class="w-5 h-5"></i>';
        } else {
            sidebar.style.width = '80px';
            sidebar.classList.add('sidebar-collapsed');
            logo.style.opacity = '0';
            toggleBtn.innerHTML = '<i data-lucide="menu" class="w-5 h-5"></i>';
        }
        lucide.createIcons();
    });

    // Tab navigation
    const tabButtons = document.querySelectorAll('.sidebar-item[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Update active button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update active content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabName).classList.add('active');
            
            activeTab = tabName;
            
            // Update page content if needed
            if (tabName === 'emails') {
                updateEmailBadge();
            } else if (tabName === 'directives') {
                loadDirectives();
            } else if (tabName === 'notes') {
                loadNotes();
            } else if (tabName === 'photos') {
                loadPhotos();
            }
        });
    });
    
    // Project selector
    const projectSelector = document.getElementById('projectSelector');
    if (projectSelector) {
        projectSelector.addEventListener('change', function() {
            currentProject = this.value;
            updateProjectData();
        });
    }

    // Update email badge
    function updateEmailBadge() {
        const badge = document.getElementById('emailBadge');
        if (unreadEmailCount > 0) {
            badge.textContent = unreadEmailCount;
            badge.style.display = 'inline-flex';
        } else {
            badge.style.display = 'none';
        }
    }

    // Global chart instances
    let revenueChart = null;
    let projectChart = null;
    
    // Initialize charts
    function initCharts() {
        // Revenue Chart
        const revenueCtx = document.getElementById('revenueChart');
        if (revenueCtx) {
            // Destroy existing chart if it exists
            if (revenueChart) {
                revenueChart.destroy();
            }
            
            revenueChart = new Chart(revenueCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
                    datasets: [{
                        label: 'Revenus',
                        data: [45000, 52000, 48000, 61000, 58000, 72000],
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        }

        // Project Chart
        const projectCtx = document.getElementById('projectChart');
        if (projectCtx) {
            // Destroy existing chart if it exists
            if (projectChart) {
                projectChart.destroy();
            }
            
            projectChart = new Chart(projectCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Commercial', 'Industriel', 'Résidentiel'],
                    datasets: [{
                        data: [35, 45, 20],
                        backgroundColor: [
                            '#3B82F6',
                            '#10B981',
                            '#F59E0B'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }

    // Email functionality
    function setupEmailHandlers() {
        // Email item clicks
        const emailItems = document.querySelectorAll('.email-item');
        emailItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // Skip if clicking checkbox
                if (e.target.type === 'checkbox') return;
                
                // Mark as read
                const unreadBadge = this.querySelector('.bg-red-100');
                if (unreadBadge) {
                    unreadBadge.remove();
                    this.classList.add('opacity-75');
                    unreadEmailCount--;
                    updateEmailBadge();
                }
                
                // Show email details (placeholder)
                console.log('Opening email details...');
            });
        });

        // Auto-process buttons
        const autoProcessBtns = document.querySelectorAll('[class*="Traiter automatiquement"], [class*="Analyser avec IA"]');
        autoProcessBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const emailItem = this.closest('.email-item');
                
                // Simulate processing
                this.textContent = 'Traitement...';
                this.disabled = true;
                
                setTimeout(() => {
                    this.textContent = '✓ Traité';
                    this.classList.add('text-green-600');
                    
                    // Add processed badge
                    const badges = emailItem.querySelector('.flex.items-center.space-x-2');
                    const processedBadge = document.createElement('span');
                    processedBadge.className = 'bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded';
                    processedBadge.textContent = 'Auto-traité';
                    badges.appendChild(processedBadge);
                }, 2000);
            });
        });

        // Sync button
        const syncBtn = document.querySelector('[data-lucide="refresh-cw"]')?.closest('button');
        if (syncBtn) {
            syncBtn.addEventListener('click', function() {
                const icon = this.querySelector('[data-lucide]');
                icon.classList.add('animate-spin');
                
                // Simulate sync
                setTimeout(() => {
                    icon.classList.remove('animate-spin');
                    showNotification('Emails synchronisés avec succès');
                }, 2000);
            });
        }
    }

    // Notification system
    function showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg text-white z-50 ${
            type === 'success' ? 'bg-green-600' : 'bg-red-600'
        }`;
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <i data-lucide="${type === 'success' ? 'check-circle' : 'alert-circle'}" class="w-5 h-5"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        lucide.createIcons();
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Simulate real-time updates
    function simulateRealTimeUpdates() {
        // Randomly update email count
        setInterval(() => {
            if (Math.random() > 0.8 && activeTab !== 'emails') {
                unreadEmailCount++;
                updateEmailBadge();
                showNotification('Nouvel email reçu', 'info');
            }
        }, 30000); // Every 30 seconds
    }

    // Load directives data
    function loadDirectives() {
        const tbody = document.getElementById('directivesTableBody');
        if (!tbody || !window.REAL_PROJECT_DATA) return;
        
        const directives = currentProject === 'S-1086' ? 
            window.REAL_PROJECT_DATA.kahnawakeDirectives : 
            window.REAL_PROJECT_DATA.alexisNihonDirectives || [];
        
        tbody.innerHTML = '';
        
        directives.slice(0, 10).forEach(dir => {
            const statusClass = getStatusClass(dir.status);
            const priceFormatted = dir.price !== 0 ? 
                new Intl.NumberFormat('fr-CA', { style: 'currency', currency: 'CAD' }).format(dir.price) : 
                '-';
            
            const row = `
                <tr class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${dir.id}</td>
                    <td class="px-6 py-4 text-sm text-gray-700">${dir.desc}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${dir.dateRecue || '-'}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-right font-mono ${dir.price < 0 ? 'text-red-600' : 'text-gray-900'}">${priceFormatted}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="${statusClass}">${dir.status}</span>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }
    
    function getStatusClass(status) {
        const classes = {
            'À préparer': 'px-2 py-1 text-xs font-medium rounded-full bg-yellow-100 text-yellow-800',
            'À clarifier': 'px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800',
            'Soumis': 'px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800',
            'Sans Frais': 'px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800',
            'Approuvé': 'px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800'
        };
        return classes[status] || '';
    }
    
    // Load notes data
    function loadNotes() {
        const notesList = document.getElementById('notesList');
        if (!notesList || !window.REAL_PROJECT_DATA) return;
        
        // Notes are already in the HTML, but we could dynamically update them here
        const notesCount = document.getElementById('notesBadge');
        if (notesCount) {
            notesCount.textContent = window.REAL_PROJECT_DATA.recentNotes.length;
        }
    }
    
    // Load photos data
    function loadPhotos() {
        // Photos functionality would connect to backend
        console.log('Loading photos for project:', currentProject);
    }
    
    // Update project data when changed
    function updateProjectData() {
        if (!window.REAL_PROJECT_DATA) return;
        
        const project = window.REAL_PROJECT_DATA.projects.find(p => p.id === currentProject);
        if (!project) return;
        
        // Update stats if on dashboard
        if (activeTab === 'dashboard') {
            updateDashboardStats();
        }
        
        // Update directives if on directives tab
        if (activeTab === 'directives') {
            loadDirectives();
            updateDirectivesStats(project);
        }
    }
    
    // Update dashboard statistics with real data
    function updateDashboardStats() {
        if (!window.REAL_PROJECT_DATA) return;
        
        // Update counters
        document.getElementById('activeProjectsCount').textContent = window.REAL_PROJECT_DATA.stats.activeProjects;
        document.getElementById('documentsCount').textContent = window.REAL_PROJECT_DATA.stats.documentsProcessed.toLocaleString();
        document.getElementById('monthlyRevenue').textContent = new Intl.NumberFormat('fr-CA', { 
            style: 'currency', 
            currency: 'CAD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(window.REAL_PROJECT_DATA.stats.monthlyRevenue);
        
        // Update badges
        document.getElementById('emailBadge').textContent = window.REAL_PROJECT_DATA.recentEmails.filter(e => e.unread).length;
        document.getElementById('notesBadge').textContent = window.REAL_PROJECT_DATA.recentNotes.filter(n => n.status === 'pending').length;
        document.getElementById('directivesBadge').textContent = currentProject === 'S-1086' ? 32 : 28;
    }
    
    // Update directives statistics
    function updateDirectivesStats(project) {
        // Update the summary cards in directives view
        const extrasEl = document.querySelector('#directives .text-green-600');
        const creditsEl = document.querySelector('#directives .text-red-600');
        const netEl = document.querySelector('#directives .text-blue-600');
        
        if (extrasEl && project.totalExtras) {
            extrasEl.textContent = new Intl.NumberFormat('fr-CA', { 
                style: 'currency', 
                currency: 'CAD' 
            }).format(project.totalExtras);
        }
        
        if (creditsEl && project.totalCredits) {
            creditsEl.textContent = `(${new Intl.NumberFormat('fr-CA', { 
                style: 'currency', 
                currency: 'CAD' 
            }).format(Math.abs(project.totalCredits))})`;
        }
        
        if (netEl && project.netImpact) {
            netEl.textContent = `(${new Intl.NumberFormat('fr-CA', { 
                style: 'currency', 
                currency: 'CAD' 
            }).format(Math.abs(project.netImpact))})`;
        }
    }
    
    // Initialize everything
    initCharts();
    setupEmailHandlers();
    updateEmailBadge();
    simulateRealTimeUpdates();
    
    // Load real data after a short delay to ensure dashboard_real_data.js is loaded
    setTimeout(() => {
        updateDashboardStats();
    }, 100);

    // Add some interactivity to other elements
    document.querySelectorAll('button').forEach(btn => {
        if (!btn.hasAttribute('data-tab') && !btn.classList.contains('sidebar-item')) {
            btn.addEventListener('click', function() {
                if (this.textContent.includes('Nouveau projet')) {
                    showNotification('Formulaire de création en développement');
                } else if (this.textContent.includes('Composer')) {
                    showNotification('Interface de composition en développement');
                }
            });
        }
    });

    // Toggle switches
    document.querySelectorAll('input[type="checkbox"].toggle').forEach(toggle => {
        toggle.addEventListener('change', function() {
            const label = this.closest('.flex').querySelector('span').textContent;
            showNotification(`${label} ${this.checked ? 'activé' : 'désactivé'}`);
        });
    });
});

// Add custom styles for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .animate-spin {
        animation: spin 1s linear infinite;
    }
    .opacity-0 {
        opacity: 0;
    }
    transition {
        transition-property: all;
        transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        transition-duration: 300ms;
    }
`;
document.head.appendChild(style);