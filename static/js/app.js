// Main JavaScript file for the Group-Buying Application

// Global variables for real-time updates
let autoRefreshInterval = null;
let lastDealUpdate = null;
let isAutoRefreshEnabled = true;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Group-Buying App loaded successfully!');
    
    // Initialize form handling
    initializeDealForm();
    
    // Initialize real-time updates
    initializeRealTimeUpdates();
    
    console.log('Flask server connection: Ready');
    console.log('Static files loading: Success');
    console.log('Real-time updates: Initialized');
});

// Real-time Updates System
function initializeRealTimeUpdates() {
    // Create connection status indicator
    createConnectionStatusIndicator();
    
    // Create notification container
    createNotificationContainer();
    
    // Start auto-refresh for deals
    startAutoRefresh();
    
    // Add visibility change handler (pause when tab is hidden)
    document.addEventListener('visibilitychange', handleVisibilityChange);
}

function createConnectionStatusIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'connectionStatus';
    indicator.innerHTML = `
        <div class="connection-indicator online">
            <span class="status-dot"></span>
            <span class="status-text">Connected</span>
        </div>
    `;
    document.body.appendChild(indicator);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notificationContainer';
    container.className = 'notification-container';
    document.body.appendChild(container);
}

function startAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        if (isAutoRefreshEnabled && !document.hidden) {
            refreshDealsWithNotifications();
        }
    }, 30000); // 30 seconds
    
    console.log('Auto-refresh started (30s intervals)');
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        console.log('Auto-refresh stopped');
    }
}

function handleVisibilityChange() {
    if (document.hidden) {
        console.log('Tab hidden - pausing auto-refresh');
    } else {
        console.log('Tab visible - resuming auto-refresh');
        // Refresh immediately when tab becomes visible
        refreshDealsWithNotifications();
    }
}

async function refreshDealsWithNotifications() {
    try {
        updateConnectionStatus('checking');
        
        // Get current deals
        const response = await fetch('/api/deals?status=active');
        const result = await response.json();
        
        if (response.ok && result.success) {
            updateConnectionStatus('online');
            updateLastRefreshTime();
            
            // Check for deal updates and show notifications
            checkForDealUpdates(result.deals);
            
            // Update the display if deals section is visible
            const dealsSection = document.getElementById('dealsSection');
            if (dealsSection && dealsSection.style.display !== 'none') {
                displayDeals(result.deals);
            }
        } else {
            updateConnectionStatus('error');
        }
    } catch (error) {
        console.error('Auto-refresh error:', error);
        updateConnectionStatus('offline');
    }
}

function updateLastRefreshTime() {
    const timeElement = document.getElementById('lastUpdateTime');
    if (timeElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        timeElement.textContent = timeString;
    }
}

function checkForDealUpdates(currentDeals) {
    if (!lastDealUpdate) {
        lastDealUpdate = currentDeals;
        return;
    }
    
    currentDeals.forEach(currentDeal => {
        const previousDeal = lastDealUpdate.find(d => d.dealId === currentDeal.dealId);
        
        if (previousDeal) {
            // Check for progress changes
            if (currentDeal.current_quantity > previousDeal.current_quantity) {
                const quantityIncrease = currentDeal.current_quantity - previousDeal.current_quantity;
                showProgressNotification(currentDeal, quantityIncrease);
            }
            
            // Check for deal completion
            if (currentDeal.progress_percentage >= 100 && previousDeal.progress_percentage < 100) {
                showDealCompletionNotification(currentDeal);
            }
            
            // Check for expiring soon status
            if (currentDeal.is_expiring_soon && !previousDeal.is_expiring_soon) {
                showExpiringNotification(currentDeal);
            }
        }
    });
    
    lastDealUpdate = currentDeals;
}

function updateConnectionStatus(status) {
    const indicator = document.getElementById('connectionStatus');
    if (indicator) {
        const statusElement = indicator.querySelector('.connection-indicator');
        const textElement = indicator.querySelector('.status-text');
        
        statusElement.className = `connection-indicator ${status}`;
        
        switch(status) {
            case 'online':
                textElement.textContent = 'Connected';
                break;
            case 'offline':
                textElement.textContent = 'Offline';
                break;
            case 'checking':
                textElement.textContent = 'Checking...';
                break;
            case 'error':
                textElement.textContent = 'Error';
                break;
        }
    }
}

