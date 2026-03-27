#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时AutoGLM Token服务
启动后监听 http://127.0.0.1:53699/get_token
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 替换为您的实际AutoGLM API Token
# 格式: Bearer xxx 或直接是token字符串
API_TOKEN = "YOUR_AUTOGLM_TOKEN_HERE"

class TokenHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_token':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(API_TOKEN.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # 简化日志输出
        print(f"[Token Server] {args[0]}")

def start_server(port=53699):
    server = HTTPServer(('127.0.0.1', port), TokenHandler)
    print(f"=" * 50)
    print(f"AutoGLM Token 服务已启动")
    print(f"监听地址: http://127.0.0.1:{port}/get_token")
    print(f"=" * 50)
    print(f"按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()

if __name__ == "__main__":
    import sys
    
    if API_TOKEN == "YOUR_AUTOGLM_TOKEN_HERE":
        print("警告: 请先编辑脚本，将 API_TOKEN 替换为您的实际Token!")
        print("\n获取Token的方法:")
        print("1. 登录AutoGLM平台 https://autoglm.zhipuai.cn/")
        print("2. 进入开发者中心或API管理页面")
        print("3. 复制您的API Token")
        print("4. 修改本脚本中的 API_TOKEN 变量")
        sys.exit(1)
    
    start_server()
