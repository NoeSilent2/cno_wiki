const MovesCache = {
    cacheKey: 'pokemon_moves',
    versionKey: 'pokemon_moves_version',
    
    // Get moves, if there isnt a cache, make one
    async get() {
        const cachedVersion = localStorage.getItem(this.versionKey);
        const cachedData = localStorage.getItem(this.cacheKey);
        
        // Check if data is outdated
        const response = await fetch('/api/moves');
        const serverMoves = await response.json();
        
        if (cachedVersion === serverMoves.version && cachedData) {
            // Cache is fresh, use it
            return JSON.parse(cachedData);
        }
        
        // Cache is stale or missing, update it
        localStorage.setItem(this.versionKey, serverMoves.version);
        localStorage.setItem(this.cacheKey, JSON.stringify(serverMoves.data));
        return serverMoves.data;
    },
    
    // Get details for a specific move
    async getMoveDetails(moveName) {
        const moves = await this.get();
        return moves[moveName] || {'name':'error','type':'Normal','category':'Status','pp':0};
    },
    
    // Get details for multiple moves
    async getMoveDetailsList(moveNames) {
        const moves = await this.get();
        return moveNames.map(name => ({
            name: name,
            details: moves[name] || {'name':'error','type':'Normal','category':'Status','pp':0}
        }));
    }
};