// Show/Hide Create Deal Form
function showCreateDealForm() {
    const form = document.getElementById('createDealForm');
    form.style.display = 'block';
    form.scrollIntoView({ behavior: 'smooth' });
    hideMessage();
}

function hideCreateDealForm() {
    const form = document.getElementById('createDealForm');
    form.style.display = 'none';
    clearForm();
    hideMessage();
}

function showDeals() {
    const dealsSection = document.getElementById('dealsSection');
    dealsSection.style.display = 'block';
    dealsSection.scrollIntoView({ behavior: 'smooth' });
    hideMessage();
    loadDeals();
}

function hideDeals() {
    const dealsSection = document.getElementById('dealsSection');
    dealsSection.style.display = 'none';
}

// Notification System
function showProgressNotification(deal, quantityIncrease) {
    const message = `🎉 "${deal.item}" deal updated! +${quantityIncrease} ${deal.unit} joined (${deal.progress_percentage}% complete)`;
    showToastNotification(message, 'success', 4000);
}

function showDealCompletionNotification(deal) {
    const message = `🎊 Deal Complete! "${deal.item}" reached ${deal.target_quantity} ${deal.unit}!`;
    showToastNotification(message, 'celebration', 6000);
}

function showExpiringNotification(deal) {
    const message = `⏰ "${deal.item}" deal expires in ${deal.hours_until_expiry}h!`;
    showToastNotification(message, 'warning', 5000);
}

function showToastNotification(message, type = 'info', duration = 4000) {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `toast-notification toast-${type}`;
    notification.innerHTML = `
        <div class="toast-content">
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.add('hide');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, duration);
}

// Enhanced deal loading with smooth animations
async function loadDeals() {
    const container = document.getElementById('dealsContainer');
    const loading = document.getElementById('dealsLoading');
    const noDealsMessage = document.getElementById('noDealsMessage');
    const locationFilter = document.getElementById('locationFilter').value;
    
    // Show loading
    loading.style.display = 'block';
    container.innerHTML = '';
    noDealsMessage.style.display = 'none';
    
    try {
        updateConnectionStatus('checking');
        
        let url = '/api/deals?status=active';
        if (locationFilter) {
            url += `&location=${encodeURIComponent(locationFilter)}`;
        }
        
        const response = await fetch(url);
        const result = await response.json();
        
        loading.style.display = 'none';
        updateConnectionStatus('online');
        
        if (response.ok && result.success) {
            if (result.deals.length === 0) {
                noDealsMessage.style.display = 'block';
            } else {
                displayDealsWithAnimation(result.deals);
                // Store for comparison in auto-refresh
                lastDealUpdate = result.deals;
            }
        } else {
            updateConnectionStatus('error');
            showMessage(`❌ Error loading deals: ${result.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error loading deals:', error);
        loading.style.display = 'none';
        updateConnectionStatus('offline');
        showMessage('❌ Network error while loading deals. Please try again.', 'error');
    }
}

