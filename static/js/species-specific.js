// Get moves from cache, if not cache, make one
async function get_moves() {
    const storedVersion = localStorage.getItem('moves_version');
    const vresponse = await fetch('/api/moves/version');
    const realVersion = await vresponse.json();

    if (storedVersion == realVersion.version) {
        const storedCache = localStorage.getItem('moves_cache');
        if (storedCache) {
            return JSON.parse(storedCache);
        }
    }
    
    const response = await fetch('/api/moves');
    const data = await response.json();

    localStorage.setItem('moves_version', realVersion.version)
    localStorage.setItem('moves_cache', JSON.stringify(data.data))

    console.log("Fetching fresh move data to cache.")

    return data.data
}

async function enhance_page() {
    let moves = await get_moves();

    const learnsets = document.querySelectorAll('tbody#learnset-tbody');
    learnsets.forEach(tbody => {
        const rows = tbody.querySelectorAll('tr');
        if (rows.length === 0) return;
        
        rows.forEach(row => {
            const moveId = row.getAttribute('move');
            const move = moves[moveId];

            const src = row.getAttribute('src');

            if (move) {
                row.innerHTML = `
                    <td>${src || '?'}</td>
                    <td>${move.name || moveId || '???'}</td>
                    <td><img style="vertical-align:middle" src='/types/${move.type || 'Normal'}Small.png'></td>
                    <td><img style="vertical-align:middle" src='/categories/${move.category || 'Status'}.png'></td>
                    <td>${move.basePower || '-'}</td>
                    <td>${move.pp || '-'}</td>
                `;
            } else if (moveId) {
                row.innerHTML = `<td colspan="6" style="color:red">Unknown move: ${moveId}</td>`;
            }
        });
    });

    document.querySelectorAll("button#collapseHead").forEach(butt => {
        const collapseRow = butt.nextElementSibling.querySelector('tr#collapseRow')

        butt.addEventListener('click', () => {
            if (collapseRow.style.height == "auto") {
                collapseRow.style.height = 0
            } else {
                collapseRow.style.height = "auto"
            }
        })
    })

    document.querySelectorAll("model-viewer#pokemon").forEach(modelViewerObject => {
        const shinyToggle = modelViewerObject.querySelector('input[type="checkbox"]');
        let modelLoaded = false;

        const imagename = shinyToggle.attributes.imagename.value;
        let imagefake = 'normal';
        if (shinyToggle.attributes.isfake.value) {
            imagefake = 'fake';
        };
        modelViewerObject.poster =`/api/pokepics/normal/${imagefake}/${imagename}.png`
        shinyToggle.addEventListener('change', () => {
            if (modelLoaded) {
                return
            }
            const imagename = shinyToggle.attributes.imagename.value;
            if (shinyToggle.checked) {
                modelViewerObject.poster =`/api/pokepics/shiny/${imagefake}/${imagename}.png`
            } else {
                modelViewerObject.poster =`/api/pokepics/normal/${imagefake}/${imagename}.png`
            }
        });

        modelViewerObject.addEventListener("load", () => {
            modelLoaded = true

            modelViewerObject.variantName = "default";

            shinyToggle.addEventListener('change', () => {
                if (shinyToggle.checked) {
                    modelViewerObject.variantName = "shiny";
                } else {
                    modelViewerObject.variantName = "default";
                }
            })

            for (const animName of modelViewerObject.availableAnimations) {
                if (animName.toLowerCase().includes('idle') && !animName.toLowerCase().includes('ride')) {
                    modelViewerObject.animationName = animName;
                    modelViewerObject.play();
                    break
                }
            }
        });
    });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', () => {
    enhance_page();
});