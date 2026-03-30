
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

    let dict = {};
    data.data.forEach(entry => {
        id = entry['id'];
        if (id) {
            dict[id] = entry
        }
    })

    localStorage.setItem('moves_version', realVersion.version)
    localStorage.setItem('moves_cache', JSON.stringify(dict))

    console.log("Fetching fresh move data to cache.")

    return dict
}

async function process_page() {
    let moves = await get_moves();

    const move_entry = document.querySelectorAll('div#move-entry');
    move_entry.forEach(entry => {
        const moveId = entry.getAttribute('move');
        const move = moves[moveId];

        const binfo = entry.querySelector('div#basic-info');
        
        if (move) {
            binfo.innerHTML = `
                <p>${move.name || moveId || '???'}</p>
                <p><img style="vertical-align:middle" src='/types/${move.type || 'Normal'}Small.png'></p>
                <p><img style="vertical-align:middle" src='/categories/${move.category || 'Status'}.png'></p>
                <p>${move.basePower || '-'}</p>
                <p>${move.pp || '-'}</p>
                <p>${move.accuracy || '-'}</p>
                <p>${move.target || '-'}</p>
                <p>${move.flags || '-'}</p>
            `;
        } else if (moveId) {
            binfo.innerHTML = `<p style="color:red">Unknown move: ${moveId}</p>`;
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {
    process_page();
});