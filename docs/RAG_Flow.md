## RAG Flow 
 
 
 ```
                 RAGPipeline
                      │
                      ▼
               RetrievalPipeline
                      │
                      ▼
             List[RetrievedChunk]
                      │
                      ▼
               PromptBuilder
                      │
                      ▼
             List[ChatMessage]
                      │
                      ▼
                 OpenAIChat
                      │
                      ▼
               ChatResponse
                      │
                      ▼
                RAGResponse
                
```


