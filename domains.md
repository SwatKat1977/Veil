# Veil Server Domains

Domains:
- Gateway/API
- Auth
- Campaigns
- Realtime
- Chat
- Maps/Scenes
- Storage

## 1. Gateway Service
the only public-facing service.

Handles:
* authentication,
* websocket connections,
* session tracking,
* routing,
* subscriptions.

This becomes “the multiplayer runtime.”

2. Auth Service
Tiny and boring.

Handles:
* login,
* sessions,
* tokens,
* account creation.

3. Campaign Service

Persistent world state.

Handles:
* campaigns,
* memberships,
* scenes,
* permissions,
* identities.

4. Chat Service

Actually more important than people think.

Handles:
* whispers,
* faction chats,
* GM channels,
* routing rules.

5. Scene/Map Service

Largest domain for mas/scene.

Handles:
* maps,
* fog,
* objects,
* visibility,
* annotations,
* scene state.