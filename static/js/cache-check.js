export async function get_moves() {
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
        const id = entry['id'];
        if (id) {
            dict[id] = entry
        }
    })

    localStorage.setItem('moves_version', realVersion.version)
    localStorage.setItem('moves_cache', JSON.stringify(dict))

    console.log("Fetching fresh move data to cache.")

    return dict
}

export async function get_abilities() {
    const storedVersion = localStorage.getItem('abilities_version');
    const vresponse = await fetch('/api/abilities/version');
    const realVersion = await vresponse.json();

    if (storedVersion == realVersion.version) {
        const storedCache = localStorage.getItem('abilities_cache');
        if (storedCache) {
            return JSON.parse(storedCache);
        }
    }
    
    const response = await fetch('/api/abilities');
    const data = await response.json();

    localStorage.setItem('abilities_version', realVersion.version)
    localStorage.setItem('abilities_cache', data.data)

    console.log("Fetching fresh ability data to cache.")

    return data.data
}