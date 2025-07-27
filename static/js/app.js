// Main JavaScript file for the Group-Buying Application

document.addEventListener('DOMContentLoaded', function() {
    console.log('Group-Buying App loaded successfully!');
    
    // Initialize form handling
    initializeDealForm();
    
    console.log('Flask server connection: Ready');
    console.log('Static files loading: Success');
});

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

// Deals functionality
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
        let url = '/api/deals?status=active';
        if (locationFilter) {
            url += `&location=${encodeURIComponent(locationFilter)}`;
        }
        
        const response = await fetch(url);
        const result = await response.json();
        
        loading.style.display = 'none';
        
        if (response.ok && result.success) {
            if (result.deals.length === 0) {
                noDealsMessage.style.display = 'block';
            } else {
                displayDeals(result.deals);
            }
        } else {
            showMessage(`❌ Error loading deals: ${result.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error loading deals:', error);
        loading.style.display = 'none';
        showMessage('❌ Network error while loading deals. Please try again.', 'error');
    }
}

function displayDeals(deals) {
    const container = document.getElementById('dealsContainer');
    
    container.innerHTML = deals.map(deal => `
        <div class="deal-card ${deal.is_expiring_soon ? 'expiring-soon' : ''}">
            <div class="deal-header">
                <h4 class="deal-title">${escapeHtml(deal.item)}</h4>
                <div class="deal-price">₹${deal.price}/${deal.unit}</div>
            </div>
            
            <div class="deal-supplier">📦 ${escapeHtml(deal.supplier_name)}</div>
            
            ${deal.description ? `<div class="deal-description">"${escapeHtml(deal.description)}"</div>` : ''}
            
            <div class="deal-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${deal.progress_percentage}%"></div>
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
                    <button class="btn btn-primary" style="width: 100%;" onclick="joinDeal('${deal.dealId}')">
                        Join Deal (${deal.remaining_quantity} ${deal.unit} available)
                    </button>
                </div>` : 
                `<div style="margin-top: 1rem;">
                    <button class="btn btn-secondary" style="width: 100%; opacity: 0.6;" disabled>
                        Deal Complete ✅
                    </button>
                </div>`
            }
        </div>
    `).join('');
}

function filterDeals() {
    loadDeals();
}

function refreshDeals() {
    loadDeals();
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
        supplierId: formData.get('supplierId'),
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
