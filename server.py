import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "FT_api.main:FT_api", host="0.0.0.0", port=8000, reload=True, proxy_headers=True
    )

# if __name__ == "__main__":
#   uvicorn.run(
#     "FT_api.main:FT_api",
#     host="localhost",
#     port=8000,
#     reload=True,
#     proxy_headers=True,
#   )
