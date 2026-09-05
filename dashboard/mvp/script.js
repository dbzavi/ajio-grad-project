document.addEventListener('DOMContentLoaded', () => {
    
    // --- Virtual Try-On Logic (Simulation) ---
    const vtoBtn = document.getElementById('vto-btn');
    const resetVtoBtn = document.getElementById('reset-vto-btn');
    const userImg = document.getElementById('user-img');
    const productImg = document.getElementById('product-img');
    const vtoOverlay = document.getElementById('vto-overlay');

    vtoBtn.addEventListener('click', () => {
        // Show loading overlay
        vtoOverlay.style.display = 'flex';
        
        // Simulate API delay for processing the photo swap
        setTimeout(() => {
            vtoOverlay.style.display = 'none';
            userImg.style.display = 'none';
            productImg.style.display = 'block';
            
            vtoBtn.style.display = 'none';
            resetVtoBtn.style.display = 'inline-block';
        }, 1500);
    });

    resetVtoBtn.addEventListener('click', () => {
        productImg.style.display = 'none';
        userImg.style.display = 'block';
        
        resetVtoBtn.style.display = 'none';
        vtoBtn.style.display = 'inline-block';
    });


    // --- Fit-Match AI Logic (Real RAG Backend Call) ---
    const fitForm = document.getElementById('fit-form');
    const fitLoading = document.getElementById('fit-loading');
    const fitResult = document.getElementById('fit-result');
    const recText = document.getElementById('recommendation-text');

    fitForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const height = document.getElementById('height').value;
        const weight = document.getElementById('weight').value;
        const fitPref = document.getElementById('fit_pref').value;

        // UI States
        fitForm.style.display = 'none';
        fitResult.style.display = 'none';
        fitLoading.style.display = 'block';

        try {
            const response = await fetch('/api/predict_fit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    height: height,
                    weight: weight,
                    fit_preference: fitPref
                })
            });

            const data = await response.json();
            
            fitLoading.style.display = 'none';
            recText.innerHTML = data.recommendation; // Use innerHTML since Groq might return bolding etc.
            fitResult.style.display = 'block';
            
            // Re-show form for another try
            setTimeout(() => {
                fitForm.style.display = 'block';
            }, 500);

        } catch (error) {
            console.error('Error fetching fit prediction:', error);
            fitLoading.style.display = 'none';
            recText.innerText = "Error connecting to AI Assistant. Please ensure backend is running.";
            fitResult.style.display = 'block';
            fitForm.style.display = 'block';
        }
    });
});
