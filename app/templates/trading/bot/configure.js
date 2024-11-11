document.addEventListener('DOMContentLoaded', function() {
    // Initialize bot configuration
    initializeBotConfig();
});

function initializeBotConfig() {
    // Set default values
    const defaultConfig = {
        botType: 'single',
        strategy: 'long',
        orderType: 'market',
        tpType: 'price',
        targetProfit: 2,
        trailingDeviation: 0.3,
        maxDeals: 1
    };

    // Initialize UI elements
    initializeUI(defaultConfig);

    // Add event listeners
    addEventListeners();
}

function initializeUI(config) {
    // Set default bot type
    selectBotType(document.querySelector(`[data-type="${config.botType}"]`), config.botType);

    // Initialize other UI elements as needed
    document.getElementById('targetProfit').value = config.targetProfit;
    document.getElementById('maxDeals').value = config.maxDeals;
}

function addEventListeners() {
    // Add event listeners for form inputs
    document.getElementById('botName').addEventListener('input', validateBotName);
    document.getElementById('exchange').addEventListener('change', handleExchangeChange);
    
    // Add event listeners for buttons
    document.querySelectorAll('.bot-type-btn').forEach(btn => {
        btn.addEventListener('click', (e) => selectBotType(e.target, e.target.dataset.type));
    });
}

function selectBotType(button, type) {
    // Remove active class from all buttons
    document.querySelectorAll('.bot-type-btn').forEach(btn => {
        btn.classList.remove('bg-indigo-500', 'text-white');
        btn.classList.add('bg-white', 'text-gray-700');
    });

    // Add active class to selected button
    button.classList.remove('bg-white', 'text-gray-700');
    button.classList.add('bg-indigo-500', 'text-white');

    // Update UI based on bot type
    updateTradingPairsUI(type);
}

function updateTradingPairsUI(type) {
    const pairsContainer = document.getElementById('tradingPairs');
    if (!pairsContainer) return;

    if (type === 'single') {
        // Show single pair selector
        pairsContainer.innerHTML = `
            <select id="singlePair" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                <option value="">Select trading pair</option>
            </select>
        `;
        loadTradingPairs();
    } else {
        // Show multi-pair interface
        pairsContainer.innerHTML = `
            <div id="selectedPairs" class="mb-2"></div>
            <div class="flex space-x-2">
                <button onclick="loadPairs('USDT')" class="px-3 py-1 rounded border">USDT_ALL</button>
                <button onclick="loadPairs('BTC')" class="px-3 py-1 rounded border">BTC_ALL</button>
                <button onclick="loadPairs('ETH')" class="px-3 py-1 rounded border">ETH_ALL</button>
                <button onclick="loadPairs('USDC')" class="px-3 py-1 rounded border">USDC_ALL</button>
            </div>
        `;
    }
}

async function loadTradingPairs() {
    try {
        const exchange = document.getElementById('exchange').value;
        const response = await fetch(`/api/trading/pairs?exchange=${exchange}`);
        const data = await response.json();
        
        if (data.success) {
            updatePairSelector(data.pairs);
        }
    } catch (error) {
        console.error('Error loading trading pairs:', error);
    }
}

function validateBotName(event) {
    const name = event.target.value;
    const isValid = name.length >= 3 && name.length <= 50;
    event.target.classList.toggle('border-red-500', !isValid);
}

function handleExchangeChange() {
    loadTradingPairs();
}
