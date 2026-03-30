
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
        
        let is_fake = `<i style="background:transparent" class="fa fa-xmark"></i>`
        if (move['is_fake']) {
            is_fake = `<i style="background:transparent" class="fa fa-check"></i>`
        }

        const desc = entry.getAttribute('desc');

        const binfo = entry.querySelector('div#basic-info');
        
        if (move) {
            binfo.innerHTML = `
                <div style="width:25%; min-width:142px;">
                    <h2>Basic data</h2>
                    <table style="width:100%">
                        <tbody>
                            <tr><th>Type</th>
                                <td>
                                    <img style="vertical-align:middle" src='/types/${move.type || 'Normal'}Small.png'>
                                </td>
                            </tr>
                            <tr><th>Category</th>
                                <td>
                                    <img style="vertical-align:middle" src='/categories/${move.category || 'Status'}.png'>
                                </td>
                            </tr>
                            <tr><th>Power</th>
                                <td>${move.basePower || '-'}</td>
                            </tr>
                            <tr><th>Accuracy</th>
                                <td>${move.accuracy || '-'}</td>
                            </tr>
                            <tr><th>PP</th>
                                <td>${move.pp || '-'}</td>
                            </tr>
                            <tr><th>Fake?</th>
                                <td>${is_fake || '<i style="background:transparent" class="fa fa-xmark"></i>'}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="width=75%; display:flex; flex-direction:column;">
                    <h2>Description</h2>
                    <p>${desc}</p>
                    <h2>Advanced data</h2>
                    <h3 style="display:inline-flex; gap:10px; align-items:center;">Target: <p style="font-weight:400; font-size:16px;">${move.target || '-'}</p></h3>
                    <h3 style="display:inline-flex; gap:10px; align-items:center;">Flags: <p style="font-weight:400; font-size:16px;">${move.flags || '-'}</p></h3>
                </div>
            `;
        } else if (moveId) {
            binfo.innerHTML = `<p style="color:red">Unknown move: ${moveId}</p>`;
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {
    process_page();
});