function displayDealsWithAnimation(deals) {
    const container = document.getElementById('dealsContainer');
    
    // Create all deal cards
    const dealCards = deals.map((deal, index) => {
        const card = document.createElement('div');
        card.className = `deal-card ${deal.is_expiring_soon ? 'expiring-soon' : ''}`;
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.innerHTML = createDealCardHTML(deal);
        return { element: card, delay: index * 100 };
    });
    
    // Clear and add all cards
    container.innerHTML = '';
    dealCards.forEach(({ element }) => {
        container.appendChild(element);
    });
    
    // Animate cards in with staggered timing
    dealCards.forEach(({ element, delay }) => {
        setTimeout(() => {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    });
}

function createDealCardHTML(deal) {
    return `
        <div class="deal-header">
            <h4 class="deal-title">${escapeHtml(deal.item)}</h4>
            <div class="deal-price">₹${deal.price}/${deal.unit}</div>
        </div>
        
        <div class="deal-supplier">📦 ${escapeHtml(deal.supplier_name)}</div>
        
        ${deal.description ? `<div class="deal-description">"${escapeHtml(deal.description)}"</div>` : ''}
        
        <div class="deal-progress">
            <div class="progress-bar">
                <div class="progress-fill animated-progress" style="width: ${deal.progress_percentage}%"></div>
            </div>
            <div class="progress-text">
                <span>${deal.current_quantity}/${deal.target_quantity} ${deal.unit}</span>
                <span>${deal.progress_percentage}% complete</span>
            </div>
        </div>
        
        <div class="deal-meta">
            <div class="deal-location">📍 ${escapeHtml(deal.location)}</div>
            <div class="deal-expiry">
                ${deal.hours_until_expiry ? 
                    (deal.is_expiring_soon ? 
                        `⚠️ ${deal.hours_until_expiry}h left` : 
                        `⏰ ${deal.hours_until_expiry}h left`
                    ) : '⏰ Expires soon'
                }
            </div>
        </div>
        
        ${deal.remaining_quantity > 0 ? 
            `<div style="margin-top: 1rem;">
                <button class="btn btn-primary" style="width: 100%;" onclick="openJoinModal('${deal.dealId}', '${escapeHtml(deal.item)}', 1)">
                    Join Deal (${deal.remaining_quantity} ${deal.unit} available)
                </button>
            </div>` : 
            `<div style="margin-top: 1rem;">
                <button class="btn btn-secondary" style="width: 100%; opacity: 0.6;" disabled>
                    Deal Complete ✅
                </button>
            </div>`
        }
    `;
}

function displayDeals(deals) {
    // Use the animated version for better UX
    displayDealsWithAnimation(deals);
}

function filterDeals() {
    loadDeals();
}

function refreshDeals() {
    loadDeals();
    showToastNotification('🔄 Deals refreshed manually', 'info', 2000);
}

// Auto-refresh toggle functionality
function toggleAutoRefresh() {
    const checkbox = document.getElementById('autoRefreshToggle');
    isAutoRefreshEnabled = checkbox.checked;
    
    if (isAutoRefreshEnabled) {
        startAutoRefresh();
        showToastNotification('✅ Auto-refresh enabled (30s)', 'success', 2000);
    } else {
        stopAutoRefresh();
        showToastNotification('⏸️ Auto-refresh paused', 'info', 2000);
    }
}

function joinDeal(dealId) {
    showMessage('Deal joining functionality will be implemented in the next step!', 'info');
    console.log('Join deal:', dealId);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Form handling
function initializeDealForm() {
    const form = document.getElementById('dealForm');
    if (form) {
        form.addEventListener('submit', handleDealSubmission);
    }
}

async function handleDealSubmission(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const dealData = {
        supplierName: formData.get('supplierName'),
        item: formData.get('item'),
        unit: formData.get('unit'),
        price: parseFloat(formData.get('price')),
        target_quantity: parseInt(formData.get('target_quantity')),
        location: formData.get('location'),
        description: formData.get('description')
    };
    
    // Remove empty description
    if (!dealData.description.trim()) {
        delete dealData.description;
    }
    
    try {
        showMessage('Creating deal...', 'info');
        
        const response = await fetch('/api/deals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dealData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            showMessage(
                `✅ Deal created successfully!<br>
                <strong>Deal ID:</strong> ${result.deal.dealId}<br>
                <strong>Item:</strong> ${result.deal.item}<br>
                <strong>Price:</strong> ₹${result.deal.price}/${result.deal.unit}<br>
                <strong>Target:</strong> ${result.deal.target_quantity} ${result.deal.unit}`,
                'success'
            );
            clearForm();
        } else {
            showMessage(`❌ Error: ${result.error || 'Failed to create deal'}`, 'error');
        }
    } catch (error) {
        console.error('Error creating deal:', error);
        showMessage('❌ Network error. Please check your connection and try again.', 'error');
    }
}

// Utility functions
function clearForm() {
    const form = document.getElementById('dealForm');
    if (form) {
        form.reset();
    }
}

function showMessage(message, type = 'info') {
    const messageArea = document.getElementById('messageArea');
    const messageContent = document.getElementById('messageContent');
    
    messageContent.innerHTML = message;
    messageArea.className = `message-area message-${type}`;
    messageArea.style.display = 'block';
    
    messageArea.scrollIntoView({ behavior: 'smooth' });
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }
}

function hideMessage() {
    const messageArea = document.getElementById('messageArea');
    messageArea.style.display = 'none';
}

// Modal functionality for joining deals
function setupModalEvents() {
    const modal = document.getElementById('joinDealModal');
    const modalClose = document.querySelector('.modal-close');
    const cancelBtn = document.getElementById('cancelJoinBtn');
    const joinForm = document.getElementById('joinDealForm');
    
    // Close modal events
    if (modalClose) {
        modalClose.addEventListener('click', closeJoinModal);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeJoinModal);
    }
    
    // Close modal when clicking outside
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeJoinModal();
            }
        });
    }
    
    // Handle join form submission
    if (joinForm) {
        joinForm.addEventListener('submit', handleJoinDeal);
    }
}

