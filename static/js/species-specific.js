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

    return data.data
}

async function enhanceLearnset() {
    // Find the tbody by ID
    const tbody = document.getElementById('learnset-tbody');
    if (!tbody) return;
    
    // Get all rows within the tbody
    const rows = tbody.querySelectorAll('tr');
    if (rows.length === 0) return;
    
    // Ensure moves cache is loaded
    let moves = get_moves();
    console.log(moves);
    
    // Process each row
    rows.forEach(row => {
        const moveId = row.getAttribute('move');
        const move = moves[moveId];
        
        row.innerHTML = '';

        const src = row.getAttribute('src');

        if (move) {
            row.innerHTML = `
                <td>${src || '?'}</td>
                <td>${move.name || moveId || '???'}</td>
                <td><img style="vertical-align:middle" src='/types/${move.type || 'Normal'}Small.png'></td>
                <td><img style="vertical-align:middle" src='/categories/${move.category || 'Status'}.png'></td>
                <td>${move.power || '-'}</td>
                <td>${move.pp || '-'}</td>
            `;
        } else {
            row.innerHTML = `<td colspan="6" style="color:red">Unknown move: ${moveId}</td>`;
        }
    });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', () => {
    enhanceLearnset();
});