# Hybrid-Retrieval-Augmented-Generation

Combine Retrieval-Augmented Generation with Cache-Augmented Generation to improve retrieval efficiency and generation quality.

---

## Overview

This project implements a hybrid system combining retrieval-based and cache-based techniques:

- **RAG** for semantic retrieval and generation  
- **CAG** to cache frequent queries or chunks for faster response and reduced redundancy  

The goal is to maintain high quality of retrieved content while improving latency and efficiency.

---

## Motivation

- Many systems using RAG repeatedly retrieve the same or very similar documents/contexts, which causes redundant computation.  
- A cache layer can greatly reduce latency for repeated/similar queries.  
- By combining both, you get semantic richness (via embeddings) + speed (via caching).

---

## Features

- Clean and filter pipeline for text preprocessing  
- Semantic chunk classification (RoBERTa)  
- Dual storage: embeddings & structured metadata  
- Hybrid search combining keywords + embedding similarity  
- Modular & extensible for new domains or models
