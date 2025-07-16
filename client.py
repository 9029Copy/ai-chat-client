#!/usr/bin/env python3
import argparse, httpx, sys, json, os
import json

CONFIG_FILE = "config.json"
with open(CONFIG_FILE, encoding="utf-8") as f:
    cfg = json.load(f)

def chat_once(q, key, url):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "text/plain"}
    r = httpx.post(f"{url}/chat", content=q, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text

def main():
    p = argparse.ArgumentParser()
    p.add_argument("question")
    p.add_argument("-k", "--key", required=True)
    p.add_argument("--host", default=cfg["host"])
    p.add_argument("--port", type=int, default=cfg["port"])
    p.add_argument("--scheme", default=cfg["scheme"])
    args = p.parse_args()

    answer = chat_once(args.question, args.key, f"{args.scheme}://{args.host}:{args.port}")
    print(answer)

if __name__ == "__main__":
    main()