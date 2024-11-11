} else {
            // Validate exit conditions
            if (this.config.exitConditions.size === 0) {
                isValid = false;
                errors.push('At least one exit condition is required');
            }

            this.config.exitConditions.forEach((condition) => {
                if (!this.validateExitCondition(condition)) {
                    isValid = false;
                    errors.push(`Invalid exit condition parameters for ${condition.type}`);
                }
            });
        }

        // Validate trailing settings
        if (this.config.enableTrailing) {
            if (this.config.trailingDeviation <= 0) {
                isValid = false;
                errors.push('Trailing deviation must be greater than 0');
            }

            if (this.config.trailingActivation === 'profit' && 
                this.config.trailingActivationValue <= 0) {
                isValid = false;
                errors.push('Trailing activation profit must be greater than 0');
            }
        }

        // Update UI with validation state
        this.updateValidationUI(isValid, errors);

        // Emit validation event
        const event = new CustomEvent('takeProfitValidated', {
            detail: { 
                isValid, 
                errors,
                config: this.getConfig() 
            }
        });
        document.dispatchEvent(event);

        return isValid;
    }

    validateExitCondition(condition) {
        switch (condition.type) {
            case 'rsi':
                return this.validateRSIExitCondition(condition);
            case 'macd':
                return this.validateMACDExitCondition(condition);
            case 'ma':
                return this.validateMAExitCondition(condition);
            case 'bb':
                return this.validateBBExitCondition(condition);
            case 'stoch':
                return this.validateStochExitCondition(condition);
            case 'supertrend':
                return this.validateSupertrendExitCondition(condition);
            case 'atr':
                return this.validateATRExitCondition(condition);
            case 'adx':
                return this.validateADXExitCondition(condition);
            case 'ichi':
                return this.validateIchimokuExitCondition(condition);
            case 'pivot':
                return this.validatePivotExitCondition(condition);
            case 'tv':
                return this.validateTVExitCondition(condition);
            default:
                return false;
        }
    }

    updateValidationUI(isValid, errors) {
        // Clear previous validation UI
        document.querySelectorAll('.validation-error').forEach(el => el.remove());

        if (!isValid) {
            // Add error messages to UI
            const container = document.querySelector('#takeProfitSettings');
            const errorList = document.createElement('div');
            errorList.className = 'validation-error mt-4 p-4 bg-red-50 border-l-4 border-red-400';
            errorList.innerHTML = `
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                        </svg>
                    </div>
                    <div class="ml-3">
                        <h3 class="text-sm font-medium text-red-800">Please fix the following issues:</h3>
                        <ul class="mt-2 text-sm text-red-700 list-disc list-inside">
                            ${errors.map(error => `<li>${error}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
            container.appendChild(errorList);
        }
    }

    addExitCondition() {
        const conditionId = this.nextExitConditionId++;
        const exitConditionsContainer = document.getElementById('exitConditions');
        
        // Create new exit condition HTML
        exitConditionsContainer.insertAdjacentHTML('beforeend', this.createExitConditionHTML(conditionId));
        
        // Initialize indicator select
        const select = document.querySelector(`[data-exit-condition-id="${conditionId}"] .exit-indicator-select`);
        select.addEventListener('change', (e) => this.handleExitIndicatorChange(conditionId, e.target.value));
        
        this.validateSettings();
    }

    createExitConditionHTML(conditionId) {
        return `
            <div class="condition-group" data-exit-condition-id="${conditionId}">
                <div class="flex justify-between items-center mb-2">
                    <label class="block text-sm font-medium text-gray-700">Exit Condition ${conditionId}</label>
                    <button type="button" 
                            onclick="takeProfitManager.removeExitCondition(${conditionId})"
                            class="text-red-600 hover:text-red-800">
                        Remove
                    </button>
                </div>
                <div class="grid grid-cols-1 gap-4">
                    <select class="exit-indicator-select w-full rounded-md border-gray-300 shadow-sm">
                        <option value="">Select Indicator</option>
                        ${this.getIndicatorOptions()}
                    </select>
                    <div class="exit-indicator-params"></div>
                </div>
            </div>
        `;
    }

    getIndicatorOptions() {
        const indicators = [
            { value: 'rsi', label: 'RSI' },
            { value: 'macd', label: 'MACD' },
            { value: 'ma', label: 'Moving Average' },
            { value: 'bb', label: 'Bollinger Band %B' },
            { value: 'stoch', label: 'Stochastic' },
            { value: 'supertrend', label: 'SuperTrend' },
            { value: 'atr', label: 'ATR' },
            { value: 'adx', label: 'ADX' },
            { value: 'ichi', label: 'Ichimoku Cloud' },
            { value: 'pivot', label: 'Pivot Points' },
            { value: 'tv', label: 'TradingView Signal' }
        ];

        return indicators.map(ind => 
            `<option value="${ind.value}">${ind.label}</option>`
        ).join('');
    }

    handleExitIndicatorChange(conditionId, indicatorType) {
        const container = document.querySelector(`[data-exit-condition-id="${conditionId}"] .exit-indicator-params`);
        
        if (indicatorType) {
            this.config.exitConditions.set(conditionId, { type: indicatorType, params: {} });
            container.innerHTML = this.getIndicatorParamsHTML(indicatorType, conditionId);
            this.initializeIndicatorParams(conditionId, indicatorType);
        } else {
            this.config.exitConditions.delete(conditionId);
            container.innerHTML = '';
        }
        
        this.validateSettings();
    }

    getConfig() {
        return {
            ...this.config,
            exitConditions: Array.from(this.config.exitConditions.values())
        };
    }

    loadConfig(config) {
        this.config = {
            ...config,
            exitConditions: new Map(config.exitConditions.map((c, i) => [i, c]))
        };
        this.updateUI();
    }
}

// Initialize the manager
let takeProfitManager;
document.addEventListener('DOMContentLoaded', () => {
    takeProfitManager = new TakeProfitManager();
});
