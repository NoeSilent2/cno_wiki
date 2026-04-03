let versions = {}
async function get_versions() {
    if (Object.keys(versions).length != 0) {
        console.log(versions)
        return versions
    }
    const title = document.querySelector('header#versions');
    let moves_version = title.getAttribute('vmoves');
    let abilities_version = title.getAttribute('vabilities');
    console.log(moves_version);
    console.log(abilities_version);
    if (moves_version && abilities_version) {
        versions = {'moves': moves_version, 'abilities': abilities_version};
        return versions
    }
    const vresponse = await fetch ('/api/moves/version');
    const realVersion = await vresponse.json();
    console.log(realVersion)
    if (!moves_version) {
        moves_version = realVersion.moves
    }
    if (!abilities_version) {
        abilities_version = realVersion.abilities
    }
    versions = {'moves': moves_version, 'abilities': abilities_version}
    return versions
}

export async function get_moves() {
    const storedVersion = localStorage.getItem('moves_version');
    const realVersion = await get_versions();

    if (storedVersion == realVersion.moves) {
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

    localStorage.setItem('moves_version', realVersion.moves);
    localStorage.setItem('moves_cache', JSON.stringify(dict));

    console.log("Fetching fresh move data to cache.");

    return dict
}

export async function get_abilities() {
    const storedVersion = localStorage.getItem('abilities_version');
    const realVersion = await get_versions();

    if (storedVersion == realVersion.abilities) {
        const storedCache = localStorage.getItem('abilities_cache');
        if (storedCache) {
            return JSON.parse(storedCache);
        }
    }
    
    const response = await fetch('/api/abilities');
    const data = await response.json();

    localStorage.setItem('abilities_version', realVersion.abilities);
    localStorage.setItem('abilities_cache', JSON.stringify(data.data));

    console.log("Fetching fresh ability data to cache.");

    return data.data
}