function openJoinModal(dealId, dealTitle, minQuantity = 1) {
    const modal = document.getElementById('joinDealModal');
    const dealTitleSpan = document.getElementById('modalDealTitle');
    const dealIdInput = document.getElementById('modalDealId');
    const quantityInput = document.getElementById('joinQuantity');
    const minQuantitySpan = document.getElementById('minQuantityValue');
    
    if (dealTitleSpan) dealTitleSpan.textContent = dealTitle;
    if (dealIdInput) dealIdInput.value = dealId;
    if (quantityInput) {
        quantityInput.min = minQuantity;
        quantityInput.value = minQuantity;
    }
    if (minQuantitySpan) minQuantitySpan.textContent = minQuantity;
    
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeJoinModal() {
    const modal = document.getElementById('joinDealModal');
    const form = document.getElementById('joinDealForm');
    
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
    
    if (form) {
        form.reset(); // Clear form data
    }
    
    // Clear any error messages
    clearFormErrors('joinDealForm');
}

async function handleJoinDeal(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = document.getElementById('submitJoinBtn');
    const formData = new FormData(form);
    
    // Clear previous errors
    clearFormErrors('joinDealForm');
    
    // Show loading state
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Joining...';
    }
    
    try {
        const response = await fetch(`/api/deals/${formData.get('deal_id')}/join`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                vendorId: formData.get('vendor_id'),
                quantity: parseInt(formData.get('quantity'))
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Success! Close modal and refresh deals
            closeJoinModal();
            
            // Show success notification
            const dealTitle = formData.get('deal_id');
            const quantity = formData.get('quantity');
            showToastNotification(
                `🎉 Successfully joined deal! Order ID: ${result.order.orderId}`, 
                'celebration', 
                5000
            );
            
            // Refresh deals to show updated progress
            setTimeout(() => {
                loadDeals();
            }, 500);
        } else {
            // Handle validation errors
            if (result.errors) {
                displayFormErrors('joinDealForm', result.errors);
            } else {
                showMessage(result.error || 'Failed to join deal', 'error');
            }
        }
    } catch (error) {
        console.error('Error joining deal:', error);
        showMessage('Network error. Please try again.', 'error');
    } finally {
        // Reset button state
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Join Deal';
        }
    }
}

// Utility functions for form error handling
function clearFormErrors(formId) {
    const form = document.getElementById(formId);
    if (form) {
        // Remove any existing error messages
        const errorElements = form.querySelectorAll('.error-message');
        errorElements.forEach(element => element.remove());
        
        // Remove error styling from inputs
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.classList.remove('error');
        });
    }
}

function displayFormErrors(formId, errors) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    // Clear existing errors first
    clearFormErrors(formId);
    
    // Display new errors
    for (const [fieldName, errorMessage] of Object.entries(errors)) {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
            // Add error styling to field
            field.classList.add('error');
            
            // Create and insert error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.style.color = '#e74c3c';
            errorDiv.style.fontSize = '0.8rem';
            errorDiv.style.marginTop = '0.25rem';
            errorDiv.textContent = errorMessage;
            
            // Insert after the field
            field.parentNode.insertBefore(errorDiv, field.nextSibling);
        }
    }
}

// Initialize modal events when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupModalEvents();
});
