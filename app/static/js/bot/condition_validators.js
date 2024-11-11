const ConditionValidators = {
    rsi: (params) => {
        const { period, overbought, oversold } = params;
        return (
            period > 0 &&
            overbought > oversold &&
            oversold >= 0 &&
            overbought <= 100
        );
    },

    macd: (params) => {
        const { fastPeriod, slowPeriod, signalPeriod } = params;
        return (
            fastPeriod > 0 &&
            slowPeriod > fastPeriod &&
            signalPeriod > 0
        );
    },

    ma: (params) => {
        const { period, type, compareWith, secondPeriod } = params;
        const validPeriod = period > 0;
        const validType = ['sma', 'ema'].includes(type);
        
        if (compareWith === 'ma') {
            return validPeriod && validType && secondPeriod > 0;
        }
        return validPeriod && validType;
    },

    bb: (params) => {
        const { period, standardDeviations, bLevel } = params;
        return (
            period > 0 &&
            standardDeviations > 0 &&
            bLevel >= 0 &&
            bLevel <= 1
        );
    },

    stoch: (params) => {
        const { kPeriod, dPeriod, smooth, overbought, oversold } = params;
        return (
            kPeriod > 0 &&
            dPeriod > 0 &&
            smooth > 0 &&
            overbought > oversold &&
            oversold >= 0 &&
            overbought <= 100
        );
    },

    tv: (params) => {
        const { signalType, timeframe } = params;
        const validSignalTypes = ['strong_buy', 'buy', 'neutral', 'sell', 'strong_sell'];
        const validTimeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d'];
        
        return (
            validSignalTypes.includes(signalType) &&
            validTimeframes.includes(timeframe)
        );
    }
};
