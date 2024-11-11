class DealConditionsManager {
    constructor() {
        this.conditions = new Map();
        this.nextId = 1;
        this.maxConditions = 5;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            // Add initial condition
            this.conditions.set(1, { type: '', params: {} });
            this.setupIndicatorListeners();
        });
    }

    setupIndicatorListeners() {
        // Listen for MA comparison type changes
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('ma-compare')) {
                const conditionGroup = e.target.closest('.condition-group');
                const secondPeriod = conditionGroup.querySelector('.ma-second-period');
                if (secondPeriod) {
                    secondPeriod.classList.toggle('hidden', e.target.value !== 'ma');
                }
            }
        });

        // Listen for indicator changes
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('indicator-select')) {
                const conditionId = parseInt(e.target.closest('.condition-group').dataset.conditionId);
                this.handleIndicatorChange(conditionId, e.target.value);
            }
        });
    }

    handleIndicatorChange(conditionId, indicatorType) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const paramsContainer = condition.querySelector('.indicator-params');
        
        // Store the indicator type
        this.conditions.set(conditionId, { type: indicatorType, params: {} });
        
        // Load indicator parameters template
        const template = document.getElementById(`${indicatorType}-params-template`);
        if (template) {
            paramsContainer.innerHTML = template.innerHTML;
            
            // Setup specific indicator handlers
            switch (indicatorType) {
                case 'rsi':
                    this.setupRSIHandlers(conditionId);
                    break;
                case 'macd':
                    this.setupMACDHandlers(conditionId);
                    break;
                case 'ma':
                    this.setupMAHandlers(conditionId);
                    break;
                case 'bb':
                    this.setupBBHandlers(conditionId);
                    break;
                case 'stoch':
                    this.setupStochHandlers(conditionId);
                    break;
                case 'tv':
                    this.setupTVHandlers(conditionId);
                    break;
            }
        }
        
        this.validateConditions();
    }

    setupRSIHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            period: condition.querySelector('.rsi-period'),
            overbought: condition.querySelector('.rsi-overbought'),
            oversold: condition.querySelector('.rsi-oversold')
        };

        const updateParams = () => {
            this.conditions.get(conditionId).params = {
                period: parseInt(params.period.value),
                overbought: parseInt(params.overbought.value),
                oversold: parseInt(params.oversold.value)
            };
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            input.addEventListener('change', updateParams);
        });

        updateParams(); // Initialize with default values
    }

    setupMACDHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            fast: condition.querySelector('.macd-fast'),
            slow: condition.querySelector('.macd-slow'),
            signal: condition.querySelector('.macd-signal')
        };

        const updateParams = () => {
            this.conditions.get(conditionId).params = {
                fastPeriod: parseInt(params.fast.value),
                slowPeriod: parseInt(params.slow.value),
                signalPeriod: parseInt(params.signal.value)
            };
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            input.addEventListener('change', updateParams);
        });

        updateParams();
    }

    setupMAHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            type: condition.querySelector('.ma-type'),
            period: condition.querySelector('.ma-period'),
            compare: condition.querySelector('.ma-compare'),
            secondPeriod: condition.querySelector('.ma-second-period input')
        };

        const updateParams = () => {
            const maParams = {
                type: params.type.value,
                period: parseInt(params.period.value),
                compareWith: params.compare.value
            };

            if (params.compare.value === 'ma') {
                maParams.secondPeriod = parseInt(params.secondPeriod.value);
            }

            this.conditions.get(conditionId).params = maParams;
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            if (input) input.addEventListener('change', updateParams);
        });

        updateParams();
    }

    setupBBHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            period: condition.querySelector('.bb-period'),
            std: condition.querySelector('.bb-std'),
            level: condition.querySelector('.bb-level')
        };

        const updateParams = () => {
            this.conditions.get(conditionId).params = {
                period: parseInt(params.period.value),
                standardDeviations: parseFloat(params.std.value),
                bLevel: parseFloat(params.level.value)
            };
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            input.addEventListener('change', updateParams);
        });

        updateParams();
    }

    setupStochHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            kPeriod: condition.querySelector('.stoch-k'),
            dPeriod: condition.querySelector('.stoch-d'),
            smooth: condition.querySelector('.stoch-smooth'),
            overbought: condition.querySelector('.stoch-overbought'),
            oversold: condition.querySelector('.stoch-oversold')
        };

        const updateParams = () => {
            this.conditions.get(conditionId).params = {
                kPeriod: parseInt(params.kPeriod.value),
                dPeriod: parseInt(params.dPeriod.value),
                smooth: parseInt(params.smooth.value),
                overbought: parseInt(params.overbought.value),
                oversold: parseInt(params.oversold.value)
            };
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            input.addEventListener('change', updateParams);
        });

        updateParams();
    }

    setupTVHandlers(conditionId) {
        const condition = document.querySelector(`[data-condition-id="${conditionId}"]`);
        const params = {
            signalType: condition.querySelector('.tv-signal-type'),
            timeframe: condition.querySelector('.tv-timeframe')
        };

        const updateParams = () => {
            this.conditions.get(conditionId).params = {
                signalType: params.signalType.value,
                timeframe: params.timeframe.value
            };
            this.validateConditions();
        };

        Object.values(params).forEach(input => {
            input.addEventListener('change', updateParams);
        });

        updateParams();
    }

    validateConditions() {
        let isValid = true;
        
        // Check if at least one condition exists
        if (this.conditions.size === 0) {
            isValid = false;
        }

        // Validate each condition
        this.conditions.forEach((condition, id) => {
            const element = document.querySelector(`[data-condition-id="${id}"]`);
            if (!condition.type || Object.keys(condition.params).length === 0) {
                isValid = false;
                element?.classList.add('border-red-500');
            } else {
                element?.classList.remove('border-red-500');
            }
        });

        // Emit validation event
        const event = new CustomEvent('conditionsValidated', {
            detail: { isValid, conditions: this.getConditions() }
        });
        document.dispatchEvent(event);

        return isValid;
    }

    getConditions() {
        const conditions = {
            combination: document.getElementById('conditionCombination').value,
            items: Array.from(this.conditions.entries()).map(([id, condition]) => ({
                id,
                ...condition
            }))
        };
        return conditions;
    }

    loadConditions(conditions) {
        // Clear existing conditions
        document.getElementById('conditionsContainer').innerHTML = '';
        this.conditions.clear();
        
        // Load saved conditions
        conditions.items.forEach(condition => {
            this.nextId = Math.max(this.nextId, condition.id + 1);
            this.addCondition();
            const element = document.querySelector(`[data-condition-id="${condition.id}"]`);
            if (element) {
                const select = element.querySelector('.indicator-select');
                select.value = condition.type;
                this.handleIndicatorChange(condition.id, condition.type);
                
                // Load parameters
                Object.entries(condition.params).forEach(([key, value]) => {
                    const input = element.querySelector(`[name="${key}"]`);
                    if (input) input.value = value;
                });
            }
        });

        // Set combination
        document.getElementById('conditionCombination').value = conditions.combination;
        
        this.validateConditions();
    }
}

// Initialize the manager
let dealConditionsManager;
document.addEventListener('DOMContentLoaded', () => {
    dealConditionsManager = new DealConditionsManager();
});
