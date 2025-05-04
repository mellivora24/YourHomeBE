async def process_log(log: dict):
    if "error" in log["content"].lower():
        print(f"Warning: {log['content']}")