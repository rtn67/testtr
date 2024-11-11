class StrategyManager {
    constructor() {
        this.config = {
            maxActiveDeals: 1,
            strategy: 'long',
            baseOrderSize: 0,
            orderType: 'market'
        };
        
        this.initializeUI();
        this.initializeEventListeners();
    }

    initializeUI() {
        // Set initial values
        document.getElementById('maxActiveDeals').value = this.config.maxActiveDeals;
        document.getElementById('baseOrderSize').value = this.config.baseOrderSize;
        
        // Set initial button states
        this.selectStrategy(this.config.strategy);
        this.selectOrderType(this.config.orderType);
    }

    initializeEventListeners() {
        // Max active deals input
        document.getElementById('maxActiveDeals').addEventListener('change', (e) => {
            this.config.maxActiveDeals = parseInt(e.target.value);
            this.validateSettings();
        });

        // Base order size input
        document.getElementById('baseOrderSize').addEventListener('change', (e) => {
            this.config.baseOrderSize = parseFloat(e.target.value);
            this.validateSettings();
        });

        // Strategy buttons
        document.querySelectorAll('.strategy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const strategy = e.target.dataset.strategy;
                this.selectStrategy(strategy);
            });
        });

        // Order type buttons
        document.querySelectorAll('.order-type-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const orderType = e.target.dataset.orderType;
                this.selectOrderType(orderType);
            });
        });
    }

    selectStrategy(strategy) {
        this.config.strategy = strategy;
        
        // Update UI
        document.querySelectorAll('.strategy-btn').forEach(btn => {
            const isSelected = btn.dataset.strategy === strategy;
            btn.classList.toggle('bg-indigo-500', isSelected);
            btn.classList.toggle('text-white', isSelected);
            btn.classList.toggle('bg-white', !isSelected);
            btn.classList.toggle('text-gray-700', !isSelected);
        });
        
        this.onStrategyChange();
    }

    selectOrderType(orderType) {
        this.config.orderType = orderType;
        
        // Update UI
        document.querySelectorAll('.order-type-btn').forEach(btn => {
            const isSelected = btn.dataset.orderType === orderType;
            btn.classList.toggle('bg-indigo-500', isSelected);
            btn.classList.toggle('text-white', isSelected);
            btn.classList.toggle('bg-white', !isSelected);
            btn.classList.toggle('text-gray-700', !isSelected);
        });
        
        this.onOrderTypeChange();
    }

    validateSettings() {
        const isValid = 
            this.config.maxActiveDeals > 0 && 
            this.config.baseOrderSize > 0;
            
        // Update UI based on validation
        const inputs = ['maxActiveDeals', 'baseOrderSize'];
        inputs.forEach(id => {
            const input = document.getElementById(id);
            const value = parseFloat(input.value);
            const isInputValid = value > 0;
            
            input.classList.toggle('border-red-500', !isInputValid);
            
            // Show/hide error message
            const errorId = `${id}Error`;
            let errorEl = document.getElementById(errorId);
            
            if (!isInputValid) {
                if (!errorEl) {
                    errorEl = document.createElement('p');
                    errorEl.id = errorId;
                    errorEl.className = 'mt-1 text-sm text-red-600';
                    errorEl.textContent = 'Value must be greater than 0';
                    input.parentNode.appendChild(errorEl);
                }
            } else if (errorEl) {
                errorEl.remove();
            }
        });
        
        return isValid;
    }

    onStrategyChange() {
        // Handle strategy change
        const event = new CustomEvent('strategyChange', {
            detail: { strategy: this.config.strategy }
        });
        document.dispatchEvent(event);
    }

    onOrderTypeChange() {
        // Handle order type change
        const event = new CustomEvent('orderTypeChange', {
            detail: { orderType: this.config.orderType }
        });
        document.dispatchEvent(event);
    }

    getConfig() {
        return { ...this.config };
    }
}

// Initialize strategy manager
let strategyManager;
document.addEventListener('DOMContentLoaded', () => {
    strategyManager = new StrategyManager();
});
