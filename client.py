#!/usr/bin/env python3
import argparse, httpx, sys, json, os
import json

CONFIG_FILE = "config.json"
with open(CONFIG_FILE, encoding="utf-8") as f:
    cfg = json.load(f)

HOST = cfg.get("host", "127.0.0.1")
PORT = cfg.get("port", 8000)
SCHEME = cfg.get("scheme", "http")
MODEL = cfg.get("model", "THUDM/GLM-4-9B-0414")


def chat_once(q, model, key, url):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "question": q,
        "model": model
    }
    try:
        r = httpx.post(f"{url}/chat", json=data, headers=headers, timeout=60)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        if(e.response.status_code == 401):
            print("密钥错误。请检查你输入的密钥是否正确。")
        else:
            print(f"HTTP服务异常: {e}\n请检查你输入的模型名是否正确。")
        sys.exit(1)
    except httpx.HTTPError as e:
        print(f"HTTP请求异常: {e}\n请检查你输入的协议、主机名、端口号是否正确，或检查你的网络连接。")
        sys.exit(1)
        
    return r.text

def main():
    p = argparse.ArgumentParser()
    p.add_argument("question")
    p.add_argument("-k", "--key", required=True)
    p.add_argument("-m", "--model", default=MODEL)
    p.add_argument("--host", default=HOST)
    p.add_argument("--port", type=int, default=PORT)
    p.add_argument("--scheme", default=SCHEME)
    args = p.parse_args()

    answer = chat_once(args.question, args.model, args.key, f"{args.scheme}://{args.host}:{args.port}")
    answer_json = json.loads(answer)
    content = answer_json["content"]
    reasoning_content = answer_json["reasoning_content"]
    total_tokens = answer_json["total_tokens"]

    print("思考过程：\n")
    print(reasoning_content)
    print("\n回答：\n")
    print(content)
    print(f"\n总tokens：{total_tokens}")

if __name__ == "__main__":
    main()