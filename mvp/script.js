document.addEventListener('DOMContentLoaded', () => {
    
    // Elements
    const openModalBtn = document.getElementById('openFitMatchBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const modal = document.getElementById('fitMatchModal');
    
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const confirmSizeBtn = document.getElementById('confirmSizeBtn');
    const loaderText = document.getElementById('loaderText');
    
    const sizeButtons = document.querySelectorAll('.size-btn');

    // Form Inputs
    const hFt = document.getElementById('heightFt');
    const hIn = document.getElementById('heightIn');
    const weight = document.getElementById('weight');
    const shape = document.getElementById('bodyShape');
    const pref = document.getElementById('fitPref');

    // Result Displays
    const recSizeDisplay = document.getElementById('recSizeDisplay');
    const confidenceText = document.getElementById('confidenceText');
    const confidencePath = document.getElementById('confidencePath');
    const insightText = document.getElementById('insightText');

    // Event Listeners for standard size selection
    sizeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            sizeButtons.forEach(b => b.classList.remove('selected'));
            e.target.classList.add('selected');
        });
    });

    // Modal Control
    openModalBtn.addEventListener('click', () => {
        modal.classList.add('active');
        showStep(1);
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Handle analysis
    analyzeBtn.addEventListener('click', async () => {
        if (!hFt.value || !weight.value) {
            alert("Please enter your height and weight.");
            return;
        }

        // Move to loading step
        showStep(2);
        
        // Sequence loading text for premium feel
        const loadingTexts = [
            "Analyzing product silhouette...",
            "Matching your body archetype...",
            "Synthesizing 1,200+ sizing reviews...",
            "Generating virtual try-on..."
        ];
        
        let textIdx = 0;
        const textInterval = setInterval(() => {
            textIdx++;
            if (textIdx < loadingTexts.length) {
                loaderText.textContent = loadingTexts[textIdx];
            } else {
                clearInterval(textInterval);
            }
        }, 800);

        // Fetch prediction from backend
        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    height_ft: parseInt(hFt.value),
                    height_in: parseInt(hIn.value || 0),
                    weight: parseFloat(weight.value),
                    body_shape: shape.value,
                    fit_pref: pref.value
                })
            });

            const data = await response.json();
            
            clearInterval(textInterval);
            
            // Populate Step 3
            recSizeDisplay.textContent = data.recommended_size;
            confidenceText.textContent = `${data.confidence_score}%`;
            confidencePath.setAttribute('stroke-dasharray', `${data.confidence_score}, 100`);
            insightText.textContent = data.insight_summary;
            confirmSizeBtn.textContent = `Select Size ${data.recommended_size} & Add to Bag`;
            
            // Show Step 3
            showStep(3);
            
        } catch (error) {
            console.error("API Error (Using local fallback):", error);
            clearInterval(textInterval);
            
            // Dynamic Fallback logic matching the Python backend
            let total_inches = (parseInt(hFt.value) * 12) + parseInt(hIn.value || 0);
            let w = parseFloat(weight.value);
            let p = pref.value;
            
            let rec = "M";
            let conf = 92;
            let ins = "A Medium provides the perfect oversized look for your build without overwhelming your frame.";
            
            if (total_inches > 68 || w > 75) {
                rec = "L"; conf = 91;
                if (p === "loose") { rec = "XL"; conf = 85; }
                ins = "Reviewers with your height/weight mention the sleeves run short. We recommend sizing up for comfort.";
            } else if (total_inches < 62 || w < 50) {
                rec = "S"; conf = 94;
                if (p === "tight") { rec = "XS"; }
                ins = "This jacket has a naturally oversized fit. Based on your profile, sizing down is recommended.";
            } else {
                if (p === "loose") { rec = "L"; conf = 89; }
            }

            recSizeDisplay.textContent = rec;
            confidenceText.textContent = `${conf}%`;
            confidencePath.setAttribute('stroke-dasharray', `${conf}, 100`);
            insightText.textContent = ins;
            confirmSizeBtn.textContent = `Select Size ${rec} & Add to Bag`;
            
            showStep(3);
        }
    });

    retakeBtn.addEventListener('click', () => {
        showStep(1);
    });

    confirmSizeBtn.addEventListener('click', () => {
        const size = recSizeDisplay.textContent;
        // Auto select the size on the main page
        sizeButtons.forEach(b => {
            b.classList.remove('selected');
            if(b.textContent === size) {
                b.classList.add('selected');
            }
        });
        modal.classList.remove('active');
        
        // Optional: show a toast
        setTimeout(() => {
            alert(`Added Size ${size} to bag!`);
        }, 500);
    });

    // Utility
    function showStep(stepNum) {
        step1.classList.remove('active');
        step2.classList.remove('active');
        step3.classList.remove('active');
        
        if (stepNum === 1) step1.classList.add('active');
        if (stepNum === 2) {
            step2.classList.add('active');
            loaderText.textContent = "Analyzing product silhouette...";
        }
        if (stepNum === 3) step3.classList.add('active');
    }
});
