# 📘 RAG by example

A step-by-step guide to building Retrieval-Augmented Generation (RAG) applications from scratch.
This course combines **theory + hands-on notebooks** to help you understand, implement, and optimize RAG pipelines.

---

## Table of Contents

### Pre-requisites

1. An IDE for development with python setup (and dependencies in requirements.txt)
2. Pytorch CUDA (I am running CUDA 12.6)
3. Python 3.12

### 1. Introduction

- What is RAG?
- Why do we need it?
- Real-world applications

### 2. Data Preparation

- Collecting & cleaning documents
- Chunking strategies
- Preprocessing text

### 3. Embeddings

- What are embeddings?
- Popular embedding models
- Generating and storing embeddings

### 4. Vector Databases and Retrieval Strategies

- Introduction to vector stores
- FAISS, Chroma, Pinecone, Weaviate
- Indexing and similarity search
- Dense retrieval
- Sparse retrieval (BM25)
- Hybrid retrieval

### 5. RAG Pipeline

- User → Retriever → LLM → Answer flow
- Basic pipeline implementation
- First working RAG demo

### 6. Enhancements

- Prompt engineering
- Reranking retrieved results
- Handling long contexts

### 7. Capstone Project (My Chef)

- End-to-end simple Q&A RAG app
- Run locally with Gradio
- Use LLMs running locally

---

## How to Use

- Each chapter has a **notebook** with explanations + code
- Follow in order for a progressive learning path
- Reusable Python scripts live in `common/`

---

**Caveat**:
This chatbot is a **learning project only** and is **not production-ready**. The objective of this tutorial is to build intuition on RAGS and to give enough hands on experience to learners.

---
