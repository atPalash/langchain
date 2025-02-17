**Steps**
1. Follow https://github.com/ollama/ollama to install with llama 3.2
2. Test locally
3. Allow remote to access ollama https://chatboxai.app/en/help-center/connect-chatbox-remote-ollama-service-guide
    ```
    systemctl edit ollama.service
    [Service]
    Environment="OLLAMA_HOST=0.0.0.0"
    Environment="OLLAMA_ORIGINS=*"
    systemctl daemon-reload
    systemctl restart ollama
    ```
4. test from remote pc. Open browser and go to <llama pc>:11434. Check llama is running is printed
5. Configure local vscode continue configuration file to add llama running on server
```
    {
      "apiBase": "http://192.168.0.31:11434/",
      "title": "Llama3server",
      "provider": "ollama",
      "model": "llama3.2"
    },

```
    
