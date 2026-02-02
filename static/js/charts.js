/**
 * Chart.js Configuration and Utilities
 * NeuroBank-Style Charts
 */

// Global Chart.js Configuration
Chart.defaults.color = '#94a3b8'; // text-secondary
Chart.defaults.font.family = "'Inter', 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;

// Common Chart Options
const commonChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false // We'll use custom legends
        },
        tooltip: {
            backgroundColor: 'rgba(26, 31, 55, 0.95)',
            titleColor: '#ffffff',
            bodyColor: '#94a3b8',
            borderColor: 'rgba(59, 130, 246, 0.3)',
            borderWidth: 1,
            padding: 12,
            displayColors: false,
            titleFont: {
                size: 14,
                weight: '600'
            },
            bodyFont: {
                size: 13
            },
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    if (context.parsed.y !== null) {
                        label += '$' + context.parsed.y.toLocaleString();
                    }
                    return label;
                }
            }
        }
    }
};

/**
 * Create a line chart with gradient fill
 */
function createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    // Create gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.3)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    const config = {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: data.label || 'Value',
                data: data.values,
                borderColor: '#3b82f6',
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointBackgroundColor: '#3b82f6',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2
            }]
        },
        options: {
            ...commonChartOptions,
            ...options,
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 },
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

/**
 * Create a donut chart
 */
function createDonutChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const config = {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: [
                    '#3b82f6',
                    '#60a5fa',
                    '#93c5fd'
                ],
                borderWidth: 0,
                cutout: '75%'
            }]
        },
        options: {
            ...commonChartOptions,
            ...options,
            plugins: {
                ...commonChartOptions.plugins,
                tooltip: {
                    ...commonChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return label + ': ' + percentage + '%';
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

/**
 * Create a bar chart
 */
function createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const config = {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: data.label || 'Value',
                data: data.values,
                backgroundColor: Array.isArray(data.colors) ? data.colors : '#3b82f6',
                borderRadius: 8,
                barThickness: 32
            }]
        },
        options: {
            ...commonChartOptions,
            ...options,
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 },
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    };

    return new Chart(ctx, config);
}

/**
 * Create an area chart (stacked or multiple lines)
 */
function createAreaChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    // Create gradients for multiple datasets
    const createGradient = (color, alpha = 0.3) => {
        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, color.replace(')', `, ${alpha})`).replace('rgb', 'rgba'));
       gradient.addColorStop(1, color.replace(')', ', 0)').replace('rgb', 'rgba'));
        return gradient;
    };

    const datasets = data.datasets.map((dataset, index) => ({
        label: dataset.label,
        data: dataset.values,
        borderColor: dataset.color || '#3b82f6',
        backgroundColor: createGradient(dataset.color || 'rgb(59, 130, 246)'),
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 5
    }));

    const config = {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: datasets
        },
        options: {
            ...commonChartOptions,
            ...options,
            interaction: {
                mode: 'index',
                intersect: false
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#64748b',
                        font: { size: 11 }
                    },
                    stacked: options.stacked || false
                }
            }
        }
    };

    return new Chart(ctx, config);
}

// Helper function to format currency
function formatCurrency(value) {
    return '$' + value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Helper function to format percentage
function formatPercentage(value) {
    return value.toFixed(1) + '%';
}
