document.addEventListener('DOMContentLoaded', async function() {
    console.log('Trading.js loaded');
    
    // Get all DOM elements
    const statusPanel = document.getElementById('statusPanel');
    const statusIndicator = document.getElementById('statusIndicator');
    const exchangeStatus = document.getElementById('exchangeStatus');
    const statusDetails = document.getElementById('statusDetails');
    const retryConnection = document.getElementById('retryConnection');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');
    const tradingPairsGrid = document.getElementById('tradingPairsGrid');
    const exchangeSelect = document.getElementById('exchangeSelect');
    const createRobotBtn = document.getElementById('createRobotBtn');
    const createRobotModal = document.getElementById('createRobotModal');
    const cancelCreateRobot = document.getElementById('cancelCreateRobot');
    const createRobotForm = document.getElementById('createRobotForm');
    const selectedPairInput = document.getElementById('selectedPair');
    const entryTypeSelect = document.querySelector('select[name="entry_type"]');
    const signalSettings = document.getElementById('signalSettings');
    
    let selectedPair = null;

    console.log('DOM Elements initialized');

    async function checkExchangeConnection() {
        try {
            console.log("Checking exchange connection...");
            updateStatus('checking', 'Checking connection...');
            
            const response = await fetch(`/api/trading/check-connection?exchange=${exchangeSelect.value}`);
            const data = await response.json();
            
            console.log("Connection response:", data);
            
            if (response.ok && data.status === 'success') {
                updateStatus('connected', 'Connected', data.data);
                return true;
            } else {
                throw new Error(data.message || 'Connection failed');
            }
        } catch (error) {
            console.error('Connection error:', error);
            updateStatus('error', 'Connection failed');
            return false;
        }
    }

    function updateStatus(status, text, data = null) {
        console.log("Updating status:", status, text, data);
        if (exchangeStatus) exchangeStatus.textContent = text;
        
        if (status === 'connected' && data && statusDetails) {
            const btcPrice = document.getElementById('btcPrice');
            const btcVolume = document.getElementById('btcVolume');
            if (btcPrice) btcPrice.textContent = `$${parseFloat(data.btc_price).toLocaleString()}`;
            if (btcVolume) btcVolume.textContent = `${parseFloat(data.btc_volume).toLocaleString()} BTC`;
            statusDetails.classList.remove('hidden');
            if (retryConnection) retryConnection.classList.add('hidden');
        } else if (statusDetails) {
            statusDetails.classList.add('hidden');
            if (retryConnection) {
                retryConnection.classList.toggle('hidden', status !== 'error');
            }
        }

        if (statusIndicator) {
            statusIndicator.className = 'w-3 h-3 rounded-full mr-2 ' + 
                (status === 'connected' ? 'bg-green-500' : 
                 status === 'error' ? 'bg-red-500' : 
                 'bg-yellow-500');
        }
             
        if (statusPanel) {
            statusPanel.className = 'mb-6 p-4 rounded-md ' +
                (status === 'connected' ? 'bg-green-50' : 
                 status === 'error' ? 'bg-red-50' : 
                 'bg-yellow-50');
        }
    }

    async function fetchTradingPairs() {
        try {
            console.log("Fetching trading pairs...");
            if (loadingState) loadingState.classList.remove('hidden');
            if (errorState) errorState.classList.add('hidden');
            if (tradingPairsGrid) tradingPairsGrid.classList.add('hidden');

            const response = await fetch(`/api/trading/pairs?exchange=${exchangeSelect.value}`);
            const data = await response.json();
            
            console.log("Trading pairs response:", data);
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch trading pairs');
            }

            if (loadingState) loadingState.classList.add('hidden');
            if (tradingPairsGrid) {
                tradingPairsGrid.classList.remove('hidden');
                tradingPairsGrid.innerHTML = data.pairs.map(pair => `
                    <div class="bg-white shadow rounded-lg p-4 hover:shadow-lg cursor-pointer trading-pair-card" 
                         data-symbol="${pair.symbol}">
                        <div class="flex justify-between items-start">
                            <h3 class="text-lg font-medium text-gray-900">${pair.symbol}</h3>
                            <span class="px-2 py-1 text-xs font-semibold rounded ${
                                parseFloat(pair.change_24h) >= 0 ? 
                                'bg-green-100 text-green-800' : 
                                'bg-red-100 text-red-800'
                            }">
                                ${parseFloat(pair.change_24h).toFixed(2)}%
                            </span>
                        </div>
                        <div class="mt-2 text-sm text-gray-500">
                            <p>Price: $${parseFloat(pair.last_price).toFixed(2)}</p>
                            <p>24h Volume: ${parseFloat(pair.volume_24h).toFixed(2)}</p>
                            <p>24h High: $${parseFloat(pair.high_24h).toFixed(2)}</p>
                            <p>24h Low: $${parseFloat(pair.low_24h).toFixed(2)}</p>
                        </div>
                    </div>
                `).join('');
            }
            
            if (createRobotBtn) createRobotBtn.disabled = true;
            
        } catch (error) {
            console.error('Error:', error);
            if (loadingState) loadingState.classList.add('hidden');
            if (errorState) errorState.classList.remove('hidden');
            if (errorMessage) errorMessage.textContent = error.message;
            if (tradingPairsGrid) tradingPairsGrid.classList.add('hidden');
            if (createRobotBtn) createRobotBtn.disabled = true;
        }
    }

    // Event Listeners
    if (exchangeSelect) {
        exchangeSelect.addEventListener('change', async () => {
            await checkExchangeConnection();
            await fetchTradingPairs();
        });
    }

    if (retryConnection) {
        retryConnection.addEventListener('click', async () => {
            await checkExchangeConnection();
        });
    }

    // Trading pair selection
    document.addEventListener('click', function(e) {
        if (e.target.closest('.trading-pair-card')) {
            const card = e.target.closest('.trading-pair-card');
            
            // Remove previous selection
            document.querySelectorAll('.trading-pair-card').forEach(c => 
                c.classList.remove('ring-2', 'ring-indigo-500'));
            
            // Add selection to clicked card
            card.classList.add('ring-2', 'ring-indigo-500');
            
            // Store selected pair
            selectedPair = card.dataset.symbol;
            
            // Enable create robot button
            if (createRobotBtn) {
                createRobotBtn.disabled = false;
            }
        }
    });

    // Create Robot Modal handlers
    if (createRobotBtn) {
        createRobotBtn.addEventListener('click', function() {
            if (!selectedPair) {
                alert('Please select a trading pair first');
                return;
            }
            if (selectedPairInput) selectedPairInput.value = selectedPair;
            if (createRobotModal) createRobotModal.classList.remove('hidden');
        });
    }

    if (cancelCreateRobot) {
        cancelCreateRobot.addEventListener('click', function() {
            if (createRobotModal) createRobotModal.classList.add('hidden');
        });
    }

    if (entryTypeSelect) {
        entryTypeSelect.addEventListener('change', function() {
            if (signalSettings) {
                signalSettings.style.display = this.value === 'signal' ? 'block' : 'none';
            }
        });
    }

    if (createRobotForm) {
        createRobotForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            try {
                const formData = new FormData(this);
                
                // Build signal config
                const signalConfig = {
                    rsi: {
                        enabled: formData.get('rsi_enabled') === 'on',
                        period: parseInt(formData.get('rsi_period')),
                        oversold: parseInt(formData.get('rsi_oversold')),
                        overbought: parseInt(formData.get('rsi_overbought'))
                    },
                    macd: {
                        enabled: formData.get('macd_enabled') === 'on',
                        fast_period: parseInt(formData.get('macd_fast_period')),
                        slow_period: parseInt(formData.get('macd_slow_period')),
                        signal_period: parseInt(formData.get('macd_signal_period'))
                    },
                    moving_averages: {
                        enabled: formData.get('ma_enabled') === 'on',
                        fast_ma: parseInt(formData.get('ma_fast')),
                        medium_ma: parseInt(formData.get('ma_medium')),
                        slow_ma: parseInt(formData.get('ma_slow'))
                    }
                };
                
                // Build DCA config
                const dcaConfig = {
                    enabled: formData.get('dca_enabled') === 'on',
                    correction_levels: formData.get('correction_levels').split(',').map(Number),
                    order_sizes: formData.get('order_sizes').split(',').map(Number),
                    max_orders: parseInt(formData.get('max_orders')),
                    min_order_interval: parseInt(formData.get('min_order_interval'))
                };
                
                // Create request body
                const requestData = {
                    name: formData.get('name'),
                    trading_pair: formData.get('trading_pair'),
                    initial_investment: parseFloat(formData.get('initial_investment')),
                    entry_type: formData.get('entry_type'),
                    signal_config: signalConfig,
                    dca_config: dcaConfig,
                    take_profit: parseFloat(formData.get('take_profit')),
                    stop_loss: parseFloat(formData.get('stop_loss')),
                    trailing_stop: parseFloat(formData.get('trailing_stop'))
                };
                
                console.log("Creating robot with data:", requestData);
                
                // Send request to create robot
                const response = await fetch('/api/trading/create_robot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    alert('Robot created successfully!');
                    window.location.href = '/dashboard';
                } else {
                    throw new Error(result.message || 'Failed to create robot');
                }
                
            } catch (error) {
                console.error('Error creating robot:', error);
                alert('Error creating robot: ' + error.message);
            }
        });
    }

    // Initialize
    await checkExchangeConnection();
    await fetchTradingPairs();

    console.log('Trading.js initialization complete');
});