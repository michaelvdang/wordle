stats: uvicorn --port $PORT UserStatsRedis:app --reload --root-path /api/v1
check: uvicorn --port $PORT WordCheck:app --reload --root-path /api/v1
validate: uvicorn --port $PORT WordValidation:app --reload --root-path /api/v1
play: uvicorn --port $PORT Play:app --reload --root-path /api/v1
orchestratorb: uvicorn --port $PORT Orchestrator:app --reload --root-path /api/v1
tester: uvicorn --port $PORT testApp:app --reload --root-path /api/v1
# traefik must be last
traefik: ./traefik --configFile=traefik.toml