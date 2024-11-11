class ValidationHelpers {
    static validateNumber(value, min = 0, max = Infinity) {
        const num = parseFloat(value);
        return !isNaN(num) && num >= min && num <= max;
    }

    static showError(inputElement, message) {
        const errorId = `${inputElement.id}Error`;
        let errorEl = document.getElementById(errorId);
        
        if (!errorEl) {
            errorEl = document.createElement('p');
            errorEl.id = errorId;
            errorEl.className = 'mt-1 text-sm text-red-600';
            inputElement.parentNode.appendChild(errorEl);
        }
        
        errorEl.textContent = message;
        inputElement.classList.add('border-red-500');
    }

    static clearError(inputElement) {
        const errorId = `${inputElement.id}Error`;
        const errorEl = document.getElementById(errorId);
        
        if (errorEl) {
            errorEl.remove();
        }
        
        inputElement.classList.remove('border-red-500');
    }
}

// Add to global scope
window.ValidationHelpers = ValidationHelpers;
