import { get_moves, get_abilities } from '/static/js/cache-check.js';


async function process_page() {
    let moves = await get_moves();

    const learnsets = document.querySelectorAll('tbody#learnset-tbody');
    learnsets.forEach(tbody => {
        const rows = tbody.querySelectorAll('tr');
        if (rows.length === 0) return;
        
        let highlight = false
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
            if (move || moveId) {
                if (highlight) {
                    highlight = false;
                    row.style.backgroundColor = "#111";
                } else {
                    highlight = true;
                    row.style.backgroundColor = "#000";
                }
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

        shinyToggle.addEventListener('change', () => {
            if (modelLoaded) {
                return
            }
            const imagename = shinyToggle.attributes.imagename.value;
            if (shinyToggle.checked) {
                modelViewerObject.poster =`https://img.pokemondb.net/sprites/home/shiny/${imagename}.png`
            } else {
                modelViewerObject.poster =`https://img.pokemondb.net/sprites/home/normal/${imagename}.png`
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

    const abilities = await get_abilities();
    console.log(abilities)

    const abilitytexts = document.querySelectorAll('a#ability');
    abilitytexts.forEach(a => {
        const abilityid = a.getAttribute('ability');
        const ability = abilities[abilityid]
        if (ability) {
            a.innerHTML = `${ability['name']}<p class="ability-description">${ability['desc']}</p>`
        }
    })
}


document.addEventListener('DOMContentLoaded', () => {
    process_page();
});