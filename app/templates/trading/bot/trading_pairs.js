class TradingPairsManager {
    constructor() {
        this.selectedPairs = new Set();
        this.botType = 'single';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Quote currency buttons
        document.querySelectorAll('.quote-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuoteButtonClick(e));
        });

        // Single pair selector
        const pairSelect = document.getElementById('pairSelect');
        if (pairSelect) {
            pairSelect.addEventListener('change', (e) => this.handlePairSelection(e));
        }
    }

    async loadPairs(quoteCurrency) {
        try {
            const exchange = document.getElementById('exchange').value;
            const response = await fetch(`/api/trading/pairs?exchange=${exchange}`);
            const data = await response.json();

            if (data.success) {
                const filteredPairs = data.pairs.filter(pair => pair.quote === quoteCurrency);
                return filteredPairs;
            }
            return [];
        } catch (error) {
            console.error('Error loading trading pairs:', error);
            return [];
        }
    }

    async handleQuoteButtonClick(event) {
        const quoteCurrency = event.target.dataset.quote;
        const pairs = await this.loadPairs(quoteCurrency);
        
        if (this.botType === 'single') {
            // Update single pair selector
            this.updatePairSelector(pairs);
        } else {
            // Add all pairs to multi-pair selection
            pairs.forEach(pair => this.addPair(pair.symbol));
        }
    }

    updatePairSelector(pairs) {
        const selector = document.getElementById('pairSelect');
        if (!selector) return;

        selector.innerHTML = `
            <option value="">Select trading pair</option>
            ${pairs.map(pair => `
                <option value="${pair.symbol}">${pair.symbol}</option>
            `).join('')}
        `;
    }

    addPair(pairSymbol) {
        if (this.selectedPairs.has(pairSymbol)) return;

        this.selectedPairs.add(pairSymbol);
        this.updateSelectedPairsDisplay();
    }

    removePair(pairSymbol) {
        this.selectedPairs.delete(pairSymbol);
        this.updateSelectedPairsDisplay();
    }

    updateSelectedPairsDisplay() {
        const container = document.getElementById('selectedPairs');
        if (!container) return;

        container.innerHTML = Array.from(this.selectedPairs).map(pair => `
            <div class="flex items-center justify-between bg-gray-50 px-3 py-2 rounded-md">
                <span class="text-sm font-medium text-gray-700">${pair}</span>
                <button type="button" 
                        onclick="tradingPairsManager.removePair('${pair}')"
                        class="text-red-600 hover:text-red-800 focus:outline-none">
                    <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
        `).join('');
    }

    setBotType(type) {
        this.botType = type;
        this.selectedPairs.clear();
        this.updateSelectedPairsDisplay();
        
        // Show/hide appropriate elements
        document.getElementById('singlePairSelector').style.display = 
            type === 'single' ? 'block' : 'none';
    }

    getSelectedPairs() {
        return Array.from(this.selectedPairs);
    }
}

// Initialize trading pairs manager
let tradingPairsManager;
document.addEventListener('DOMContentLoaded', () => {
    tradingPairsManager = new TradingPairsManager();
});
