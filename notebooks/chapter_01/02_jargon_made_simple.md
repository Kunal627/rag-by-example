## Key Concepts & Jargon

Before we jump into building our RAG system, let’s understand some common terms in plain English, using examples you can actually picture.

---

### Chunk

A **chunk** is a manageable piece of text.

- Why? LLMs have a limit on how much text they can process at once.
- Imagine reading a long novel. You wouldn’t try to remember the entire book in one go — you read chapter by chapter. Each chapter (or even a few paragraphs) is a chunk. Similarly, a chunk is a slice of your text that the model can “digest” easily.

---

### Embedding

An **embedding** is a way to turn text into numbers so the computer can “understand” it.

- The model uses embeddings to figure out which pieces of text are similar to each other.
- Think of online shopping recommendations. When you look at a pair of shoes, Amazon suggests similar shoes. Behind the scenes, it’s comparing numerical features — size, color, style. In RAG, embeddings do the same thing for text: they assign a numerical “fingerprint” to each chunk, so the system knows which chunks are most relevant to your query.

---

### Token

A **token** is a unit of text that the model processes — usually a word, part of a word, or even punctuation.

- Imagine building a LEGO model. Each LEGO brick is a token. Alone, it doesn’t do much, but put enough together, and you can build a sentence, paragraph, or even a whole story. LLMs count and process tokens, not letters, so every chunk gets broken down into these “bricks” for the model to understand.

---

### Vector Store

A **vector store** is where embeddings are stored so they can be searched efficiently.

- Imagine a library where every book has a secret code that summarizes its content. When you ask the librarian for a topic, they don’t read every book — they check the codes and pull the books that are closest to what you asked. In RAG, the vector store is that magical library, storing embeddings so the retriever can quickly find the right chunks.

---

### Retriever & Generator

- **Retriever**: Finds the relevant chunks from your data (the librarian).
- **Generator**: Reads those chunks and crafts a coherent, human-readable answer (the storyteller).
- Suppose you want to cook a new dish. The retriever is like a friend who finds the recipe in a cookbook or online blog. The generator is like a cooking coach who explains each step in plain English, so you don’t accidentally put salt in your coffee. Together, they make sure your dish (or answer) comes out perfect.

---

**Takeaway:**
RAG is basically teamwork: the **retriever fetches the right info**, the **generator turns it into something you can actually understand**, and embeddings, tokens, and chunks are the tools that make this possible. With these concepts clear, you’re ready to prep your data and start building!
