/**
 * Pygentic AI - Frontend Application
 * Progressive loading and enhanced UX interactions
 */

(function() {
    'use strict';

    // Progressive loading messages
    const LOADING_MESSAGES = [
        'Fetching URL content...',
        'Analyzing page structure...',
        'Extracting key information...',
        'Identifying patterns...',
        'Generating SWOT analysis...',
        'Finalizing insights...',
        'Almost there...'
    ];

    let loadingMessageIndex = 0;
    let loadingInterval = null;
    let pollCount = 0;
    let pollInterval = 1000; // Start at 1s
    const MAX_POLL_INTERVAL = 5000; // Max 5s

    /**
     * Update loading message progressively
     */
    function updateLoadingMessage() {
        const statusElement = document.getElementById('loading-status');
        if (!statusElement) return;

        if (loadingMessageIndex < LOADING_MESSAGES.length - 1) {
            loadingMessageIndex++;
        }

        statusElement.textContent = LOADING_MESSAGES[loadingMessageIndex];
        statusElement.style.animation = 'fadeIn 0.3s ease-in';
    }

    /**
     * Start progressive loading messages
     */
    function startLoadingMessages() {
        loadingMessageIndex = 0;
        pollCount = 0;
        pollInterval = 1000;

        const statusElement = document.getElementById('loading-status');
        if (statusElement) {
            statusElement.textContent = LOADING_MESSAGES[0];
        }

        // Update message every 3 seconds
        if (loadingInterval) {
            clearInterval(loadingInterval);
        }

        loadingInterval = setInterval(updateLoadingMessage, 3000);
    }

    /**
     * Stop loading messages
     */
    function stopLoadingMessages() {
        if (loadingInterval) {
            clearInterval(loadingInterval);
            loadingInterval = null;
        }
        loadingMessageIndex = 0;
    }

    /**
     * Smooth scroll to results
     */
    function scrollToResults() {
        const resultsSection = document.getElementById('result-container');
        if (resultsSection) {
            resultsSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    /**
     * Exponential backoff for polling
     */
    function calculateNextPollInterval() {
        pollCount++;

        if (pollCount > 3) {
            pollInterval = Math.min(pollInterval * 1.5, MAX_POLL_INTERVAL);
        }

        return pollInterval;
    }

    /**
     * Initialize form submission handler
     */
    function initializeForm() {
        const form = document.getElementById('swotSearch');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Start loading messages when form is submitted
            startLoadingMessages();

            // Show spinner
            const spinner = document.getElementById('spinner');
            if (spinner) {
                spinner.classList.remove('is-hidden');
            }
        });
    }

    /**
     * Monitor for analysis completion
     */
    function monitorAnalysisCompletion() {
        const resultBox = document.getElementById('result');
        if (!resultBox) return;

        // Use MutationObserver to watch for content changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && resultBox.innerHTML.trim().length > 0) {
                    // Analysis complete
                    stopLoadingMessages();

                    // Hide spinner
                    const spinner = document.getElementById('spinner');
                    if (spinner) {
                        spinner.classList.add('is-hidden');
                    }

                    // Scroll to results after a brief delay
                    setTimeout(scrollToResults, 500);

                    // Add success class for animation
                    const resultContainer = document.getElementById('result-container');
                    if (resultContainer) {
                        resultContainer.classList.add('animate-in');
                    }
                }
            });
        });

        observer.observe(resultBox, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Add button press effects
     */
    function initializeButtonEffects() {
        const buttons = document.querySelectorAll('.search-button, .error-state__button');

        buttons.forEach(button => {
            button.addEventListener('mousedown', function() {
                this.style.transform = 'scale(0.95)';
            });

            button.addEventListener('mouseup', function() {
                this.style.transform = '';
            });

            button.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }

    /**
     * Initialize smooth anchor scrolling
     */
    function initializeSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#' || !href) return;

                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    /**
     * Initialize all features on DOM ready
     */
    function initialize() {
        initializeForm();
        monitorAnalysisCompletion();
        initializeButtonEffects();
        initializeSmoothScrolling();

        console.log('✨ Pygentic AI initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

    // Export functions for external use if needed
    window.PygenticAI = {
        startLoadingMessages,
        stopLoadingMessages,
        scrollToResults
    };
})();
